from os import getenv

import factory
from django.contrib.auth.hashers import make_password
from dotenv import load_dotenv

from apps.users.models import User

load_dotenv()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password(getenv("FACTORY_USER_PW")))
    about = factory.Faker("sentence", nb_words=15, variable_nb_words=True)
    job = factory.Faker("job")
    company = factory.Faker("company")
    phone = factory.Faker("phone_number")


class AgentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password(getenv("FACTORY_USER_PW")))
    about = factory.Faker("sentence", nb_words=15, variable_nb_words=True)
    job = factory.Faker("job")
    company = factory.Faker("company")
    phone = factory.Faker("phone_number")
    role = 2
