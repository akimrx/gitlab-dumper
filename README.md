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

### Run CLI

Install:

```shell
make install

gitlab-dumper --help
```

Debug running:

```shell
python3 -m 'src.main' --help
```
