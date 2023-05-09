from dataclasses import dataclass
import uuid
from faker.factory import Factory
from polyfactory.factories import DataclassFactory

fake = Factory.create()


@dataclass
class Person:
    id: uuid.UUID
    firstname: str
    surname: str


class PersonFactory(DataclassFactory[Person]):
    __model__ = Person

    id = uuid.uuid4
    firstname = fake.first_name
    surname = fake.last_name


def create_persons(n: int):
    for i in range(n):
        yield PersonFactory.build()
