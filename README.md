## TL;DR

Go to `https://<your_gitlab_domain>/-/profile/personal_access_tokens` and create personal token with permissions:
- api
- read_api
- read_repository

Create `.env` file and put credentials:
```shell

GITLAB_URL=https://<your_gitlab_domain>
GITLAB_PRIVATE_TOKEN=xxxxxx
```

**Preflight:**
- The git command line tool must be installed on your PC
- The utility clones over SSH, so make sure that your public key is added to the GitLab profile, [read the doc](https://docs.gitlab.com/ee/user/ssh.html)


### Run CLI

Install:

```shell
make install

gitlab-dumper --help
gitlab-dumper projects --help
```

Usage:

```shell

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

```shell
Options:
  --dumps-dir TEXT  Directory for dumps (default: ./dumps).
  --delay INTEGER   Delay between clones in seconds (default 0).
  --skip-empty      Ignore empty projects.
  --exclude TEXT    Comma-separated projects (slug) to exclude.
  --help            Show this message and exit.
```


### Development run

```shell
python3 -m 'src.main' --help
```
