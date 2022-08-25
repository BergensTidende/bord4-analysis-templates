# Bord4 Data Analysis Templates

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#structure">Structure</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Rewriting code is tedious, meaningless and boring. To counter act this horror we collect our best code snippets in this repo to be used in other projects. Projects created with the bord4 analysis cookiecutter can pull directly from this repo.

Theese templates are used by the [cookiecutter-bord4-analysis](https://github.com/BergensTidende/cookiecutter-bord4-analysis) project.
### Requirements

---

- pyenv - manage python versions
- pipenv - manage python dependencies

To install on mac you can use homebrew:

```bash
brew upgrade
brew install pyenv
brew install pipenv
```

### Makefile commands

- `make lint`
  - lint the code in the src folder
- `make lab`
  - run jupyter lab
- `make new`
  - creates a new template notebook by copying generic header

### Structure

```
.
├── README.md
├── data
│   ├── processed
│   ├── public
│   ├── source
│   └── untracked
├── etl
├── src
└── templates
```

- `README.md`
  - This file.
- `data`
  - This is the directory used for storing and saving data, mirrored from the cookiecutter-bord4-analysis structure
  - `data/processed`
    - Contains data that has either been transformed from an `etl` script or output from an `analysis` jupyter notebook.
    - Data that has been transformed from an `etl` script will follow a naming convention: `etl_{file_name}.[csv,json...]`
  - `data/public`
    - Public-facing data files go here - data files which are 'live'.
  - `data/source``
    - Raw untouched data. Data in this folder should never be altered
  - `data/untracked`
    - Files that are either to large or to sensitive to be on github goes here.
- etl
  - symlinked to templates. In a real world project notebooks in other directories will fetch from scripts in etl. 
- src
  - Python files used as utils that can be imported from notebooks and script.
  - `src/dataframe`
    - util functions for working with dataframes
  - `src/integration`
    - helper functions when working with Schibsted MM API
  - `src/log`
    - better log functions
  - `src/scripts`
    - for scripts used by the make file
  - `src/utils`
    - much needed utils functions. Like code for uploading to S3.
  - `src/extra`
    - add folders under here for less used functionality that don't need to come with every project
    - install with make command
    - `src/visvegen`
      - Functions to work with Vegvesenet's VisVegen API

## Usage

To play around with the templates and code in src you must first install the virtual enviroment.

```bash
pipenv install
```

And the run jupyter lab

```bash
pipenv run jupyter lab
```

## Contributing

Do you have write permissions to the repo? Then you can clone this project to a folder on your computer.

```bash
git clone this.template-repo
```

If not do the following:

- Create a personal fork of the project on Github.
- Clone the fork on your local machine. Your remote repo on Github is called `origin`.
- Add the original repository as a remote called `upstream`.
- If you created your fork a while ago be sure to pull upstream changes into your local repository.

This will clone the repo into `bord4-analysis-templates`. 

Create a branch for your changes

```bash
git checkout -b name-of-branch
```

Make your changes, rememeber to commit. And always write your commit messages in the present tense. Your commit message should describe what the commit, when applied, does to the code – not what you did to the code.

If you're working on a clone push the branch to github and make PR.

If your're working a fork:

- Squash your commits into a single commit with git's [interactive rebase](https://help.github.com/articles/interactive-rebase). Create a new branch if necessary.
- Push your branch to your fork on Github, the remote `origin`.
- From your fork open a pull request in the correct branch. Target the project's `develop` branch if there is one, else go for `master`!
- …
- If the maintainer requests further changes just push them to your branch. The PR will be updated automatically.
- Once the pull request is approved and merged you can pull the changes from `upstream` to your local repo and delete
  your extra branch(es).

 <!-- CONTACT -->

## Contact

Bord4 - bord4@bt.no
