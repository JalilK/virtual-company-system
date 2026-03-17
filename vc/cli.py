import click
import inspect
from pathlib import Path

from vc.project_init import init_company
import vc.role_ops as role_ops


def _resolve_optional(*names):
    for name in names:
        fn = getattr(role_ops, name, None)
        if callable(fn):
            return fn
    return None


create_role_from_spec = _resolve_optional("create_role_from_spec")
inspect_role_fn = _resolve_optional("inspect_role")
validate_company_fn = _resolve_optional("validate_company")
expand_fn = _resolve_optional("expand_from_founder_init")
refresh_fn = _resolve_optional("refresh_org_files")


def _call_init(company_name):
    sig = inspect.signature(init_company)
    if len(sig.parameters) == 1:
        return init_company(company_name)
    if len(sig.parameters) == 2:
        return init_company(Path.cwd(), company_name)
    raise click.ClickException(f"Unsupported init_company signature {sig}")


def print_file(path: Path):
    if not path.exists():
        raise click.ClickException(f"Missing file {path}")
    click.echo("\n" + "=" * 60)
    click.echo(str(path))
    click.echo("=" * 60 + "\n")
    click.echo(path.read_text())
    click.echo("\n" + "=" * 60 + "\n")


@click.group()
def cli():
    pass


@cli.command("init")
@click.argument("company_name")
def init_cmd(company_name):
    _call_init(company_name)


@cli.command("create-role")
@click.argument("request_file")
def create_role_cmd(request_file):
    if create_role_from_spec is None:
        raise click.ClickException("create_role_from_spec not available")
    create_role_from_spec(Path.cwd(), Path(request_file))


@cli.command("inspect")
@click.argument("company_name")
@click.argument("role_id")
def inspect_cmd(company_name, role_id):
    if inspect_role_fn is None:
        raise click.ClickException("inspect_role not available")
    company_root = Path.cwd() / company_name
    click.echo(inspect_role_fn(company_root, role_id))


@cli.command("run")
@click.argument("company_name")
@click.argument("role")
def run_cmd(company_name, role):
    company_root = Path.cwd() / company_name

    if role != "founder":
        raise click.ClickException(f"Unknown role {role}")

    prompt_path = company_root / "roles" / "founder" / "FOUNDER_INIT_PROMPT.txt"
    plan_path = company_root / "inputs" / "FOUNDER_EXPANSION_CONFIRMATION.yaml"

    print_file(prompt_path)
    click.echo("NEXT STEP")
    click.echo(f"Fill this file\n{plan_path}\n")


@cli.command("founder-confirm")
@click.argument("company_name")
def founder_confirm_cmd(company_name):
    if expand_fn is None:
        raise click.ClickException("expand_from_founder_init not available in this repo build")

    company_root = Path.cwd() / company_name
    plan_path = company_root / "inputs" / "FOUNDER_EXPANSION_CONFIRMATION.yaml"

    if not plan_path.exists():
        raise click.ClickException(f"Missing founder plan file\n{plan_path}")

    click.echo("Running founder expansion")
    expand_fn(company_root, plan_path)

    if refresh_fn is not None:
        refresh_fn(company_root)

    click.echo("Expansion complete")


@cli.command("validate")
@click.argument("company_name")
def validate_cmd(company_name):
    if validate_company_fn is None:
        raise click.ClickException("validate_company not available")
    company_root = Path.cwd() / company_name
    ok, errors = validate_company_fn(company_root)
    if not ok:
        for error in errors:
            click.echo(error)
        raise SystemExit(1)
    click.echo("validation passed")


if __name__ == "__main__":
    cli()
