from src._settings import Settings, get_logger
from functools import cached_property
from typing import Iterator

from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupSubgroup, Project

logger = get_logger()


class GitlabClientWrapper:
    """A simple wrapper with additional methods over the Gitlab client."""

    def __init__(
        self,
        endpoint: str,
        oauth_token: str | None = None,
        personal_token: str | None = None,
    ) -> None:
        self.endpoint = endpoint
        self.oauth_token = oauth_token
        self.personal_token = personal_token

    @cached_property
    def client(self) -> Gitlab:
        """Returns Gitlab client object."""
        auth = self._validate()
        return Gitlab(url=self.endpoint, retry_transient_errors=True, **auth)

    def _validate(self) -> dict[str, str]:
        """Validate Gitlab authentification."""
        if self.endpoint is None:
            raise RuntimeError("Gitlab endpoint url is empty")
        if not any((self.personal_token, self.oauth_token)):
            raise RuntimeError("Gitlab OAuth or Private token required")
        if all((self.personal_token, self.oauth_token)):
            raise RuntimeError("Only one of Gitlab token can be used")

        if self.personal_token:
            auth = {"private_token": self.personal_token}
        elif self.oauth_token:
            auth = {"oauth_token": self.oauth_token}
        return auth

    def fetch_available_groups(
        self, only_parent_groups: bool = False, exclude: list[str] | None = None
    ) -> Iterator[Group]:
        """Find available groups and returns iterator of Group objects."""
        logger.info(f"Starting search groups with params: {only_parent_groups=} {exclude=}")
        groups: Iterator[Group] = self.client.groups.list(all=True, iterator=True)

        if exclude is None and not only_parent_groups:
            return groups

        if only_parent_groups:
            groups = filter(lambda group: not group.parent_id, groups)

        if exclude is not None:
            return filter(lambda group: group.path not in exclude, groups)

        return groups

    def fetch_available_projects(
        self,
        exclude: list[str] | None = None,
        namespaces: list[str] | None = None,
        statistics: bool = False,
        no_personal: bool = False,
    ) -> Iterator[Project]:
        """Find available projects and returns iterator of Project objects."""
        logger.info(f"Starting search projects with params: {namespaces=} {exclude=} {no_personal=}")
        projects = self.client.projects.list(all=True, iterator=True, statistics=statistics)

        if no_personal:
            projects = filter(lambda project: project.namespace.get("kind") != "user", projects)

        if namespaces is not None:
            projects = filter(lambda project: project.namespace.get("path") in namespaces, projects)

        if exclude is not None:
            projects = filter(lambda project: project.path not in exclude, projects)

        return projects


def get_gitlab_client(settings: Settings) -> GitlabClientWrapper:
    return GitlabClientWrapper(
        endpoint=settings.GITLAB_URL,
        oauth_token=settings.GITLAB_OAUTH_TOKEN,
        personal_token=settings.GITLAB_PERSONAL_TOKEN,
    )


__all__ = ["get_gitlab_client", "GitlabClientWrapper"]
