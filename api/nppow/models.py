from django.db import models
from uuid import UUID

# Create your models here.


class Operation:
    id: UUID
    done: bool

    def __init__(self, id: UUID, done: bool = False, result=None) -> None:
        self.id = id
        self.done = done
        self.result = result

    def __eq__(self, other: "Operation") -> bool:
        return (
            self.id == other.id
            and self.done == other.done
            and self.result == other.result
        )
