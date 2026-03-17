from __future__ import annotations

from pathlib import Path

import click

from vc.project_init import DEFAULT_C_SUITE, init_company
from vc.role_ops import create_role_from_spec, inspect_role
from vc.validators.runner import validate_company


@click.group()
def cli() -> None:
    pass


@cli.command("init")
@click.argument("company")
def init_command(company: str) -> None:
    company_name = company.replace("-", "_")
    company_root = init_company(Path.cwd(), company_name)
    click.echo(f"initialized {company_root}")
    click.echo("created founder and c_suite only")
    click.echo("review roles/founder/FOUNDER_INIT_PROMPT.txt before expanding the organization")


@cli.command("validate")
@click.argument("company")
def validate_command(company: str) -> None:
    ok, messages = validate_company(Path(company))
    if not ok:
        for message in messages:
            click.echo(message)
        raise SystemExit(1)
    click.echo("validation passed")


@cli.command("create-role")
@click.argument("company")
@click.option("--spec", "spec_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
def create_role_command(company: str, spec_path: Path) -> None:
    create_role_from_spec(Path(company), spec_path)
    click.echo("role created")


@cli.command("generate-chain")
@click.argument("company")
@click.argument("role_family")
def generate_chain_command(company: str, role_family: str) -> None:
    click.echo(f"generate-chain placeholder for {role_family} in {company}")


@cli.command("run")
@click.argument("company")
@click.argument("role")
def run_command(company: str, role: str) -> None:
    click.echo(f"run placeholder for role {role} in {company}")


@cli.command("inspect")
@click.argument("company")
@click.argument("role")
def inspect_command(company: str, role: str) -> None:
    click.echo(inspect_role(Path(company), role))


if __name__ == "__main__":
    cli()
