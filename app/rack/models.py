from django.db import models

# Create your models here.
class Rack:
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __init__(self) -> None:
        self.shelves = [[{"level": 100, "locked": True}] * 5] * 5

    def unlock_shelf(self, i: int, j: int):
        self.shelves[i][j]["locked"] = False

    def lock_shelf(self, i: int, j: int):
        self.shelves[i][j]["locked"] = True

    def recharge(self):
        for row in self.shelves:
            for shelf in row:
                shelf["level"] += 1
