# Gitlab dumper

A simple CLI tool for creating a dump of all projects in your Gitlab instance.
  
Supports dump as raw repo and archives.

## Preflight

Go to `https://<YOUR_GITLAB_ENDPOINT>/-/profile/personal_access_tokens` and create personal token with permissions:
- api
- read_api
- read_repository

If you want to see all repositories, it may make sense to grant administrator permissions for the access token.

### Configuration

Create `.env` file and put credentials:
```bash

LOG_LEVEL="info"
GITLAB_URL="https://<YOUR_GITLAB_ENDPOINT>"
GITLAB_PERSONAL_TOKEN="xxxxxx"  # also, GITLAB_OAUTH_TOKEN supports
```

Or set environment variables directly:
```bash
export LOG_LEVEL="info"
export GITLAB_URL="https://<YOUR_GITLAB_ENDPOINT>"
export GITLAB_PERSONAL_TOKEN="xxxxxx"
```

**Requirements:**
- Python >= 3.10
- The git command line tool must be installed on your PC
- The utility clones over SSH, so make sure that your public key is added to the GitLab profile, **[read the doc](https://docs.gitlab.com/ee/user/ssh.html)**


### Install

Using pip:
```shell
python3 -m venv venv
source venv/bin/activate
pip install gitlab-dumper

gitlab-dumper --help
```


Installing from source:
```shell
git clone https://github.com/akimrx/gitlab-dumper  --recursive
cd gitlab-dumper
python3 -m venv venv
source venv/bin/activate
make install  # or: python3 setup.py install

gitlab-dumper --help
```


## Usage

```
Commands:
  groups    Operations with Gitlab groups.
  projects  Operations with Gitlab projects.
  tree      Show groups, subgroups and projects as tree.

Groups commands:
  list      Show available Gitlab groups.
  projects  List projects in group or subgroup.

Projects commands:
  dump  Download, clone or re-pull all available projects.
  list  Show available Gitlab projects.
```

#### Dump

Before really dump use `--dry-run` flag, for example:
```shell
gitlab-dumper projects dump --namespaces foo,bar --no-personal --dry-run
```
  
For full dump just use `gitlab-dumper projects dump`


Available optional flags: 
```
  --dumps-dir TEXT   Directory for dumps (default: ./dumps).
  --delay INTEGER    Delay between clones in seconds (default 0).
  --skip-empty       Ignore empty projects.
  --no-personal      Ignore personal user projects.
  --as-archive       Download projects as tar.gz archive instead clone.
  --dry-run          Safe simulate dump without download/clone.
  --namespaces TEXT  Comma-separated namespaces to operate.
  --exclude TEXT     Comma-separated projects (slug) to exclude.
  --help             Show this message and exit.
```

### Development run

```shell
python3 -m 'src.main' --help
```
