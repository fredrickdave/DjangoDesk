import random

import factory
from dotenv import load_dotenv

from apps.tickets.models import Reference, Ticket

from ..users.factory import CustomerFactory

load_dotenv()


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    ticket_number = factory.LazyFunction(lambda: Reference.generate(prefix="INC"))
    summary = factory.Faker("sentence", nb_words=6)
    description = factory.Faker("sentence", nb_words=30)
    issue_type = factory.LazyFunction(lambda: random.randint(1, 4))
    created_by = factory.SubFactory(CustomerFactory)

    # https://factoryboy.readthedocs.io/en/latest/reference.html#factory.Factory._create
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj._change_reason = "Ticket has been created."
        obj._history_user = obj.created_by
        obj.save()
        return obj
