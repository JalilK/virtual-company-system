import click
from pathlib import Path

from vc.project_init import init_company
from vc.role_ops import (
    create_role_from_spec,
    expand_from_founder_init,
    inspect_role,
    validate_company,
)


@click.group()
def cli():
    pass


@cli.command("init-company")
@click.argument("company_name")
def init_company_cmd(company_name):
    init_company(company_name)


@cli.command("create-role")
@click.argument("request_file")
def create_role_cmd(request_file):
    create_role_from_spec(Path.cwd(), Path(request_file))


@cli.command("expand")
@click.argument("company_name")
@click.option(
    "--from-founder-init",
    "from_founder_init",
    is_flag=True,
    default=False,
    help="Expand company from founder initialization confirmation file.",
)
@click.option(
    "--plan-file",
    default=None,
    help="Optional explicit path to founder expansion plan file.",
)
def expand_cmd(company_name, from_founder_init, plan_file):
    company_root = Path.cwd() / company_name
    if plan_file:
        plan_path = Path(plan_file)
    else:
        plan_path = company_root / "inputs" / "FOUNDER_EXPANSION_CONFIRMATION.yaml"

    if from_founder_init:
        expand_from_founder_init(company_root, plan_path)
    else:
        raise click.ClickException("Only --from-founder-init is currently supported.")


@cli.command("inspect")
@click.argument("company_name")
@click.argument("role_id")
def inspect_cmd(company_name, role_id):
    company_root = Path.cwd() / company_name
    result = inspect_role(company_root, role_id)
    click.echo(result)


@cli.command("validate")
@click.argument("company_name")
def validate_cmd(company_name):
    company_root = Path.cwd() / company_name
    ok, errors = validate_company(company_root)
    if not ok:
        for error in errors:
            click.echo(error)
        raise SystemExit(1)
    click.echo("validation passed")


if __name__ == "__main__":
    cli()
