import asyncio

import click
from dishka import make_async_container

from backend.src.core.dependencies import MyProvider
from backend.src.core.exceptions import ValidationError
from backend.src.core.validators import EmailValidator, PasswordValidator
from backend.src.presentation.dto import RegisterRequest
from backend.src.services import AuthService


async def _create_admin_async(email: str, password: str, name: str) -> None:
    click.echo(f"Creating admin with email: {email}")
    try:
        container = make_async_container(MyProvider())
        async with container() as request_container:
            auth_service = await request_container.get(AuthService)
            data = RegisterRequest(name=name, password=password, email=email)
            user = await auth_service.register(data=data, is_admin=True)

            click.secho("✓ Admin created successfully!", fg="green")
            click.echo(f"ID: {user.id}")
            click.echo(f"Email: {user.email}")
            click.echo(f"Name: {user.name}")
    except Exception as e:
        click.secho(f"Error - {e}", fg="red")


@click.command()
@click.option("-n", "--name", prompt="Name", help="Name of admin")
@click.option("-e", "--email", prompt="Email", help="Email adress")
@click.option(
    "-p",
    "--password",
    prompt="Password",
    help="Admin passwort",
    confirmation_prompt=True,
    hide_input=True,
)
def create_admin(name: str, email: str, password: str) -> None:
    """Create admin user - sync wrapper"""
    try:
        EmailValidator.validate(email)
        PasswordValidator.validate(password)
    except ValidationError as e:
        click.secho(f"Error - {e.message}", fg="red")
        return

    asyncio.run(_create_admin_async(name=name, email=email, password=password))


if __name__ == "__main__":
    create_admin()
