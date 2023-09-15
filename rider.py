"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
WAITING: A constant used for the waiting rider status.
CANCELLED: A constant used for the cancelled rider status.
SATISFIED: A constant used for the satisfied rider status
"""

from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """A rider for a ride-sharing service.

    """
    id: str
    origin: Location
    destination: Location
    patience: int
    status: str

    def __init__(self, identifier: str, origin: Location, destination: Location,
                 patience: int) -> None:
        """Initialize a Rider.

        """
        self.id = identifier
        self.origin = origin
        self.destination = destination
        self.status = WAITING
        self.patience = patience

    def __str__(self) -> str:
        """Return a string representation of the rider in the form of 'Rider
        (id) -> Origin: (origin), Destination: (destination), Patience
        (patience), Status: (status)
        """

        return f'Rider {self.id} -> Origin: {self.origin}, Destination:' \
               f' {self.destination}, Patience {self.patience}, Status: ' \
               f'{self.status}'

    def __eq__(self, other: Location) -> bool:
        """Evaluate if one rider is equivalent to another by assessing if they
        other is Rider then assessing if they have the same id, origin,
        destination, and status.
        """
        if isinstance(other, Rider):
            if self.patience == other.patience and self.id == other.id and \
                    self.origin == other.origin and \
                    self.destination == other.destination and \
                    self.status == other.status:
                return True
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['location']})
