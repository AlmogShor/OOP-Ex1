class Building:
    def __init__(self, minFloor, maxFloor):
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.list_elvators = []

    def __str__(self) -> str:
        for i in self.list_elvators:
            print(i)

        return ""