"""Locations for the simulation"""

from __future__ import annotations


class Location:
    """A two-dimensional location.

    """
    row: int
    column: int

    def __init__(self, row: int, column: int) -> None:
        """Initialize a location.
        """

        if row >= 0:
            self.row = row
        if column >= 0:
            self.column = column

    def __str__(self) -> str:
        """Return a string representation.
        >>> l = Location(2, 1)
        >>> print(l)
        (2, 1)
        """
        return f'({self.row}, {self.column})'

    def __eq__(self, other: Location) -> bool:
        """Return True if self equals other, and false otherwise.

        """
        if isinstance(other, Location):
            return self.row == other.row and self.column == other.column
        else:
            return False


def manhattan_distance(origin: Location, destination: Location) -> int:
    """Return the Manhattan distance between the origin and the destination.
    """
    return abs(origin.row - destination.row) + abs(origin.column - destination.
                                                   column)


def deserialize_location(location_str: str) -> Location:
    """Deserialize a location.

    location_str: A location in the format 'row,col'

    >>> print(deserialize_location('4, 6'))
    (4, 6)
    """
    deserialize_row = int(location_str.split(',')[0])
    deserialize_column = int(location_str.split(',')[1])
    return Location(deserialize_row, deserialize_column)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
