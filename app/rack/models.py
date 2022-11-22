from django.db import models

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

    def eject(self, row: int, column: int):
        if self.shelves[row][column]["present"]:
            self.shelves[row][column]["level"] = 0
            self.shelves[row][column]["present"] = False
        else:
            raise BatteryNotPresent

    def submit(self, row: int, column: int, battery_level: int):
        if self.shelves[row][column]["present"]:
            raise BatteryAlreadyPresent
        else:
            self.shelves[row][column]["level"] = battery_level
            self.shelves[row][column]["present"] = True

    def available_batteries(self) -> int:
        count = 0
        for row in self.shelves:
            for shelf in row:
                if shelf["present"] and shelf["level"] > 30:
                    count += 1
        return count
