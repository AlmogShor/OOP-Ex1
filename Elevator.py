from CallForElevator import CallForElevator

class Elevator:
    def __init__(self, id: float, speed: float, minFloor: float, maxFloor: float, closeTime: float, openTime: float, startTime: float,
                 stopTime: float) -> None:
        self.id = id
        self.speed = int(speed)
        self.minFloor = int(minFloor)
        self.maxFloor = int(maxFloor)
        self.closeTime = int(closeTime)
        self.openTime = int(openTime)
        self.startTime = int(startTime)
        self.stopTime = int(stopTime)
        self.calls = []


    def __str__(self) -> str:
        return f"id:{self.id} speed:{self.speed} minFloor:{self.minFloor} maxFloor:{self.maxFloor} closeTime:{self.closeTime} openTime:{self.openTime} StartTime:{self.startTime} stopTime:{self.stopTime}"

    def isEmpty(self):
        return (not self.call)


