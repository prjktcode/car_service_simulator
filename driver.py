"""Drivers for the simulation"""

from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    id: A unique identifier for the driver.
    location: The current location of the driver.
    is_idle: True if the driver is idle and False otherwise.
    """

    id: str
    location: Location
    is_idle: bool
    speed: int
    destination: Location or None
    rider: Rider

    def __init__(self, identifier: str, location: Location, speed: int) -> None:
        """Initialize a Driver.

        """
        self.rider = None
        self.location = location
        self.is_idle = True
        self.speed = speed
        self.destination = None
        self.id = identifier

    def __str__(self) -> str:
        """Return a string representation.
        >>> d = Driver('Johnny', Location(2,2), 90)
        >>> print(d)
        Driver Johnny -> Location: (2, 2), Is idle? True, Speed: 90
        """
        return f'Driver {self.id} -> Location: {self.location}, Is idle? ' \
               f'{self.is_idle}, Speed: {self.speed}'

    def __eq__(self, other: object) -> bool:
        """Return True if self equals other, and false otherwise.

        >>> d = Driver('Johnny', Location(1, 1), 90)
        >>> s =  Driver('Johnny', Location(1, 1), 90)
        >>> d == s
        True
        """
        if isinstance(other, Driver):
            if self.id == other.id and \
                    self.speed == other.speed and \
                    self.location == other.location and \
                    self.is_idle == other.is_idle and \
                    self.destination == other.destination:
                return True
            else:
                return False
        return False

    def get_travel_time(self, destination: Location) -> int:
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

       """
        return int((round(manhattan_distance(self.location, destination)
                          / self.speed, 0)))

    def start_drive(self, location: Location) -> int:
        """Start driving to the location.
        Return the time that the drive will take.

        """
        self.is_idle = False
        self.destination = location
        return self.get_travel_time(location)

    def end_drive(self) -> None:
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        """
        self.location = self.destination
        self.destination = None
        self.is_idle = True
        self.rider = None

    def start_ride(self, rider: Rider) -> int:
        """Start a ride and return the time the ride will take.

        """
        self.rider = rider
        self.destination = rider.destination
        self.is_idle = False
        return self.get_travel_time(rider.destination)

    def end_ride(self) -> None:
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        """
        self.location = self.destination
        self.destination = None
        self.is_idle = True
        self.rider = None


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={'extra-imports': ['location', 'rider']})
