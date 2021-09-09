Class Log
=========

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
