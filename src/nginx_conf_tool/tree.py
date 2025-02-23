import click

from .parse import ParseError, parse


def _print_directive(name, prefix, is_last, is_context: bool = False):
    connector = "└── " if is_last else "├── "
    click.echo(f"{prefix}{connector}", nl=False)
    if is_context:
        click.echo(click.style(name, fg="cyan"), color=True)
    else:
        click.echo(name)


def print_tree(
    nodes: list, directory_only: bool = False, level: int = -1, prefix: str = ""
):
    if level == 0:
        return

    for index, node in enumerate(nodes):
        is_last = index == len(nodes) - 1

        name = node["directive"]
        children = node.get("block")
        if children:
            _print_directive(name, prefix, is_last, is_context=True)
            print_tree(
                nodes=children,
                directory_only=directory_only,
                level=-1 if level == -1 else level - 1,
                prefix=prefix + ("    " if is_last else "│   "),
            )
        elif not directory_only:
            _print_directive(name, prefix, is_last)


@click.command()
@click.pass_context
@click.argument("file")
@click.option(
    "-d",
    "--directory",
    is_flag=True,
    help="List only those directives with children (AKA) context",
)
@click.option(
    "-L", "--level", type=int, default=-1, metavar="N", help="Limit to N levels deep"
)
def tree(ctx: click.Context, file, directory, level):
    try:
        parsed_list = parse(file)
    except ParseError as error:
        ctx.exit(error)

    for parsed in parsed_list:
        print_tree(parsed, directory_only=directory, level=level)
        click.echo()
