import csv
import json  # This is a sample Python script.
import sys
from Building import Building
from call_for_elevator import call_for_elevator
from Elevator import Elevator


# def TimePeople(elev, call: call_for_elevator) -> float:
#     min_time = float(sys.float_info.max)
#     tmpTime = 0
#     print(elev.speed)
#     if elev.isEmpty():
#         # +time to move to the call floor
#         tmpTime = + float(Elevator(elev).openTime) + float(Elevator(elev).closeTime)
#         print(elev.speed)
#         tmpTime = + Elevator(elev).startTime + abs(float(call.src) - float(call.dst)) / float(elev.speed)
#         tmpTime = + elev.stopTime + elev.openTime
#         if tmpTime <= float(min_time):
#             min_time = tmpTime
#         return min_time

# new = elev.lastCall()
# current = new
# if call.src > current.src and call.dst < current.dst:
#     time = call.callTime - current.callTime
#     tmpTime = elev.startTime + abs(
#         current.src - call.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
#     if time <= tmpTime:
#         tmpTime = tmpTime + elev.startTime + abs(
#             current.src - current.dst) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
#         if tmpTime <= min_time:
#             min_time = tmpTime
#
# if call.src < current.src and call.dst > current.dst:
#     time = call.callTime - current.callTime
#     tmpTime = elev.startTime + abs(
#         current.src - call.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
#     if time <= tmpTime:
#         tmpTime = tmpTime + elev.startTime + abs(
#             current.src - current.dst) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
#         if tmpTime <= min_time:
#             min_time = tmpTime
#
# tmpTime = elev.startTime + abs(current.dst - call.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
# time_of_the_last_call = current.callTime + elev.startTime + abs(
#     current.dst - current.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
# time = tmpTime + time_of_the_last_call
# tmpTime2 = elev.startTime + abs(call.dst - call.src) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
# if time >= call.callTime:
#     tmpTime = tmpTime + elev.startTime + abs(
#         current.src - current.dst) / elev.speed + elev.openTime + elev.closeTime + elev.stopTime
#     if tmpTime <= min_time:
#         min_time = tmpTime
# return min_time


def allocate(call_list: call_for_elevator, bld: Building, output):
    out_file = open(output, "w", newline="")
    writer = csv.writer(out_file)
    mission = 0
    onboard = 0
    end_time = 0
    reset_list_idx = bld.list_elvators[0].id

    for i in call_list:
        chosen_elev = -1
        min_time = float(sys.float_info.max)

        if i.src < bld.min_floor or i.src > bld.max_floor or i.dst < bld.min_floor or i.dst > bld.max_floor:
            i.data[5] = chosen_elev
            writer.writerow(i.data)
            continue

        for j in bld.list_elvators:
            tmp_time = call_time(j, i)

            if tmp_time <= min_time:
                chosen_elev = j.id
                min_time = tmp_time
                onboard = min_time
                end_time = min_time + tmp_time

            i.data[5] = chosen_elev - reset_list_idx
            i.data[7] = onboard
            i.data[8] = end_time
            bld.list_elvators[chosen_elev - reset_list_idx].calls.append(i)
            writer.writerow(i.data)
    out_file.close()


# Basic function to check how much time added per elevator
def time_check(call: call_for_elevator, elev: Elevator):
    if not elev.isEmpty():
        if elev.calls[-1].data[8] > call.call_time:
            return elev.calls[-1].data[8] + elev.closeTime + elev.startTime + (
                abs(elev.calls[-1].data[3] - call.src)) / elev.speed + elev.stopTime + elev.openTime
        else:
            if elev.calls[-1].data[3] == call.src:
                return call.call_time
            return call.call_time + elev.closeTime + elev.startTime + (
                abs(elev.calls[-1].data[3] - call.src)) / elev.speed + elev.stopTime + elev.openTime
    else:
        if call.src == 0:
            return call.call_time
        return call.call_time + elev.closeTime + elev.startTime + (
            abs(0 - call.src)) / elev.speed + elev.stopTime + elev.openTime


# Call time is a function thats consider the basic scenario - the elevator free and waiting for the call
def call_time(call: call_for_elevator, elev: Elevator):
    return elev.closeTime + elev.startTime + (abs(call.dst - call.src)) / elev.speed + elev.stopTime + elev.openTime


def Ex1(bld, calls, output):
    # Opening json file
    f = open(bld)
    data = json.load(f)
    # Creating a Building. Extracted from the json file
    building = Building(minFloor=data["_minFloor"], maxFloor=data["_maxFloor"])
    # Creating the elevators in the building
    for i in data['_elevators']:
        elev = Elevator(id=i['_id'], speed=i['_speed'], minFloor=i['_minFloor'], maxFloor=i['_maxFloor'],
                        closeTime=i['_closeTime'], openTime=i['_openTime'], startTime=i['_startTime'],
                        stopTime=i['_stopTime'])
        building.list_elvators.append(elev)

    # Closing the json file
    f.close()
    # Opening CSV file
    c = open(calls)
    csv_reader = csv.reader(c)
    # Creating the callForElevators objects
    idx = 0
    calls_list = []
    for row in csv_reader:
        call = call_for_elevator(row[1], row[2], row[3], idx)
        idx += 1
        calls_list.append(call)

    allocate(calls_list, building, output)
    # Closing the CSV file
    c.close()


if __name__ == '__main__':
    Ex1('data\\Ex1_input\\Ex1_Buildings\\B3.json', 'data\\Ex1_input\\Ex1_calls\\Calls_a.csv', 'out.csv')
