"""Dispatcher for the simulation"""

from typing import Optional
from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.

    """
    driver_register: list
    riders_waiting_list: list

    def __init__(self) -> None:
        """Initialize a Dispatcher.

        """
        self.driver_register = []
        self.riders_waiting_list = []

    def __str__(self) -> str:
        """Return a string representation of the driver_register and the
         riders_waiting_list. Each rider is separated by a line. After the
         riders_waiting_list, a blank line separates them to the
         driver_register
        """
        rider_string = ''
        driver_string = ''
        for rider in self.riders_waiting_list:
            rider_string += rider.__str__() + '\n'
        for driver in self.driver_register:
            driver_string += driver.__str__() + '\n'
        return 'Rider Waiting list: ' + rider_string + '\n' + \
            'Driver Waiting List: ' + driver_string + '\n'

    def request_driver(self, rider: Rider) -> Optional[Driver]:
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.
        """
        if len(self.driver_register) == 0:
            self.riders_waiting_list.append(rider)
            return None

        elif len(self.driver_register) == 1:
            fastest = self.driver_register[0]
            fastest.is_idle = False
            return fastest
        else:
            fastest = self.driver_register[0]
            for available_driver in self.driver_register[1:]:
                if available_driver.start_drive(rider.origin) <= \
                        fastest.start_drive(rider.origin):
                    fastest = available_driver
                    fastest.is_idle = False
            return fastest

    def request_rider(self, driver: Driver) -> Optional[Rider]:
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.
        """

        if driver not in self.driver_register:
            self.driver_register.append(driver)
        if len(self.riders_waiting_list) == 0:
            return None
        else:
            rider_assigned = self.riders_waiting_list.pop(0)
            driver.destination = rider_assigned.origin
            driver.is_idle = False

        return rider_assigned

    def cancel_ride(self, rider: Rider) -> None:
        """Cancel the ride for rider.
        """
        if rider in self.riders_waiting_list:
            self.riders_waiting_list.remove(rider)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing', 'driver', 'rider']})
