import click
import crossplane


def print_tree(nodes: list, prefix: str = ""):
    for index, node in enumerate(nodes):
        is_last = index == len(nodes) - 1
        connector = "└── " if is_last else "├── "
        click.echo(f"{prefix}{connector}", nl=False)

        name = node["directive"]
        children = node.get("block")
        if children:
            click.echo(click.style(name, fg="cyan"), color=True, nl=False)
            if name == "location":
                click.echo(" " + " ".join(node["args"]), nl=False)
            click.echo("")
            print_tree(
                nodes=children,
                prefix=prefix + ("    " if is_last else "│   "),
            )
        else:
            click.echo(name)


@click.command()
@click.pass_context
@click.argument("file")
def tree(ctx, file):
    root = crossplane.parse(file)
    assert root["errors"] == []
    config = root["config"][0]
    assert config["errors"] == []
    parsed = config["parsed"]
    print_tree(parsed)
