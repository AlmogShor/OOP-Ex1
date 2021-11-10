

class Elevator:
    def __init__(self, id=0, speed="", minFloor: int = 0, maxFloor="" , closeTime="",openTime="" , startTime= "", stopTime="") -> None:
        self.id = id
        self.speed=speed
        self.minFloor = minFloor
        self.maxFloor=maxFloor
        self.closeTime = closeTime
        self.openTime= openTime
        self.startTime=startTime
        self.stopTime=stopTime
