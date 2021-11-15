

class CallForElevator:
    def __init__(self, call_time, src, dst, idx):
        self.call_time = float(call_time)
        self.src = int(src)
        self.dst = int(dst)
        self.idx = idx
        self.dir = self.check_dir(src, dst)
        self.data = ['Elevator Call', float(call_time), int(src), int(dst), 0, -1, 0, 0, 0, 0]

    def __str__(self):
        print(self.call_time + ", " + self.src + ", " + self.dst)
        return ""

    def check_dir(self, src, dst):
        if src > dst: return -1
        else: return 1