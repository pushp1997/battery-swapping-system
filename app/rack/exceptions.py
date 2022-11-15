class BatteryNotPresent(Exception):
    def __str__(self) -> str:
        return "Rack shelf position provided does not have battery in it."


class BatteryAlreadyPresent(Exception):
    def __str__(self) -> str:
        return "Rack shelf position provided already has battery in it."
