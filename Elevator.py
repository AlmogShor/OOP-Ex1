from CallForElevator import CallForElevator

class Elevator:
    def __init__(self, id: float, speed: float, minFloor: float, maxFloor: float, closeTime: float, openTime: float, startTime: float,
                 stopTime: float) -> None:
        self.id = id
        self.speed = float(speed)
        self.minFloor = float(minFloor)
        self.maxFloor = float(maxFloor)
        self.closeTime = float(closeTime)
        self.openTime = float(openTime)
        self.startTime = float(startTime)
        self.stopTime = float(stopTime)
        self.calls = []


    def __str__(self) -> str:
        return f"id:{self.id} speed:{self.speed} minFloor:{self.minFloor} maxFloor:{self.maxFloor} closeTime:{self.closeTime} openTime:{self.openTime} StartTime:{self.startTime} stopTime:{self.stopTime}"

    def isEmpty(self):
        return (not self.call)


