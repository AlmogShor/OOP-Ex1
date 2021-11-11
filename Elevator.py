from call_for_elevator import call_for_elevator


class Elevator:
    def __init__(self, id, speed: float = 0, minFloor: float = 0, maxFloor: float = 0, closeTime: float = 0,
                 openTime: float = 0, startTime: float = 0,
                 stopTime: float = 0) -> None:
        self.id = id
        self.speed = speed
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.closeTime = closeTime
        self.openTime = openTime
        self.startTime = startTime
        self.stopTime = stopTime
        self.calls = []
        self.pos = 0
        self.time = 0
        self.source = 0
        self.dest = 0

    def __str__(self) -> str:
        return f"id:{self.id} speed:{self.speed} minFloor:{self.minFloor} maxFloor:{self.maxFloor} closeTime:{self.closeTime} openTime:{self.openTime} StartTime:{self.startTime} stopTime:{self.stopTime}"

    def isEmpty(self):
        return True

    def currTime(self, time):
        ans = 0

    def addCall(self, call: call_for_elevator):
        if (not self.call):
            self.call.append(call)
            self.source = call.src
            self.dest = call.dst
            self.time = self.time + self.openTime + self.closeTime + self.startTime + self.stopTime + abs(
                self.source - self.dest) / self.speed
        else:
            self.call.append(call)
            self.time = call.call_time

    def lastCall(self):
        return self.call[-1]
