import os
from typing import Literal

from src._settings import get_logger
from src._utils import safe_resolve_path

from git import Repo as GitRepository
from git.exc import GitCommandError

from gitlab.v4.objects import Project

logger = get_logger()


def clone_or_update_repo(project: Project, dumps_base_dir: str, dry_run: bool = False) -> None:
    """Clone repo from remote origin or pull fresh changes if exists."""
    project_slug = project.path_with_namespace
    destination_path = os.path.join(safe_resolve_path(dumps_base_dir), *project_slug.split("/"))

    if dry_run:
        logger.info(f"Simulate clonning {project_slug} to {destination_path}")
        return

    try:
        logger.info(f"Clonning {project.path_with_namespace}...")
        GitRepository.clone_from(project.ssh_url_to_repo, to_path=destination_path)
        logger.info(f"Project {project_slug} successfully cloned")
    except GitCommandError:
        logger.warning("Repo already cloned, trying to pulling changes...")
        existed_repo = GitRepository(destination_path)

        if existed_repo.is_dirty():
            logger.error(f"Can't pull repo {project_slug}, cause we have unsaved changes. Please resolve it manually")
            return

        try:
            existed_repo.remotes.origin.pull()
            logger.info(f"Successfully pulled {project_slug} from remote origin")
        except (GitCommandError, ValueError):
            logger.error(f"Possible empty repo or head, skipping pull for {project_slug}")


def save_repo_as_archive(
    project: Project,
    dumps_base_dir: str,
    dry_run: bool = False,
    archive_format: Literal["zip", "tar", "tar.gz"] = "tar.gz",
) -> None:
    """Download archived repo."""
    project_slug = project.path_with_namespace
    if project.empty_repo:
        logger.warning(f"Project {project_slug} is empty and can't be download")
        return

    breadcrumbs = project_slug.split("/")
    destination_path = os.path.join(safe_resolve_path(dumps_base_dir), *breadcrumbs[:1])
    archive_name = os.path.join(destination_path, f"{breadcrumbs[-1]}.{archive_format}")

    if dry_run:
        logger.info(f"Simulate downloading {archive_name} to {destination_path}")
        return

    os.makedirs(destination_path, exist_ok=True)
    with open(archive_name, "wb") as archive:
        logger.info(f"Downloading {project_slug} to {destination_path}")
        archive.write(project.repository_archive(format=archive_format))
        logger.info(f"Project {project_slug} successfully saved as {archive_name}")


__all__ = ["clone_or_update_repo", "save_repo_as_archive"]
