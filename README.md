## TL;DR

Go to `https://<YOUR_GITLAB_ENDPOINT>/-/profile/personal_access_tokens` and create personal token with permissions:
- api
- read_api
- read_repository

Create `.env` file and put credentials:
```bash

GITLAB_URL="https://<YOUR_GITLAB_ENDPOINT>"
GITLAB_PERSONAL_TOKEN="xxxxxx"
```

Or set environment variables directly:
```bash
export GITLAB_URL="https://<YOUR_GITLAB_ENDPOINT>"
export GITLAB_PERSONAL_TOKEN="xxxxxx"
```

**Preflight:**
- The git command line tool must be installed on your PC
- The utility clones over SSH, so make sure that your public key is added to the GitLab profile, [read the doc](https://docs.gitlab.com/ee/user/ssh.html)


### Run CLI

#### Install

```shell
make install

gitlab-dumper --help
gitlab-dumper projects --help
```

#### Usage

```
Commands:
  groups    Operations with Gitlab groups.
  projects  Operations with Gitlab projects.
  tree      Show groups, subgroups and projects as tree.

Groups commands:
  list      Show available Gitlab groups.
  projects  List projects in group or subgroup.

Projects commands:
  dump  Clone or re-pull all available projects.
  list  Show available Gitlab projects
```

#### Dump

Just run `gitlab-dumper projects dump`
```
Options:
  --dumps-dir TEXT   Directory for dumps (default: ./dumps).
  --delay INTEGER    Delay between clones in seconds (default 0).
  --skip-empty       Ignore empty projects.
  --no-personal      Ignore personal user projects.
  --as-archive       Download projects as tar.gz archive instead clone.
  --namespaces TEXT  Comma-separated namespaces to operate.
  --exclude TEXT     Comma-separated projects (slug) to exclude.
  --help             Show this message and exit.
```


### Development run

```shell
python3 -m 'src.main' --help
```
