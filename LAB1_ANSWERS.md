# Lab 1 – git/dvc and data preparation: Answers

## Project Setup: `uv init`

> **Question 1:** Observe the files created, what do you think they contain.

`uv init` created four files:

| File | Contents |
|---|---|
| `pyproject.toml` | The project's configuration: name (`mlops-lab-1`), version, description, readme, authors (taken from the git config), the minimum Python version (`requires-python = ">=3.13"`), the list of dependencies (empty for now; `uv add <package>` appends to it), a `[project.scripts]` entry that exposes `main()` as an `mlops-lab-1` command, and a `[build-system]` section telling uv how to build the project as an installable package (`uv_build`). |
| `.python-version` | The Python version uv uses for this project (`3.13`). |
| `README.md` | The project description shown on the repository page (empty for now). |
| `src/mlops_lab_1/__init__.py` | A starter Python package with a `main()` function that prints `Hello from mlops-lab-1!`. |

Two more files appear the first time `uv run`, `uv add` or `uv sync` is used:
- `.venv/`: the project's virtual environment, with the dependencies installed. It is local to the machine and is not committed.
- `uv.lock`: the exact resolved version of every dependency, so the same environment can be recreated anywhere. It should be committed.

No `.gitignore` was created. uv only creates one when it also initializes the git repository, and here the repository already existed because it was cloned from GitHub.

## Setup dvc: `dvc init`

> **Question 2:** What are the created files. What do you think they are used for? And which ones should be pushed to git?

| File | Purpose | Pushed to git? |
|---|---|---|
| `.dvcignore` | Like `.gitignore`, but for DVC: patterns of files DVC should skip when scanning the workspace. It only contains comments for now. | Yes |
| `.dvc/config` | The project's DVC configuration, shared with everyone who clones the repo (remotes, default remote, ...). It is empty right after `dvc init`. | Yes |
| `.dvc/.gitignore` | Tells git to ignore DVC's local-only files: `/config.local`, `/tmp` and `/cache`. | Yes |
| `.dvc/tmp/` | Temporary internal files (locks, indexes, state). | No, ignored |

Two more locations inside `.dvc/` are created later, and git ignores them too:
- `.dvc/cache/` holds the actual data files after `dvc add`. The data is sent to the DVC remote with `dvc push`, never to git.
- `.dvc/config.local` holds settings that only apply to this machine, such as credentials.

**Pushed to git:** `.dvc/config`, `.dvc/.gitignore` and `.dvcignore`. `dvc init` staged exactly these three files by itself. They are also exactly what `git add .dvc .dvcignore` adds, because git respects `.dvc/.gitignore`.

## Add DagsHub as the remote for dvc

> **Question 3:** Where are the credentials stored? and what are the options other than --global? Should the credentials be pushed to github?

Commands used:

```bash
dvc remote add origin https://dagshub.com/Robin-devlp/mlops-lab-1.dvc   # project level -> .dvc/config
dvc remote modify origin --local auth basic                              # -> .dvc/config.local
dvc remote modify origin --local user Robin-devlp
dvc remote modify origin --local password <token>
dvc remote default origin
```

**Where are the credentials stored?** With `--global`, as in the lab instructions, they are written to the user-wide DVC config, which is outside the repository: `%LOCALAPPDATA%\iterative\dvc\config` on Windows. I stored them with `--local` instead, so they are in `.dvc/config.local` inside the repository. That file is listed in `.dvc/.gitignore`, so git never tracks it.

**Options other than `--global`:** DVC reads its configuration from four levels. When two levels set the same option, the more specific one wins, in the order `--local` > project > `--global` > `--system`.

| Flag | File | Scope | Tracked by git? |
|---|---|---|---|
| `--local` | `.dvc/config.local` | This repository, on this machine only | No, gitignored |
| *(none)* / `--project` | `.dvc/config` | This repository, for everyone who clones it | Yes |
| `--global` | `%LOCALAPPDATA%\iterative\dvc\config` | Every DVC repository of the current user | No, outside the repo |
| `--system` | `%PROGRAMDATA%\iterative\dvc\config` | Every user on the machine | No, outside the repo |

**Should the credentials be pushed to GitHub?** No. The repository is public, and a DagsHub token gives full access to the account, so anyone could use it to read, overwrite or delete the data. Even in a private repository, git keeps every past commit, so a secret that was committed once stays in the history after the file is deleted. Only the non-secret part, the remote URL and the default remote, goes into the committed `.dvc/config`.

**Why I did not use `--global` for the remote URL:** if the URL is added with `--global`, it goes to the user-wide file, and the committed `.dvc/config` only contains `remote = origin`, without any URL. It still works on this laptop, but a fresh clone on another machine, for example a teammate's laptop or a CI/CD pipeline, would not know where the data is. Adding the URL at the project level puts it in `.dvc/config`, which is committed, and keeping the credentials in `.dvc/config.local` keeps them private.
