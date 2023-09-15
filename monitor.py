"""
The Monitor module contains the Monitor class, the Activity class,
and a collection of constants. Together the elements of the module
help keep a record of activities that have occurred.

Activities fall into two categories: Rider activities and Driver
activities. Each activity also has a description, which is one of
request, cancel, pickup, or dropoff.

=== Constants ===
RIDER: A constant used for the Rider activity category.
DRIVER: A constant used for the Driver activity category.
REQUEST: A constant used for the request activity description.
CANCEL: A constant used for the cancel activity description.
PICKUP: A constant used for the pickup activity description.
DROP OFF: A constant used for the drop-off activity description.
"""

from typing import Dict, List
from location import Location, manhattan_distance

RIDER = "rider"
DRIVER = "driver"

REQUEST = "request"
CANCEL = "cancel"
PICKUP = "pickup"
DROPOFF = "dropoff"


class Activity:
    """An activity that occurs in the simulation.

    === Attributes ===
    timestamp: The time at which the activity occurred.
    description: A description of the activity.
    identifier: An identifier for the person doing the activity.
    location: The location at which the activity occurred.
    """

    time: int
    description: str
    id: str
    location: Location

    def __init__(self, timestamp: int, description: str, identifier: str,
                 location: Location) -> None:
        """Initialize an Activity.

        """
        self.time = timestamp
        self.description = description
        self.id = identifier
        self.location = location


class Monitor:
    """A monitor keeps a record of activities that it is notified about.
    When required, it generates a report of the activities it has recorded.
    """

    # === Private Attributes ===
    _activities: Dict[str, Dict[str, List[Activity]]]

    #       A dictionary whose key is a category, and value is another
    #       dictionary. The key of the second dictionary is an identifier
    #       and its value is a list of Activities.

    def __init__(self) -> None:
        """Initialize a Monitor.

        """
        self._activities = {
            RIDER: {},
            DRIVER: {}
        }
        """@type _activities: dict[str, dict[str, list[Activity]]]"""

    def __str__(self) -> str:
        """Return a string representation.

        """
        return "Monitor ({} drivers, {} riders)".format(
            len(self._activities[DRIVER]), len(self._activities[RIDER]))

    def notify(self, timestamp: int, category: str, description: str,
               identifier: str, location: Location) -> None:
        """Notify the monitor of the activity.

        timestamp: The time of the activity.
        category: The category (DRIVER or RIDER) for the activity.
        description: A description (REQUEST | CANCEL | PICKUP | DROP_OFF)
            of the activity.
        identifier: The identifier for the actor.
        location: The location of the activity.
        """
        if identifier not in self._activities[category]:
            self._activities[category][identifier] = []

        activity = Activity(timestamp, description, identifier, location)
        self._activities[category][identifier].append(activity)

    def report(self) -> Dict[str, float]:
        """Return a report of the activities that have occurred.

        """
        return {"rider_wait_time": self._average_wait_time(),
                "driver_total_distance": self._average_total_distance(),
                "driver_ride_distance": self._average_ride_distance()}

    def _average_wait_time(self) -> float:
        """Return the average wait time of riders that have either been picked
        up or have cancelled their ride.

        """
        wait_time = 0
        count = 0
        for activities in self._activities[RIDER].values():
            # A rider that has less than two activities hasn't finished
            # waiting (they haven't cancelled or been picked up).
            if len(activities) >= 2:
                # The first activity is REQUEST, and the second is PICKUP
                # or CANCEL. The wait time is the difference between the two.
                wait_time += activities[1].time - activities[0].time
                count += 1
        return wait_time / count

    def _average_total_distance(self) -> float:
        """Return the average distance drivers have driven.
        >>> m2 = Monitor()
        >>> A1 = Activity(1,"request","Chris",Location(0,0))
        >>> A2 = Activity(3,"pickup","Chris",Location(10,2))
        >>> A3 = Activity(5,"dropoff","Chris",Location(1,3))
        >>> A4 = Activity(6,"request","Louis",Location(6,7))
        >>> A5 = Activity(2,"request","Chen",Location(3,3))
        >>> A6 = Activity(6,"cancel","Chen",Location(4,3))
        >>> A7 = Activity(9,"cancel","Louis",Location(0,0))
        >>> m2._activities = {RIDER:{},DRIVER:{"Chris":[A1,A2,A3], "Louis": [A4,A7],"Chen":[A5,A6]}}
        >>> m2._average_total_distance()
        12.0
        """
        total_distance = 0
        for activities in self._activities[DRIVER].values():
            i = 1
            while i < len(activities):
                total_distance += manhattan_distance(activities[i].location,
                                                     activities[i - 1].location)
                i += 1
        return total_distance / len(self._activities[DRIVER])

    def _average_ride_distance(self) -> float:
        """Return the average distance drivers have driven on rides.
        >>> m3 = Monitor()
        >>> A1 = Activity(1,"request","Chris",Location(0,0))
        >>> A2 = Activity(3,"pickup","Chris",Location(10,2))
        >>> A3 = Activity(5,"dropoff","Chris",Location(1,3))
        >>> A4 = Activity(6,"request","Louis",Location(6,7))
        >>> A5 = Activity(2,"request","Chen",Location(3,3))
        >>> A6 = Activity(6,"pickup","Chen",Location(4,0))
        >>> A7 = Activity(10,"dropoff","Chen",Location(13,20))
        >>> A8 = Activity(9,"cancel","Louis",Location(0,0))
        >>> m3._activities = {RIDER:{},DRIVER:{"Chris":[A1,A2,A3], "Louis":[A4,\
        A8],"Chen":[A5,A6,A7]}}
        >>> m3._average_ride_distance()
        13.0

        """
        total_distance = 0
        for activities in self._activities[DRIVER].values():
            for activity in activities:
                if activity.description == PICKUP:
                    item = activities.index(activity)
                    total_distance += manhattan_distance(
                        activities[item + 1].location,
                        activities[item].location)
        return total_distance / len(self._activities[DRIVER])


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(
        config={
            'max-args': 6,
            'extra-imports': ['typing', 'location']})
