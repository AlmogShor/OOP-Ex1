from CallForElevator import CallForElevator
class Elevator:
    def __init__(self, idx: float, speed: float, min_floor: float, max_floor: float, close_time: float,
                 open_time: float, start_time: float, stop_time: float):
        self.idx = idx
        self.speed = float(speed)
        self.min_floor = float(min_floor)
        self.max_floor = float(max_floor)
        self.close_time = float(close_time)
        self.open_time = float(open_time)
        self.start_time = float(start_time)
        self.stop_time = float(stop_time)
        self.calls = [CallForElevator()]
        self.floors_mng = [0]
        self.times = [0]
        self.dir = [0]
        self.id_mng = [0]

    def __str__(self) -> str:
        return f"id:{self.idx} speed:{self.speed} minFloor:{self.min_floor} maxFloor:{self.max_floor} closeTime:{self.close_time} openTime:{self.open_time} StartTime:{self.start_time} stopTime:{self.stop_time}"

    def is_empty(self):
        return not self.calls
