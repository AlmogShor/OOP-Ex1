import csv
import json
import math
import sys

from Building import Building
from Elevator import Elevator
from CallForElevator import CallForElevator


def allocate(call_list: CallForElevator, b: Building, output):
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
        min_time = sys.float_info.max
        on_board = -1
        start_move = -1
        end_time = -1
        best_elv = -1
        mission = -1
        # if there is a call outside the building floors
        if i.src < b.min_floor or i.src > b.max_floor or i.dst < b.min_floor or i.dst > b.max_floor:
            i.data[5] = -1
            continue
        # for every elevator in the building
        for j in b.list_elevators:
            if not j.is_empty():
                for cll in j.calls:
                    time_check = check_time_to_add(i, j, cll)
                    if time_check == -1:
                        continue
                    if i.src < i.dst and cll.src < cll.dst:
                        if cll.src < i.src < cll.dst:
                                min_time = 0
                                on_board = time_check
                                start_move = time_check + j.close_time + j.start_time
                                end_time = time_check + time_elev_to_dst(i, j)
                                mission = cll.data[9]
                                best_elv = j.idx
                    if i.src > i.dst and cll.src > cll.dst:
                        if cll.src > i.src > cll.dst:
                                min_time = 0
                                on_board = time_check
                                start_move = time_check + j.close_time + j.start_time
                                end_time = time_check + time_elev_to_dst(i, j)
                                mission = cll.data[9]
                                best_elv = j.idx
            # check time to add in the end

            # last case- didnt find a place to push the call so add in the end
            time_to_me = time_elev_to_me(i, j)
            time_to_dst = time_elev_to_dst(i, j)
            dif = math.ceil(i.call_time) - i.call_time
            tmp_time = time_to_me + time_to_dst + dif
            if tmp_time < min_time:
                on_board = math.ceil(i.call_time) + time_to_me
                start_move = math.ceil(on_board + j.close_time + j.start_time)
                end_time = math.ceil(i.call_time) + time_to_me + time_to_dst
                min_time = tmp_time
                best_elv = j.idx
                if j.is_empty():
                    mission = 0
                else:
                    mission = j.calls[-1].data[9] + 1

        # data i want to write in the csv
        i.data[5] = best_elv
        i.data[6] = on_board
        i.data[7] = start_move
        i.data[8] = end_time
        i.data[9] = mission
        # added call to the elevator call list
        b.list_elevators[best_elv].calls.append(i)
        # write in the csv

    out_file = open(output, "w", newline="")
    writer = csv.writer(out_file)
    for i in call_list:
        writer.writerow(i.data)
    out_file.close()


def check_time_to_add(curr_call: CallForElevator, elev: Elevator, last_call: CallForElevator):
    if last_call.data[8] < curr_call.call_time:
        return -1
    tmp_time = math.ceil(last_call.data[7] + (abs(curr_call.src - last_call.src))/elev.speed + elev.stop_time + elev.open_time)
    if tmp_time < curr_call.call_time:
        return -1
    return tmp_time



def time_elev_to_me(curr_call: CallForElevator, elev: Elevator):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    start_t = elev.start_time
    stop_t = elev.stop_time
    if elev.is_empty():
        if curr_call.src == 0:
            return 0
        return math.ceil(close_t + start_t + curr_call.src/speed + stop_t + open_t)
    elif curr_call.src == elev.calls[-1].data[3]:
        if elev.calls[-1].data[8] <= curr_call.call_time:
            return 0
        return math.ceil(elev.calls[-1].data[8] - math.ceil(curr_call.call_time))
    else:
        if elev.calls[-1].data[8] <= curr_call.call_time:
            return math.ceil(close_t + start_t + abs(curr_call.src - elev.calls[-1].data[3]) / speed + open_t + stop_t)
        return math.ceil(elev.calls[-1].data[8] - math.ceil(curr_call.call_time) + close_t + start_t + abs(curr_call.src - elev.calls[-1].data[3]) / speed + open_t + stop_t)


def time_elev_to_dst(curr_call: CallForElevator, elev: Elevator):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    start_t = elev.start_time
    stop_t = elev.stop_time
    return math.ceil(close_t + start_t + abs(curr_call.src-curr_call.dst) / speed + stop_t + open_t)


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
