import click

from src._settings import get_settings, get_logger
from src._gitlab import get_gitlab_client, Group, GroupSubgroup

logger = get_logger()
gitlab = get_gitlab_client(get_settings())


@click.command("tree")
def tree() -> None:
    """Show groups, subgroups and projects as tree."""

    from treelib import Tree

    tree = Tree()
    root_id = "root"
    projects_counter = 0
    tree.create_node(tag="Gitlab", identifier=root_id)

    def deep_search_projects_in_subgroup(subgroup: GroupSubgroup, parent: Group) -> None:
        nonlocal projects_counter
        tree.create_node(tag=subgroup.path, identifier=f"G:{subgroup.id}", parent=f"G:{parent.id}")
        subgroup_as_group: Group = subgroup.manager.gitlab.groups.get(subgroup.id)

        for project in subgroup_as_group.projects.list(all=True, iterator=True):
            projects_counter += 1
            tree.create_node(tag=project.path, identifier=f"P:{project.id}", parent=f"G:{subgroup.id}")

        for nested_subgroup in subgroup_as_group.subgroups.list(all=True, iterator=True):
            deep_search_projects_in_subgroup(subgroup=nested_subgroup, parent=subgroup)

    for group in gitlab.fetch_available_groups(only_parent_groups=True):
        tree.create_node(tag=group.path, identifier=f"G:{group.id}", parent=root_id)

        for project in group.projects.list(all=True, iterator=True):
            if project.namespace.get("id", 0) == group.id:  # ignore projects in subgroups
                projects_counter += 1
                tree.create_node(tag=project.path, identifier=f"P:{project.id}", parent=f"G:{group.id}")

        for subgroup in group.subgroups.list(all=True, iterator=True):
            deep_search_projects_in_subgroup(subgroup=subgroup, parent=group)

    click.echo(tree)
    click.echo("")
    click.secho(f"Total projects found: {projects_counter}", fg="cyan")
