import csv
import json
import sys

from Building import Building
from Elevator import Elevator
from CallForElevator import CallForElevator


# this is the new one
def allocate(call_list: CallForElevator, b: Building, output):
    # for every call in the call list
    for i in call_list:
        min_time = sys.float_info.max
        # if there is a call outside the building floors
        if i.src < b.min_floor or i.src > b.max_floor or i.dst < b.min_floor or i.dst > b.max_floor:
            i.data[5] = -1
            continue
        # for every elevator in the building
        for j in b.list_elevators:
            on_board = -1
            end_time = -1
            best_elv = -1
            mission = -1

            if not j.is_empty():
                for cll in j:
                    if i.src < i.dst and cll.src < cll.dst:
                        if cll.src < i.src < cll.dst:
                            tmp_on_board = time_checker_for_can_add(i, cll, j)
                            if tmp_on_board > 0:
                                pass

                    if i.src > i.dst and cll.src > cll.dst:
                        if cll.src > i.src > cll.dst:
                            tmp_on_board = time_checker_for_can_add(i, cll, j)
                            if tmp_on_board > 0:
                                pass





        # data i want to write in the csv
        i.data[5] = best_elv
        i.data[6] = mission
        i.data[7] = on_board
        i.data[8] = end_time
        # added call to the elevator call list
        b.list_elevators[best_elv].calls.append(i)
        # write in the csv

    out_file = open(output, "w", newline="")
    writer = csv.writer(out_file)
    for i in call_list:
        writer.writerow(i.data)
    out_file.close()


def time_checker_for_can_add(curr_call: CallForElevator, cll: CallForElevator, elev: Elevator):
    if cll.data[7] + elev.close_time + elev.start_time + \
            (abs(curr_call.src - cll.src)) / elev.speed + elev.stop_time + elev.open_time > curr_call.call_time:
        return cll.data[7] + elev.close_time + elev.start_time + \
            (abs(curr_call.src - cll.src)) / elev.speed + elev.stop_time + elev.open_time
    else:
        return -1


def current_average(curr_call: CallForElevator, elev: Elevator):
    total_time = 0
    sum_people = 0
    if elev.is_empty():
        return 0
    for cll in elev.calls:
        if cll.data[8] > curr_call.call_time:
            pass


def ex1(bld, calls, output):
    # Opening json file
    f = open(bld)
    data = json.load(f)
    # Creating a Building. Extracted from the json file
    b = Building(min_floor=data["_minFloor"], max_floor=data["_maxFloor"])
    # Creating the elevators in the building
    for i in data['_elevators']:
        elev = Elevator(id=i['_id'], speed=i['_speed'], min_floor=i['_minFloor'], max_floor=i['_maxFloor'],
                        close_time=i['_closeTime'], open_time=i['_openTime'], start_time=i['_startTime'],
                        stop_time=i['_stopTime'])
        b.list_elevators.append(elev)

    # print(B)
    # Closing the json file
    f.close()
    # Opening CSV file
    c = open(calls)
    csv_reader = csv.reader(c)
    # Creating the callForElevators objects
    idx = 0
    call_list = []
    for row in csv_reader:
        call = CallForElevator(row[1], row[2], row[3], idx)
        idx = +1
        call_list.append(call)

    allocate(call_list, b, output)
    # Closing the CSV file
    c.close()


if __name__ == '__main__':
    ex1('data\\Ex1_input\\Ex1_Buildings\\B2.json', 'data\\Ex1_input\\Ex1_calls\\Calls_a.csv', 'out.csv')
