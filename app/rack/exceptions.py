class BatteryNotPresent(Exception):
    def __str__(self) -> str:
        return "Rack shelf position provided does not have battery in it."


class BatteryAlreadyPresent(Exception):
    def __str__(self) -> str:
        return "Rack shelf position provided already has battery in it."


class NotEnoughEmptySlots(Exception):
    def __str__(self) -> str:
        return "Rack does not have enough empty slots in it."


class NotEnoughChargedBatteries(Exception):
    def __str__(self) -> str:
        return "Rack does not have enough charged batteries in it."
