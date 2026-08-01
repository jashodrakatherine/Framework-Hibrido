"""Datos de prueba aleatorios (wrapper delgado sobre Faker)."""
from faker import Faker

fake = Faker()


def random_email() -> str:
    return fake.email()


def random_name() -> str:
    return fake.name()


def random_username() -> str:
    return fake.user_name()


def random_password(length: int = 12) -> str:
    return fake.password(length=length)


def random_phone() -> str:
    return fake.phone_number()


def random_address() -> str:
    return fake.address()
