import click

from .parse import ParseError, parse


def print_tree(nodes: list, directory_only: bool = False, prefix: str = ""):
    for index, node in enumerate(nodes):
        is_last = index == len(nodes) - 1
        connector = "└── " if is_last else "├── "

        name = node["directive"]
        children = node.get("block")
        if children:
            click.echo(f"{prefix}{connector}", nl=False)
            click.echo(click.style(name, fg="cyan"), color=True, nl=False)
            if name == "location":
                click.echo(" " + " ".join(node["args"]), nl=False)
            click.echo("")
            print_tree(
                nodes=children,
                directory_only=directory_only,
                prefix=prefix + ("    " if is_last else "│   "),
            )
        elif not directory_only:
            click.echo(f"{prefix}{connector}", nl=False)
            click.echo(name)


@click.command()
@click.pass_context
@click.argument("file")
@click.option(
    "-d", "--directory", is_flag=True, help="List only those directives with children"
)
def tree(ctx: click.Context, file, directory):
    try:
        parsed_list = parse(file)
    except ParseError as error:
        ctx.exit(error)

    for parsed in parsed_list:
        print_tree(parsed, directory_only=directory)
