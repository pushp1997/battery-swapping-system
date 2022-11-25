import time
from threading import Thread

from django.conf import settings
from .exceptions import (
    BatteryNotPresent,
    BatteryAlreadyPresent,
    NotEnoughEmptySlots,
    NotEnoughChargedBatteries,
)
from .utils import generate_random_battery_level_for_battery_inserted_by_user


# Create your models here.
class Rack:
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def __init__(self) -> None:
        self.shelves = [
            [{"level": 100, "locked": True, "present": True} for _ in range(5)] for _ in range(5)
        ]
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

    def eject(self, battery_positions: list[list[int]]):
        """
        When asked to eject batteries from the rack, positions for all the batteries are needed to be
        provided and hence there present flag will be set to Flase and locked status to be 'unlocked'.
        It returns the battery levels of the batteries ejected w.r.t the position sequence.

        Eg: input = [[2, 3], [4, 5]]; output = [100, 95]
        """
        battery_levels = []
        for battery_position in battery_positions:
            if self.shelves[battery_position[0]][battery_position[1]]["present"]:
                battery_levels.append(
                    self.shelves[battery_position[0]][battery_position[1]]["level"]
                )
                self.shelves[battery_position[0]][battery_position[1]]["level"] = 0
                self.unlock_shelf(battery_position[0], battery_position[1])
                self.shelves[battery_position[0]][battery_position[1]]["present"] = False
            else:
                raise BatteryNotPresent
        return battery_levels

    def submit(self, battery_positions: list[list[int]]):
        """
        When asked to submit batteries to the rack, positions for all the batteries are needed to be
        provided along with the battery percentage in them and hence there present flag will be set to True
        and locked status to be 'locked'.

        Eg: input = [[2, 3, 15], [4, 5, 8]]
        """
        for battery_position in battery_positions:
            if self.shelves[battery_position[0]][battery_position[1]]["present"]:
                raise BatteryAlreadyPresent
            else:
                self.shelves[battery_position[0]][battery_position[1]]["level"] = battery_position[
                    2
                ]
                self.shelves[battery_position[0]][battery_position[1]]["present"] = True
                self.lock_shelf(battery_position[0], battery_position[1])

    def request_withdrawal_of_batteries(self, no_of_batteries: int) -> list[list[int]]:
        """
        When user initiates a requst to withdraw batteries, kiosk needs to ask positions of the shelves
        from which the batteries are supposed to withdrawn. This method will return those positions,
        based on the no of batteries requested.

        eg: no_of_batteries = 2 -> [ [1, 2], [4, 5] ]
        """
        # Searching for all positions which have charged batteries
        avlbl_positions = []
        found_all = False
        for i, row in enumerate(self.shelves):
            for j, shelf in enumerate(row):
                if (
                    shelf["present"]
                    and shelf["level"] >= settings.BATTERY_STATUS_CHARGED_THRESHOLD_VALUE
                ):
                    avlbl_positions.append([i, j])
                    no_of_batteries -= 1
                    if no_of_batteries == 0:
                        found_all = True
                        break
            if found_all:
                break
        if no_of_batteries > 0:
            raise NotEnoughChargedBatteries

        # Withdrawing batteries from the found positions
        return self.eject(avlbl_positions)

    def request_submission_of_batteries(self, no_of_batteries: int) -> list[list[int]]:
        """
        When user initiates a requst to submit batteries, kiosk needs to provide positions of the shelves
        to which the batteries are supposed to submitted by the user. This method will return those positions,
        based on the no of batteries requested.

        eg: no_of_batteries = 2 -> [ [1, 2], [4, 5] ]
        """
        # Searching for all positions which are empty
        battery_levels_deposited = []
        empty_positions = []
        found_all = False
        for i, row in enumerate(self.shelves):
            for j, shelf in enumerate(row):
                if not shelf["present"]:
                    battery_level_deposited = (
                        generate_random_battery_level_for_battery_inserted_by_user()
                    )
                    battery_levels_deposited.append(battery_level_deposited)
                    empty_positions.append([i, j, battery_level_deposited])
                    no_of_batteries -= 1
                    if no_of_batteries == 0:
                        found_all = True
                        break
            if found_all:
                break
        if no_of_batteries > 0:
            raise NotEnoughEmptySlots

        # Submitting batteries for the found positions
        self.submit(empty_positions)
        return battery_levels_deposited

    def rack_stats(self) -> dict[str, int]:
        """
        This method returns the statistics about the rack, which are: total no of available batteries,
        discharged batteries and empty shelves that do not have battery in them.

        eg: Output: {
            "charged_batteries": 20,
            "undercharged_batteries": 2,
            "empty_shelves": 3,
        }
        """
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
