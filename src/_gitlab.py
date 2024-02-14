from src._settings import Settings
from functools import cached_property
from typing import Iterator

from gitlab import Gitlab
from gitlab.v4.objects import Group, Project, GroupSubgroup


class GitlabClientWrapper:
    """A simple wrapper with additional methods over the Gitlab client."""

    def __init__(
        self,
        endpoint: str,
        oauth_token: str | None = None,
        private_token: str | None = None,
    ) -> None:
        self.endpoint = endpoint
        self.oauth_token = oauth_token
        self.private_token = private_token

    @cached_property
    def client(self) -> Gitlab:
        """Returns Gitlab client object."""
        auth = self._validate()
        return Gitlab(url=self.endpoint, retry_transient_errors=True, **auth)

    def _validate(self) -> dict[str, str]:
        """Validate Gitlab authentification."""
        if self.endpoint is None:
            raise RuntimeError("Gitlab endpoint url is empty")
        if not any((self.private_token, self.oauth_token)):
            raise RuntimeError("Gitlab OAuth or Private token required")
        if all((self.private_token, self.oauth_token)):
            raise RuntimeError("Only one of Gitlab token can be used")

        if self.private_token:
            auth = {"private_token": self.private_token}
        elif self.oauth_token:
            auth = {"oauth_token": self.oauth_token}
        return auth

    def fetch_available_groups(
        self, only_parent_groups: bool = False, exclude: list[str] | None = None
    ) -> Iterator[Group]:
        """Find available groups and returns iterator of Group objects."""
        groups: Iterator[Group] = self.client.groups.list(all=True, iterator=True)

        if exclude is None and not only_parent_groups:
            return groups

        if only_parent_groups:
            groups = filter(lambda group: not group.parent_id, groups)

        if exclude is not None:
            return filter(lambda group: group.path not in exclude, groups)

        return groups

    def fetch_available_projects(
        self, exclude: list[str] | None = None, statistics: bool = False
    ) -> Iterator[Project]:
        """Find available projects and returns iterator of Project objects."""
        projects = self.client.projects.list(all=True, iterator=True, statistics=statistics)

        if exclude is None:
            return projects

        return filter(lambda project: project.path not in exclude, projects)


def get_gitlab_client(settings: Settings) -> GitlabClientWrapper:
    return GitlabClientWrapper(
        endpoint=settings.GITLAB_URL,
        oauth_token=settings.GITLAB_OAUTH_TOKEN,
        private_token=settings.GITLAB_PRIVATE_TOKEN,
    )


__all__ = ["get_gitlab_client", "GitlabClientWrapper"]
