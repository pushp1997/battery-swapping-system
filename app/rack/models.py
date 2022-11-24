import time
from typing import Iterator
from threading import Thread

from django.conf import settings
from .exceptions import BatteryNotPresent, BatteryAlreadyPresent


# Create your models here.
class Rack:
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __init__(self) -> None:
        self.shelves = [[{"level": 100, "locked": True, "present": True}] * 5] * 5
        self.recharge_thread = Thread(target=self.recharge)
        self.recharge_thread.start()

    def unlock_shelf(self, row: int, column: int) -> None:
        if self.shelves[row][column]["present"]:
            self.shelves[row][column]["locked"] = False
        else:
            raise BatteryNotPresent

    def lock_shelf(self, row: int, column: int) -> None:
        if self.shelves[row][column]["present"]:
            self.shelves[row][column]["locked"] = True
        else:
            raise BatteryNotPresent

    def recharge(self) -> None:
        for row in self.shelves:
            for shelf in row:
                if shelf["present"] and shelf["level"] < 100:
                    shelf["level"] += 1
        time.sleep(settings.BATTERY_PER_PERCENTAGE_RECHARGE_TIME_IN_SECS)

    def eject(self, battery_positions: Iterator[list[int]]):
        """
        When asked to eject batteries from the rack, positions for all the batteries are needed to be
        provided and hence there present flag will be set to Flase and locked status to be 'unlocked'.

        Eg: input = [[2, 3], [4, 5]]
        """
        # if self.shelves[row][column]["present"]:
        #     self.shelves[row][column]["level"] = 0
        #     self.shelves[row][column]["present"] = False
        # else:
        #     raise BatteryNotPresent

    def submit(self, row: int, column: int, battery_level: int):
        if self.shelves[row][column]["present"]:
            raise BatteryAlreadyPresent
        else:
            self.shelves[row][column]["level"] = battery_level
            self.shelves[row][column]["present"] = True

    def request_withdrawal_of_batteries(self, no_of_batteries: int) -> list[list[int]]:
        """
        When user initiates a requst to withdraw batteries, kiossk needs to ask positions of the shelves
        from which the batteries are supposed to withdrawn. This method will return those positions,
        based on the no of batteries requested.

        eg: no_of_batteries = 2 -> [ [1, 2], [4, 5] ]
        """
        avlbl_positions = []
        for i, row in enumerate(self.shelves):
            for j, shelf in enumerate(row):
                if (
                    shelf["present"]
                    and shelf["level"] >= settings.BATTERY_STATUS_CHARGED_THRESHOLD_VALUE
                ):
                    avlbl_positions.append([i, j])
                    print(no_of_batteries)
                    no_of_batteries -= 1
                    if no_of_batteries == 0:
                        return avlbl_positions
        return avlbl_positions

    def rack_stats(self):
        # avlbl, undercharged, empty shelves
        charged_batteries, undercharged_batteries, empty_shelves = 0, 0, 0

        for row in self.shelves:
            for shelf in row:
                if shelf["present"]:
                    if shelf["level"] <= settings.BATTERY_STATUS_DISCHARGED_THRESHOLD_VALUE:
                        undercharged_batteries += 1
                    else:
                        charged_batteries += 1
                else:
                    empty_shelves += 1

        return {
            "charged_batteries": charged_batteries,
            "undercharged_batteries": undercharged_batteries,
            "empty_shelves": empty_shelves,
        }
