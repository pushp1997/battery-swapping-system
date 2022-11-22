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

    def rack_stats(self):
        # avlbl, undercharged, empty slots
        charged_batteries, undercharged_batteries, empty_shelves = 0, 0, 0

        for row in self.shelves:
            for shelf in row:
                if shelf["present"]:
                    if shelf["level"] <= 30:
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
