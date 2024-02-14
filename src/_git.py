import os

from src._settings import get_logger

from git import Repo as GitRepository
from git.exc import GitCommandError

from gitlab.v4.objects import Project

logger = get_logger()


def clone_or_update_repo(project: Project, dumps_base_dir: str) -> None:
    """Clone repo from remote origin or pull fresh changes if exists."""
    project_slug = project.path_with_namespace
    destination_path = os.path.join(dumps_base_dir, *project_slug.split("/"))

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
