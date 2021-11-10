import csv
import json  # This is a sample Python script.
import struct
import sys
import importlib
from Building import Building
from callForElevator import callForElevator
from Elevator import Elevator
import pandas as pd


def allocate(callList, b):
    calls = []
    for i in callList:
        chosenElev = -1
        minTime = float(sys.float_info.max)
        for j in b.list_elvators:
            tmpTime = TimePeople(j, i)
            print()
            if (tmpTime <= minTime):
                minTime = tmpTime
                chosenElev = j.id

        b.list_elvators[chosenElev] = i
        calls.append(chosenElev)
    return calls


def TimePeople(elev, call: callForElevator) -> float:
    minTime = float(sys.float_info.max)
    tmpTime = 0
    print(elev.speed)
    if elev.isEmpty():
        # +time to move to the call floor
        tmpTime = + float(Elevator(elev).openTime) + float(Elevator(elev).closeTime)
        print(elev.speed)
        tmpTime = + Elevator(elev).startTime + abs(float(call.src) - float(call.dst)) / float(elev.speed)
        tmpTime = + elev.stopTime + elev.openTime
        if (tmpTime <= float(minTime)):
            minTime = tmpTime
        return minTime

    new = elev.lastCall()
    current = new
    if (call.src > current.src and call.dst < current.dst):
        time = call.callTime - current.callTime
        tmpTime = elev.startTime + abs(
            current.src - call.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
        if (time <= tmpTime):
            tmpTime = tmpTime + elev.startTime + abs(
                current.src - current.dst) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
            if (tmpTime <= minTime):
                minTime = tmpTime

    if (call.src < current.src and call.dst > current.dst):
        time = call.callTime - current.callTime
        tmpTime = elev.startTime + abs(
            current.src - call.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
        if (time <= tmpTime):
            tmpTime = tmpTime + elev.startTime + abs(
                current.src - current.dst) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
            if (tmpTime <= minTime):
                minTime = tmpTime

    tmpTime = elev.startTime + abs(current.dst - call.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
    timeofthelastcall = current.callTime + elev.startTime + abs(
        current.dst - current.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
    time = tmpTime + timeofthelastcall
    tmpTime2 = elev.startTime + abs(call.dst - call.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
    if (time >= call.callTime):
        tmpTime = tmpTime + elev.startTime + abs(
            current.src - current.dst) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
        if (tmpTime <= minTime):
            minTime = tmpTime
    return minTime


def Ex1(bld, calls, output):
    # Opening json file
    f = open(bld)
    data = json.load(f)
    # Creating a Building. Extracted from the json file
    B = Building(minFloor=data["_minFloor"], maxFloor=data["_maxFloor"])
    # print(data['_elevators'][0])
    # print(data['_elevators'][0]['_id'])
    # Creating the elevtors in the building
    for i in data['_elevators']:
        elev = Elevator(id=i['_id'], speed=i['_speed'], minFloor=i['_minFloor'], maxFloor=i['_maxFloor'],
                        closeTime=i['_closeTime'], openTime=i['_openTime'], startTime=i['_startTime'],
                        stopTime=i['_stopTime'])
        B.list_elvators.append(elev)

    # print(B)
    # Closing the json file
    f.close()
    # Opening CSV file
    c = open(calls)
    csvreader = csv.reader(c)
    # Creating the callForElevators objects
    idx = 0
    callsList = []
    for row in csvreader:
        call = callForElevator(row[1], row[2], row[3], idx)
        idx = +1
        callsList.append(call)

    b = allocate(callsList, B)
    print(b)
    # Closing the CSV file
    c.close()


if __name__ == '__main__':
    Ex1('f.json', 'Calls_a.csv', 'ex1.csv')