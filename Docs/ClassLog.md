---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.1
kernelspec:
  display_name: Python 3 (phys-581-2021)
  language: python
  name: phys-581-2021
metadata:
   execution:
      timeout: 30
---

Class Log
=========

<!--
pi = 11.00100100001111110110
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
[3, 5, 5, 6, 7, 8, 8, 9, 9, 10, 10, 11]
[11, 101, 101, 110, 111, 1000, 1001, 1001, 1010, 1010, 1011]

10^(2*digits-2)
2^(2*digits-4)

10^0 = 1 digit
10^2 = 2 digits
10^4 = 3 digits


     0b1 = 1                = 1
1    0b11 = 3          2^0  = 2
4    0b110 = 6         2^2  = 3
16   0b1100 = 12       2^4  = 4 digits
64   0b11001 = 25      2^6  = 5 digits
256  0b110010 = 50     2^8  = 6 digits
1024 0b1100100 = 100   2^10 = 7 digits
0b11001001 = 201
0b110010010 = 402
0b1100100100 = 804
0b11001001000 = 1608
0b110010010000 = 3216
-->

Fri 29 Oct 2021
---------------
In class we considered the numerical error accumulation in a chaotic system by evolving
forward and backward in time.  This gives something related to the [Loschmidt
echo](http://www.scholarpedia.org/article/Loschmidt_echo).


Fri 24 Sept 2021
----------------

**Plan:**

* Tell students to use a generated CC number (CITI has one) so they can use the shared
    runners on GitLab.  (I tried it with a $1 limit and it was fine.)
* Review error estimates, then start demonstrating Euler's method.  Maybe do this with
    the Lorenz system?
* Discuss Stiff equations?  Maybe construct an example.

```{code-cell} ipython3
%pylab inline --no-import-all
from scipy.integrate import solve_ivp

sigma = 10.0
beta = 8.0/3
rho = 28.0

q0 = (1.0, 1.0, 1.0)
t0 = 0.0

def fun(t, q):
   """Lorenz equations."""
   x, y, z = q
   return (sigma * (y-x), x * (rho - z) - y, x * y - beta * z)


T = 30.0
tols = [1e-3, 1e-5, 1e-8, 1e-12]
ress = [solve_ivp(fun, t_span=(0, T), y0=q0, atol=_tol, rtol=_tol/10, 
                  dense_output=True)
        for _tol in tols]

fig, ax = plt.subplots()

res_best = ress[-1]
ts = res_best.t
qs = res_best.y

line_styles = ['-', '--', '-.']
for n, tol in enumerate(tols[:-1]):
    res = ress[n]
    err = abs(res.sol(ts) - qs).max(axis=0)
    l, = ax.semilogy(ts, err, ls=line_styles[n], label=f"tol={tol}")
    ax.axhline([tol], c=l.get_c(), ls=':')
ax.legend()
ax.set(xlabel='T', ylabel='max abs err');
```


Wed 22 Sept 2021
----------------

We started working with the simple 1D problem posed on Monday, but stated *without the
solution*.

$$
  \dot{y}(t) = -ty(t), \qquad y(0) = 1.
$$

```{code-cell} ipython3

%pylab inline --no-import-all
from scipy.integrate import solve_ivp

# Initial condition
y0 = 1.0

def fun(t, y):
    return -t*y

t0 = 0.0
tf = 3.0
res = solve_ivp(
    fun, t_span=(t0, tf),
    y0=[y0],  # Gotcha 1:
    t_eval=np.linspace(t0, tf, 100), # Gotcha 3:
    max_step=0.1,
)

fig, ax = plt.subplots()

ts = res.t
ys = res.y[0]  # Gotcha 2:

ax.plot(ts, ys)
ax.set(xlabel='t', ylabel='y');
```

There are still a few "Gotcha"s here which need to be carefully addressed:

1. Reading the [`solve_ivp`] docs carefully, one sees that the parameter `y0` has the
    following type:

    > **y0** : ***array_like, shape (n,)***

    The following error is obtained:
    
    ```python
    res = solve_ivp(fun, t_span=(t0, tf), y0=y0)
    ...
    ValueError: `y0` must be 1-dimensional.
    ```
    
    One needs to explain that floats are *0-dimensional*, so we need to put the initial
    condition into a list or an array.
    
2. Similarly, in the results, `res.y.shape == (1, Nt)` because [`solve_ivp`] is setup to
    deal with a vector of parameters.  Thus, we need to extract the zero-th element
    here.  This was most easily explained in terms of the previous problem where `x =
    res.y[0]`, `y = res.y[1]`, etc.
    
    This issue was typically encountered if students tried:
    
    ```python
    ...
    ax.plot(res.t, res.y)
    ...
    ValueError: x and y must have same first dimension, but have shapes (100,) and (1, 100)
    ```
    
3. The third "Gotcha" is that if you just use the default arguments, you get a very
    low-resolution plot (shown below).  The reason is that the solver is adaptive, only
    evaluating the function where needed.  To get more points, we need to either specify
    `min_step` or `t_eval`.  I discussed both.
    
    I mentioned a third option shown below of using `dense_output=True`, but did not
    show this in class: 

      
```{code-cell} ipython3
res = solve_ivp(fun, t_span=(t0, tf), y0=[y0], dense_output=True)
plt.plot(res.t, res.y[0])

ts = np.linspace(t0, tf, 100)
plt.plot(ts, res.sol(ts)[0], ':', label='dense solution')
plt.gca().set(xlabel='t', ylabel='y');
plt.legend()
```

We then solved the IVP and looked at the errors:

$$
    \int_{y_0}^{y} \frac{1}{y} \d{y} =  \int_{t_0}^{t} -t\d{t}, \qquad
    \ln \frac{y}{y_0} = -\frac{t^2-t0^2}{2}\\
    y(t) = y_0 e^{-(t^2-t_0^2)/2}.
$$

```{code-cell} ipython3
res = solve_ivp(fun, t_span=(t0, tf), y0=[y0], rtol=1e-5, atol=1e-5)

ts = res.t
ys = res.y[0]
ys_exact = y0 * np.exp(-(ts**2 - t0**2)/2)
abs_err = abs(ys_exact - ys)
rel_err = abs(abs_err/ys_exact)

fig, ax = plt.subplots()
ax.semilogy(ts, abs_err, label='abs_err')
ax.semilogy(ts, rel_err, label='rel_err')
ax.legend()
ax.set(xlabel='t', ylabel='err');
```

We then explored changing the tolerances a bit and discussed absolute vs. relative
errors.  I explained that if you scale your problem well, then these are roughly the
same, but that usually the relative tolerance is more important (significant digits).
However, when your solution is zero, your relative error will go through the roof, so
you need to fallback on the absolute error.

* Students asked why this plot looks so jumpy.  I explained that if the solver is doing
  what it claims, then the solution will oscillate about the true solution within the
  specified errors, but that how it does this is up to the solver details.


Mon 20 Sept 2021
----------------

Today we worked on setting up ODE's for use with [`solve_ivp`].  We started with the
problem of solving for the motion of a projectile in a constant downward gravitational
field, allowing for drag:

```{code-cell} ipython3

%pylab inline --no-import-all
from scipy.integrate import solve_ivp

m = 1.0        # Mass
g = 9.81       # Acceleration due to gravity
lam = 0.5      # Drag
h0 = 10.0      # Initial height
v0 = 10.0      # Initial velocity
theta = 45.0/180*np.pi  # Initial angle

# Initial condition
q0 = [
    0.0, 0.0, h0,  # x0, y0, z0
    v0*np.cos(theta), 0, v0*np.sin(theta),  # vx0, vy0, vz0
]

def fun(t, q):
    x, y, z, vx, vy, vz = q
    ax = -lam*vx / m
    ay = -lam*vy / m
    az = -lam*vz / m - g
    return [vx, vy, vz, ax, ay, az]

t0 = 0.0
tf = 3.0
res = solve_ivp(fun, t_span=(t0, tf), y0=q0, max_step=0.1)

fig, ax = plt.subplots()

ts = res.t
xs, ys, zs, vxs, vys, vzs = res.y
ax.plot(xs, zs)
ax.set(xlabel='x', ylabel='z', aspect=1);
```

The following issues were encountered:

* Some students were confused about how to write `fun(t, q)`, especially about whether
  or not the initial conditions `q0` should play a role.  I discussed how `fun(t, q)`
  has access to `q` which allows you to forget about `q0` etc. and focus on the current
  time.  (However, there is the issue of `m`, `g`, etc. which maybe should be passed as
  default arguments?)

To try to simplify this, I suggested a simpler problem inspired by a known solution:

$$
  y(t) = e^{-t^2/2}, \qquad \dot{y} = -te^{-t^2/2} = -ty(t), \qquad y(0) = 1.
$$

* This helped some students, but confused others because we switched gears mid-class.
  Here some students became fixated on the solution $e^{-t^2/2}$ and were not sure how
  this should enter their code.  In future, just specify the IVP and *then* solve it later.

Wed 8 Sept 2021
---------------

Today we had the class fork the main repo so they could submit their work.  The steps
were:

1. Create a personal [GitLab] account.
2. Open private [CoCalc] account (in this case, created through the class course.
    Instructors like Matt Duez need to create a private account).
3. Open a terminal on [CoCalc], and generate an ssh key if needed with `ssh-keygen -t ed25519`:

    ```console
    ~$ ls ~/.ssh/              # See if keys exist
    authorized_keys  known_hosts
    $ ssh-keygen -t ed25519   # Generate new key if needed
    Generating public/private ed25519 key pair.
    Enter file in which to save the key (/home/user/.ssh/id_ed25519): 
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /home/user/.ssh/id_ed25519
    Your public key has been saved in /home/user/.ssh/id_ed25519_1.pub
    The key fingerprint is:
    ...
    ~$ ls ~/.ssh/              # Now keys exist
    authorized_keys  id_ed25519  id_ed25519.pub  known_hosts
    ```
4. Start an ssh agent running `bash` and authenticate with `ssh-add`:

    ```console
    ~$ ssh-agent bash
    ~$ ssh-add
    Enter passphrase for /home/user/.ssh/id_ed25519:
    Identity added: /home/user/.ssh/id_ed25519 (user@project-...)
    ```
    
    ````{admonition} Potential failure
    Students may have created a key earlier but forgot their password.  In this case,
    they should delete the keys and regenerate them: 

    ```console
    ~$ ssh-keygen -t ed25519
    Generating public/private ed25519 key pair.
    Enter file in which to save the key (/home/user/.ssh/id_ed25519): 
    /home/user/.ssh/id_ed25519 already exists.
    Overwrite (y/n)? y
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /home/user/.ssh/id_ed25519
    Your public key has been saved in /home/user/.ssh/id_ed25519.pub
    The key fingerprint is:
    ...
    ```
    ````

5. Copy the public key and add it to the student's [GitLab] project (top right
    **Preferences > SSH Keys**).
    
    ```console
    ~$ cat ~/.ssh/id_ed25519.pub 
    ssh-ed25519 AAAA...
    ```

6. Open the [Official Course Repository] on [GitLab] and create a **Fork** (top right)
    in the student's personal namespace with **Private** visibility level.  Have
    students alter the **Project description** so as to differentiate this from the
    [Official Course Repository].
    
7. In this **Fork**, copy the **Clone > Clone with SSH** link
    i.e. `git@gitlab.com:mforbes/physics-581-physics-inspired-computation.git`.

8. Clone the private fork on [CoCalc] after first moving or removing any previously
    cloned repository:
   
    ```console
    ~$ cd ~     # Go to home directory
    ~$ ls       # See if there are any previous clones
    2021-09-08-131459.term  physics-581-physics-inspired-computation
    ~$ mv physics-581-physics-inspired-computation physics-581-physics-inspired-computation_old
    ~$ git clone git@gitlab.com:mforbes/physics-581-physics-inspired-computation.git
    Cloning into 'physics-581-physics-inspired-computation'...
    ...
    ```
    
    ````{admonition} Potential failure
    This needs to be done in the terminal where `ssh-agent bash` and `ssh-add` were run,
    otherwise the clone will fail:
    
    ```console
    ~$ git clone git@gitlab.com:mforbes/physics-581-physics-inspired-computation.git
    Cloning into 'physics-581-physics-inspired-computation'...
    git@gitlab.com: Permission denied (publickey,keyboard-interactive).
    fatal: Could not read from remote repository.

    Please make sure you have the correct access rights
    and the repository exists.
    ```
    
    Perhaps we should add something [like this](https://serverfault.com/a/547929) to
    `~/.bash_aliases`:
    
    ```bash
    ...
    # if we can't find an agent, start one, and restart the script.
    if [ -z "$SSH_AUTH_SOCK" ] ; then
      exec ssh-agent bash -c "ssh-add ; $0"
      exit
    fi
    ...
    
    ```
    
    This would ensure an agent is always running, requiring only `ssh-add`.
    ````
9. After cloning, the private fork should be the remote called `origin`.  Add the
    [Official Course Repository] as a remote called `upstream` with `git remote add upstream git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation.git`:
    
    ```console
    ~$ cd ~/physics-581-physics-inspired-computation
    ~/physics-581-physics-inspired-computation$ git remote -v
    origin  git@gitlab.com:mforbes/physics-581-physics-inspired-computation.git (fetch)
    origin  git@gitlab.com:mforbes/physics-581-physics-inspired-computation.git (push)
    ~/physics-581-physics-inspired-computation$ git remote add upstream git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation.git
    ~/physics-581-physics-inspired-computation$ git remote -v
    origin  git@gitlab.com:mforbes/physics-581-physics-inspired-computation.git (fetch)
    origin  git@gitlab.com:mforbes/physics-581-physics-inspired-computation.git (push)
    upstream        git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation.git (fetch)
    upstream        git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation.git (push)
    ```
    
    Now students can `git pull` and `git push` to interact with their private repo, and
    `git pull upstream main` to get updates from the [Official Course Repository].

10. Pull any changes from the [Official Course Repository], and then run `make init`:

    ```console
    ~/physics-581-physics-inspired-computation$ git pull upstream main
        $ git pull upstream main
    From gitlab.com:wsu-courses/physics-581-physics-inspired-computation
     * branch            main       -> FETCH_HEAD
    Already up to date.
    ~/physics-581-physics-inspired-computation$ make init
    git clone git@gitlab.com:wsu-courses/physics-581-physics-inspired-computation_resources.git _ext/Resources
    Cloning into '_ext/Resources'...
    ...
    ```
    
    ```{admonition} Crash and burn failure
    Many students ran into a major issue where `make init` failed due to an error
    introduced into the laatest setuptools two days ago:
    
    * [[BUG] error in XXXX setup command: use_2to3 is invalid when
        false. #2775](https://github.com/pypa/setuptools/issues/2775)
    
    To fix this for now, we pin the version of `setuptools<58.0.2|>=59` in
    `anaconda-project.yaml`.
    ```
    
    Once this is done, when a new terminal is started, it should be using the
    `phys-581-2021` kernel:
    
    ```console
    (phys-581-2021) ~$
    ```
    
    This kernel should also be available in Jupyter Notebooks in the list of Kernels.

11. (Incomplete) Specify the [Git] username and email so that students can commit by
    specifying the following in their [CoCalc] project **Settings > **Custom environment
    variables** *(The `LC_EDITOR` need not be specified unless students prefer `vi` to
    the default `nano`.)*:
    
    ```json
    {
      "LC_GIT_USERNAME": "Michael McNeil Forbes",
      "LC_GIT_USEREMAIL": "m.forbes@wsu.edu",
      "LC_EDITOR": "vi",
    }
    ```
    
    The project needs to be restarted for these to take effect.  After restarting, [Git]
    should see these:
    
    ```console
    ~$ git 

    ````{admonition} Potential failure
    If this is not done properly, students may get an error like the following:
    
    ```console
    (phys-581-2021) ~/physics-581-physics-inspired-computation$ git commit
    
    *** Please tell me who you are.

    Run

      git config --global user.email "you@example.com"
      git config --global user.name "Your Name"

    to set your account's default identity.
    Omit --global to set the identity only in this repository.

    fatal: empty ident name (for <user@fa57a33d76fc>) not allowed
    ```

    Our current `~/.bash_aliases` file uses `LC_GIT_USERNAME` and `LC_GIT_USERMAIL` to
    set the following:
    
    ```bash
    export GIT_AUTHOR_NAME="${LC_GIT_USERNAME}"
    export GIT_AUTHOR_EMAIL="${LC_GIT_USEREMAIL}"
    export GIT_COMMITTER_NAME="${LC_GIT_USERNAME}"
    export GIT_COMMITTER_EMAIL="${LC_GIT_USEREMAIL}"
    ```
    
    These should only be set if the variables are defined, otherwise, they will have
    empty values cause any customization in `~/.gitconfig` to be ignored.  This will be
    fixed in the next version of `mmf_setup`.
    ````

[CoCalc]: <https://cocalc.com> "CoCalc: Collaborative Calculation and Data Science"
[GitLab]: <https://gitlab.com> "GitLab"
[Official Course Repository]: <https://gitlab.com/wsu-courses/physics-581-physics-inspired-computation/> "Official Physics 581 Repository hosted on GitLab"
[`solve_ivp`]: <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html>

