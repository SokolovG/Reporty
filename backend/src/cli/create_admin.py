import asyncio
import click
from typing import TypeVar


T = TypeVar("T")


async def _create_admin_async(email: str, password: str) -> T:  # type: ignore
    click.echo(f"Creating admin with email: {email}")


@click.command()
@click.option("-e", "--email", prompt="Email", help="Email adress")
@click.option("-p", "--password", prompt="Password", help="Admin passwort")
def create_admin(email: str, password: str) -> T:  # type: ignore
    """Create admin user - sync wrapper"""
    asyncio.run(_create_admin_async(email=email, password=password))


if __name__ == "__main__":
    create_admin()
