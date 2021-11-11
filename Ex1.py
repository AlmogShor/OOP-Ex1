import csv
import json

from Building import Building
from Elevator import Elevator
from CallForElevator import CallForElevator


def allocate(calllist: CallForElevator, b: Building, output):
    out_file = open(output, "w", newline="")
    writer = csv.writer(out_file)
    # mission = 0
    # time the person enter the elevator
    onboard = 0
    # end of call time
    endtime = 0
    # save the best elevator
    best_elv = -1
    # elevators id dont start with 0
    boaz_idiot = b.list_elvators[0].id

    # for every call in the call list
    for i in calllist:
        min_time = 1500
        # if there is a call outside the building floors
        if i.src < b.minFloor or i.src > b.maxFloor or i.dst < b.minFloor or i.dst > b.maxFloor:
            i.data[5] = -1
            writer.writerow(i.data)
            continue
        # for every elevator in the building
        for j in b.list_elvators:
            # for the current elevator check the time to the call
            if timecheck(i, j) < min_time:
                best_elv = j.id
                min_time = timecheck(i, j)
                onboard = int(min_time)+1
                endtime = onboard + calltime(i, j)

        # data i want to write in the csv
        i.data[5] = best_elv - boaz_idiot
        i.data[7] = onboard
        i.data[8] = endtime
        # added call to the elevator call list
        b.list_elvators[best_elv - boaz_idiot].calls.append(i)
        # write in the csv
        writer.writerow(i.data)
    out_file.close()


def timecheck(call: CallForElevator, elev: Elevator):
    if elev.calls:
        if elev.calls[-1].data[8] > call.callTime:
            return elev.calls[-1].data[8] + elev.closeTime + elev.startTime + (
                abs(elev.calls[-1].data[3] - call.src)) / elev.speed + elev.stopTime + elev.openTime
        else:
            if elev.calls[-1].data[3] == call.src:
                return call.callTime
            return call.callTime + elev.closeTime + elev.startTime + (
                abs(elev.calls[-1].data[3] - call.src)) / elev.speed + elev.stopTime + elev.openTime
    else:
        if call.src == 0:
            return call.callTime
        return call.callTime + elev.closeTime + elev.startTime + (
            abs(0 - call.src)) / elev.speed + elev.stopTime + elev.openTime


def calltime(call: CallForElevator, elev: Elevator):
    return elev.closeTime + elev.startTime + (abs(call.dst - call.src)) / elev.speed + elev.stopTime + elev.openTime


def ex1(bld, calls, output):
    # Opening json file
    f = open(bld)
    data = json.load(f)
    # Creating a Building. Extracted from the json file
    b = Building(minFloor=data["_minFloor"], maxFloor=data["_maxFloor"])
    # Creating the elevtors in the building
    for i in data['_elevators']:
        elev = Elevator(id=i['_id'], speed=i['_speed'], minFloor=i['_minFloor'], maxFloor=i['_maxFloor'],
                        closeTime=i['_closeTime'], openTime=i['_openTime'], startTime=i['_startTime'],
                        stopTime=i['_stopTime'])
        b.list_elvators.append(elev)

    # print(B)
    # Closing the json file
    f.close()
    # Opening CSV file
    c = open(calls)
    csvreader = csv.reader(c)
    # Creating the callForElevators objects
    idx = 0
    callslist = []
    for row in csvreader:
        call = CallForElevator(row[1], row[2], row[3], idx)
        idx = +1
        callslist.append(call)

    allocate(callslist, b, output)
    # Closing the CSV file
    c.close()


if __name__ == '__main__':
    ex1('data\\Ex1_input\\Ex1_Buildings\\B2.json', 'data\\Ex1_input\\Ex1_calls\\Calls_a.csv', 'out.csv')
