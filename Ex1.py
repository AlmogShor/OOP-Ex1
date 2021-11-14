import csv
import json
import math
import sys

from Building import Building
from Elevator import Elevator
from CallForElevator import CallForElevator


def allocate(call_list: [CallForElevator()], b: Building, output):
    # i.data[0] - elevator call
    # i.data[1] - call time
    # i.data[2] - src
    # i.data[3] - dst
    # i.data[4] - status irrelevant
    # i.data[5] - elevator
    # i.data[6] - onboard
    # i.data[7] - start move
    # i.data[8] - end time
    # i.data[9] - mission
    # for every call in the call list
    for i in call_list:
        up_or_down = None
        if i.src < i.dst:
            up_or_down = 1
        else:
            up_or_down = -1
        idx_to_add_src = 0
        idx_to_add_dst = 0
        delay = 0
        case = 0
        min_time = sys.float_info.max
        tmp_time_to_call = 0
        # if there is a call outside the building floors
        if i.src < b.min_floor or i.src > b.max_floor or i.dst < b.min_floor or i.dst > b.max_floor:
            i.data[5] = -1
            continue
        # for every elevator in the building
        for j in b.list_elevators:
            for k in len(j.times):
                if i.call_time > j.times[k]:
                    continue
                if i.call_time < j.times[k]:
                    time_on_board = math.ceil(time_check(i, j, k-1))
                    if j.floors_mng[k-1] == i.src:
                        if j.times[k-1] >= i.call_time:






                    if j.floors_mng[k-1] < i.src < j.floors_mng[k]:
                        if time_on_board > -1:
                            if up_or_down == 1:
                                new_k = k
                                while new_k < len(j.times):
                                    # case 1- i have dst in the list
                                    if i.dst == j.floors_mng[new_k]:
                                        tmp_time_to_call = j.times[new_k] - i.call_time
                                        if tmp_time_to_call < min_time:
                                            min_time = tmp_time_to_call
                                            idx_to_add_src = k
                                            case = 1
                                    if i.dst < j.floors_mng[new_k]:
                                        tmp_time_to_call = calculate_time_for_call(i, j) + delay
                                        # case 2- place a call inside elev movement
                                        if tmp_time_to_call < min_time:
                                            min_time = tmp_time_to_call
                                            idx_to_add_src = k
                                            idx_to_add_dst = new_k
                                            case = 2
                                    if new_k < len(j.times)+1:
                                        if j.floors_mng[new_k] < i.dst < j.floors_mng[new_k+1]:
                                            delay = + math.ceil(j.stop_time + j.open_time) + math.ceil(j.close_time + j.start_time)
                                            continue
                                        if j.floors_mng < i.dst > j.floors_mng[new_k+1]:
                                            tmp_time_to_call = calculate_time_for_call(i, j) + delay
                                            if tmp_time_to_call < min_time:
                                                min_time = tmp_time_to_call
                                                idx_to_add_src = k
                                                idx_to_add_dst = new_k
                                                case = 3
                                    else:
                                        tmp_time_to_call = calculate_time_for_call(i, j) + delay
                                        if tmp_time_to_call < min_time:
                                            min_time = tmp_time_to_call
                                            idx_to_add_src = k
                                            case = 4
                                    new_k = +1


                    if j.floors_mng[k-1] > i.src > j.floors_mng[k]
                        if time_on_board > -1:
        #if we finished the for loop without break we will get into else
        else:






        # write in the csv
    out_file = open(output, "w", newline="")
    writer = csv.writer(out_file)
    for i in call_list:
        writer.writerow(i.data)
    out_file.close()


def time_check(curr_call: CallForElevator, elev: Elevator, idx):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    stop_t = elev.stop_time
    start_t = elev.start_time
    tmp_t = elev.times[idx] + close_t + start_t + (abs(curr_call.src-elev.floors_mng[idx]))/speed + stop_t + open_t
    if tmp_t >= curr_call.call_time:
        return tmp_t
    return -1


def calculate_time_for_call(curr_call: CallForElevator, elev: Elevator):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    stop_t = elev.stop_time
    start_t = elev.start_time
    return math.ceil(close_t + start_t + (abs(curr_call.src - curr_call.dst))/speed + stop_t + open_t)


def ex1(bld, calls, output):
    # Opening json file
    f = open(bld)
    data = json.load(f)
    # Creating a Building. Extracted from the json file
    b = Building(min_floor=data["_minFloor"], max_floor=data["_maxFloor"])
    # Creating the elevators in the building
    for i in data['_elevators']:
        elev = Elevator(idx=i['_id'], speed=i['_speed'], min_floor=i['_minFloor'], max_floor=i['_maxFloor'],
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
