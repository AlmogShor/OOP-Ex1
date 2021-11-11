class Building:
    def __init__(self, minFloor, maxFloor):
        self.min_floor = minFloor
        self.max_floor = maxFloor
        self.list_elvators = []

    def __str__(self) -> str:
        for i in self.list_elvators:
            print(i)

        return ""