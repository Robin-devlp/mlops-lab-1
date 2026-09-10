Lab 1 - git/dvc and data preparation - Answers


Question 1: Observe the files created, what do you think they contain.

uv init created these files:

- pyproject.toml: the project configuration. It has the project name, version, description, the required Python version (3.13 or newer) and the list of dependencies, which is empty for now and gets filled when we run uv add.
- .python-version: the Python version used for the project (3.13).
- README.md: the project description, empty for now.
- src/mlops_lab_1/: a small starter package with a main() function that prints "Hello from mlops-lab-1!".

The virtual environment (.venv) and the lock file (uv.lock) are not created yet. They appear the first time we run uv run or uv add. uv.lock should be committed so everyone gets the same package versions, but .venv should not.


Question 2: What are the created files. What do you think they are used for? And which ones should be pushed to git?

dvc init created:

- .dvc/config: the DVC settings of the project, like the remote storage. It is empty at first.
- .dvc/.gitignore: tells git to ignore the DVC files that must stay local (config.local, tmp and cache).
- .dvc/tmp: temporary files that DVC uses internally.
- .dvcignore: like .gitignore, but it lists the files DVC should ignore.

Later DVC also creates .dvc/cache, where the actual data is stored locally, and .dvc/config.local for private settings like passwords.

The files that should be pushed to git are .dvc/config, .dvc/.gitignore and .dvcignore. The tmp folder, the cache and config.local stay on the laptop. The data itself goes to the DVC remote with dvc push, not to git.


Question 3: Where are the credentials stored? and what are the options other than --global? Should the credentials be pushed to github?

With --global, as written in the lab, the credentials are saved in the user's global DVC config file, outside the project (on Windows: %LOCALAPPDATA%\iterative\dvc\config).

The other options are:

- --local: saved in .dvc/config.local, only for this project on this computer. This file is ignored by git.
- --project (the default when no option is given): saved in .dvc/config, which is committed and shared with everyone.
- --system: saved in a system-wide file that applies to all users of the computer.

The credentials should not be pushed to GitHub. The repository is public, so anyone could use the token to access or delete the data on DagsHub. And once something is committed, it stays in the git history even if the file is deleted later.

In my case I added the remote URL at the project level, so it is saved in .dvc/config and pushed to GitHub, and I put the username and token with --local so they stay in .dvc/config.local. This way someone who clones the repo knows where the data is, but the password stays private.


Question 4: Take a look at the .gitignore file. Explain what happened.

Before dvc add there was no .gitignore in the repository. dvc add created one containing the line /data, which tells git to ignore the whole data folder. This way the images are never added to git. Instead, DVC tracks the folder: it computed a hash for each of the 16643 files and saved a copy of them in .dvc/cache. After this, git status no longer shows the data folder, only two new small files to commit: .gitignore and data.dvc.


Question 5: Do you see a .dvc file? What does it contain?

Yes, dvc add created data.dvc. It is a small text file that points to the data:

    outs:
    - md5: a3a457d03c51ff8b037a833440f6ad13.dir
      size: 1188442712
      nfiles: 16643
      hash: md5
      path: data

It contains the md5 hash of the data folder, the total size in bytes (about 1.19 GB), the number of files (16643), the hash algorithm used and the path of the tracked folder. The .dir at the end means the hash is of the folder's file list, where each file has its own hash. Git versions this small file instead of the data, and DVC uses the hash to find the right version of the data in the cache or on the remote.
