

class CallForElevator:
    def __init__(self, callTime: float, src: int, dst: int, idx):
        self.callTime = float(callTime)
        self.src = int(src)
        self.dst = int(dst)
        self.idx =idx
        self.data = ['Elevator Call', float(callTime), int(src), int(dst), 0,-1,0,0,0]

    def __str__(self):
        print(self.callTime+", "+self.src+", "+self.dst)
        return ""

