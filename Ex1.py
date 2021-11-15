import csv
import json
import math
import sys

from Building import Building
from Elevator import Elevator
from CallForElevator import CallForElevator


def allocate(call_list: [CallForElevator()], b: Building, output):
    # for every call in the call list
    for i in call_list:
        idx_to_add_src = 0
        idx_to_add_dst = 0
        best_elev = 0
        min_time = sys.float_info.max
        # if there is a call outside the building floors
        # for every elevator in the building
        for j in b.list_elevators:
            if len(j.floors_mng) == 1:
                time_to_src = time_first_call(i, j)
                time_from_src_to_dest = time_for_first_call_2(i, j)
                if time_to_src + time_from_src_to_dest < min_time:
                    best_elev = j.idx
                    time_in_src = time_to_src
                    time_in_dst = time_in_src + time_from_src_to_dest
            else:
                if j.times[-1] < i.call_time:
                    time_to_src = check_time(i, j)
                    time_from_src_to_dest = time_for_first_call_2(i, j)
                    if time_to_src - i.call_time + time_from_src_to_dest < min_time:
                        best_elev = j.idx
                        time_in_src = time_to_src
                        time_in_dst = time_in_src + time_from_src_to_dest
                else:
                    for k in len(j.floors_mng):
                        # elev going up and call up then last and can get go to command in time
                        if j.dir[k] == 1 and i.call_time < j.times[k] and j.floors_mng[k] < i.src:
                            idx_to_add_src = k + 1
                            time_to_src = times_sab(i, j, k)
                            idx_to_add_dst = where_is_dest(i, j, k)


                        if j.dir[k] == -1 and i.call_time < j.times[k] and j.floors_mng[k] > i.src:
                            idx_to_add_src = k + 1
                            time_to_src = times_sab(i, j, k)
                            idx_to_add_dst = where_is_dest(i, j, k)
                            time_to_dst = calc_time(i, j, idx_to_add_src, idx_to_add_src)[2]
                            delay = calc_time(i, j, idx_to_add_src, idx_to_add_src)[3]

                        if j.floors_mng[k] == i.src and i.call_time < j.times[k]:
                            idx_to_add_src = k + 1
                            time_to_src = j.times[k]
                            idx_to_add_dst = where_is_dest(i, j, k)


                        if k+1 < len(j.floors_mng):
                            # calls between floors
                            if j.floors_mng[k] < i.src < j.floors_mng[k + 1]:
                                idx_to_add_src = k + 1
                                idx_to_add_dst = where_is_dest(i, j, k)
                                # if we can stop in time
                            if j.floors_mng[k] < i.src < j.floors_mng[k + 1]:
                                idx_to_add_src = k + 1
                                idx_to_add_dst = where_is_dest(i, j, k)
                                # if we can stop in time







        # write in the csv
    out_file = open(output, "w", newline="")
    writer = csv.writer(out_file)
    for i in call_list:
        writer.writerow(i.data)
    out_file.close()


def calc_time(curr: CallForElevator, elev: Elevator, s_id, d_id):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    stop_t = elev.stop_time
    start_t = elev.start_time
    time_to_src = elev.times[s_id - 1] + close_t + start_t + (abs(elev.floors_mng[s_id - 1] - curr.src)) / speed + stop_t + open_t
    if s_id == d_id:
        time_from_src_to_dst = close_t + start_t + (abs(curr.dst - curr.src))/speed + stop_t + open_t
        time_from_dst_to_next = close_t + start_t + (abs(curr.dst - elev.floors_mng[s_id]))/speed + stop_t + open_t
        return [time_to_src, time_to_src + time_from_src_to_dst,time_to_src + time_from_src_to_dst + time_from_dst_to_next - elev.times[s_id]]
    else:
        time_from_src_to_next = close_t + start_t + (abs(curr.src - elev.floors_mng[s_id]))/speed + stop_t + open_t
        time_in_next_src = time_to_src + time_from_src_to_next
        delay = time_in_next_src - elev.times[s_id]
        time_to_dst = elev.times[d_id - 1] + close_t + start_t + (abs(elev.floors_mng[d_id - 1] - curr.dst)) / speed + stop_t + open_t + delay
        return [time_to_src, time_to_dst, delay]

def where_is_dest(curr: CallForElevator, elev: Elevator, k):
    if elev.dir[k] == 1 and curr.dir == 1:
        new_k = k+1
        while new_k < len(elev.floors_mng):
            if elev.floors_mng[new_k] == curr.dst:
                return new_k
            if elev.dir[new_k] == -1:
                return new_k
            if elev.floors_mng[new_k] > curr.dst:
                return new_k
            if elev.floors_mng[new_k] < curr.dst:
                new_k = +1
        else:
            return new_k
    if elev.dir[k] == -1 and curr.dir == -1:
        new_k = k+1
        while new_k < len(elev.floors_mng):
            if elev.floors_mng[new_k] == curr.dst:
                return new_k
            if elev.dir[new_k] == 1:
                return new_k
            if elev.floors_mng[new_k] < curr.dst:
                return new_k
            if elev.floors_mng[new_k] > curr.dst:
                new_k = +1
        else:
            return new_k
    if elev.dir[k] == 1 and curr.dir == -1:
        new_k = k + 1
        while new_k < len(elev.floors_mng):
            if elev.floors_mng[new_k] == curr.dst:
                return new_k
            if elev.dir[new_k] == 1:
                new_k = +1
                continue
            if elev.dir[new_k] == -1 and elev.floors_mng[new_k] < curr.dst:
                return new_k
            if elev.dir[new_k] == -1 and elev.floors_mng[new_k] > curr.dst:
                new_k = +1
        else:
            return new_k
    if elev.dir[k] == -1 and curr.dir == 1:
        new_k = k + 1
        while new_k < len(elev.floors_mng):
            if elev.floors_mng[new_k] == curr.dst:
                return new_k
            if elev.dir[new_k] == -1:
                new_k = +1
                continue
            if elev.dir[new_k] == 1 and elev.floors_mng[new_k] > curr.dst:
                return new_k
            if elev.dir[new_k] == 1 and elev.floors_mng[new_k] < curr.dst:
                new_k = +1
        else:
            return new_k


def times_sab(curr: CallForElevator, elev: Elevator, k):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    stop_t = elev.stop_time
    start_t = elev.start_time
    last_floor = elev.floors_mng[k]
    return elev.times[k] + math.ceil(close_t + start_t + (abs(last_floor - curr.src))/speed + stop_t + open_t)


def check_time(curr: CallForElevator, elev: Elevator):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    stop_t = elev.stop_time
    start_t = elev.start_time
    if curr.src == elev.floors_mng[-1]:
        return math.ceil(curr.call_time)
    return math.ceil(curr.call_time) + close_t + start_t + (abs(elev.floors_mng[-1] - curr.src))/speed + stop_t +open_t


def time_first_call(curr: CallForElevator, elev: Elevator):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    stop_t = elev.stop_time
    start_t = elev.start_time
    if curr.src == 0:
        return math.ceil(curr.call_time)
    return math.ceil(close_t + start_t + (abs(curr.src))/speed + stop_t + open_t)


def time_for_first_call_2(curr: CallForElevator, elev: Elevator):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    stop_t = elev.stop_time
    start_t = elev.start_time
    return math.ceil(close_t + start_t + (abs(curr.src - curr.dst))/speed + stop_t + open_t)


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
