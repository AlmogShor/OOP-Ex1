import csv
import json
import math
import sys

from Building import Building
from Elevator import Elevator
from CallForElevator import CallForElevator


def allocate(call_list: [CallForElevator()], b: Building, output):
    # time the person enter the elevator

    # end of call time

    # save the best elevator
    best_elv = -1
    # elevators id dont start with 0

    # for every call in the call list
    for i in call_list:
        on_board = 0
        end_time = 0
        best_elv = -1
        idx_src = 0
        idx_dst = 0
        tmp_end_time = 0
        tmp_on_board = 0
        delay = 0
        call_t = 0
        min_time = sys.float_info.max
        # for every elevator in the building
        for j in b.list_elevators:
            # @add next- contain
            if j.is_empty():
                tmp_on_board, tmp_end_time, call_t = check_call_time_0(i, j)
                if call_t < min_time:
                    idx_src = 1
                    idx_dst = 1
                    best_elv = j.id
                    min_time = call_t
                    on_board = tmp_on_board
                    end_time = tmp_end_time
            else:
                # Checking each call that currently in the elevator
                for k in len(j.floor_mng):
                    # Check if the new call is possibly to catch the elevator that's just arrived to its floor
                    if j.floor_mng[k] == i.src and j.times[k] + math.floor(j.close_time + j.start_time) > i.call_time:
                        # Possible there is a person that's already waiting for an elevator
                        if j.times[k] > i.call_time:
                            tmp_on_board = j.times[k]
                        # Else - the person just entered the elevator
                        else:
                            tmp_on_board = j.times[k] + math.ceil(
                                j.close_time + j.start_time + j.stop_time + j.open_time)
                            call_t, tmp_end_time, tmp_delay, tmp_idx_dst = calc_time_1(i, j, k, tmp_on_board)
                        if call_t < min_time:
                            idx_src = k + 1
                            idx_dst = tmp_idx_dst
                            best_elv = j.id
                            min_time = call_t
                            on_board = tmp_on_board
                            end_time = tmp_end_time
                            delay = tmp_delay
                    elif k < len(j.floor_mng) - 1:
                        if j.floor_mng[k] < i.src < j.floor_mng[k + 1] and can_the_elevator_stop(i, j, k):
                            call_t, tmp_end_time, tmp_delay, tmp_idx_dst = calc_time_2(i, j, k, tmp_on_board)
                            if call_t < min_time:
                                idx_src = k + 1
                                idx_dst = tmp_idx_dst
                                best_elv = j.id
                                min_time = call_t
                                on_board = tmp_on_board
                                end_time = tmp_end_time
                        if j.floor_mng[k] > i.src > j.floor_mng[k + 1] and can_the_elevator_stop(i, j, k):
                            call_t, tmp_end_time, tmp_delay, tmp_idx_dst = calc_time_3(i, j, k, tmp_on_board)
                            if call_t < min_time:
                                idx_src = k + 1
                                idx_dst = tmp_idx_dst
                                best_elv = j.id
                                min_time = call_t
                                on_board = tmp_on_board
                                end_time = tmp_end_time
                    elif k > 0:
                        if i.src > j.floor_mng[k] > j.floor_mng[k - 1]:
                            # @tmp_on_board
                            # @how much time to finish the call
                            # @idx to add dst
                            # @delay
                            # @end time call
                            if call_t < min_time:
                                idx_src = k + 1
                                idx_dst = 0
                                best_elv = j.id
                                min_time = call_t
                                on_board = tmp_on_board
                                end_time = tmp_end_time
                        if i.src < j.floor_mng[k] < j.floor_mng[k - 1]:
                            # @tmp_on_board
                            # @how much time to finish the call
                            # @idx to add dst
                            # @delay
                            # @end time call
                            if call_t < min_time:
                                idx_src = k + 1
                                idx_dst =

                                @

                                best_elv = j.id
                                min_time = call_t
                                on_board = tmp_on_board
                                end_time = tmp_end_time
                    else:
                        # @tmp_on_board
                        # @how much time to finish the call
                        # @idx to add dst
                        # @delay
                        # @end time call
                        if call_t < min_time:
                            idx_src = len(j.floor_mng)
                            idx_dst = len(j.floor_mng) + 1
                            best_elv = j.id
                            min_time = call_t
                            on_board = tmp_on_board
                            end_time = tmp_end_time

        # delay function if its not 0
        j.floor_mng.insert(idx_src, i.src)
        j.times.insert(idx_src, on_board)
        j.times.insert(idx_src, i.idx)

        j.floor_mng.insert(idx_dst + 1, i.dst)
        j.times.insert(idx_dst + 1, end_time)
        j.times.insert(idx_dst + 1, i.idx)
        i.data[5] = best_elv
        i.data[7] = on_board
        i.data[8] = end_time
        b.list_elevators[best_elv].calls.append(i)

        #     # for the current elevator check the time to the call
        #     if time_check(i, j) < min_time:
        #         best_elv = j.id
        #         min_time = time_check(i, j)
        #         on_board = int(min_time)+1
        #         end_time = on_board + call_time(i, j)
        # # data i want to write in the csv
        # i.data[5] = best_elv
        # i.data[7] = on_board
        # i.data[8] = end_time
        # # added call to the elevator call list

        # # write in the csv

    out_file = open(output, "w", newline="")
    writer = csv.writer(out_file)
    for i in call_list:
        writer.writerow(i.data)
    out_file.close()


def calc_time_1(call: CallForElevator, elev: Elevator, k, tmp_on_board):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    start_t = elev.start_time
    stop_t = elev.stop_time
    delay = tmp_on_board - elev.times[k]
    if call.dir == 1 and elev.floor_mng[k - 1] < elev.floor_mng[k]:
        while k + 1 < len(elev.floor_mng):
            if elev.floor_mng[k + 1] == call.dst:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
                if end_t == elev.times[k + 1]:
                    return end_t - call.call_time, end_t, 0, k
                else:
                    return end_t - call.call_time, end_t, end_t - elev.times[k + 1], k
            if elev.floor_mng[k + 1] < call.src:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
                call_t = end_t - call.call_time
                delay = end_t + math.ceil(
                    close_t + start_t + (abs(call.dst - elev.floor_mng[k + 1])) + stop_t + open_t) - elev.times[k + 1]
                if delay < 0:
                    delay = 0
                return call_t, end_t, delay, k
            #q. How this is possible? the direction is up, but the destination is lower than the curr floor??
            if call.dst < elev.floor_mng[k]:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
                call_t = end_t - call.call_time
                delay = math.ceil(open_t + stop_t) + math.ceil(start_t + close_t)
                return call_t, end_t, delay, k
            if call.dst > elev.floor_mng[k + 1]:
                while k + 1 < len(elev.floor_mng):
                    if call.dst > elev.floor_mng[k + 1]:
                        k = k + 1
                    elif call.dst == elev.floor_mng[k + 1]:
                        end_t = delay + elev.times[k + 1]
                        call_t = end_t - call.call_time
                        return call_t, end_t, delay, k + 1
                    elif call.dst < elev.floor_mng[k + 1]:
                        k = k - 1
                        break
                    else:
                        break
                end_t = elev.times[k] + math.ceil(
                    close_t + start_t + (abs(elev.floor_mng[k] - call.dst)) / speed + stop_t + open_t + delay)
                call_t = end_t - call.call_time
                return call_t, end_t, delay, k + 1
        else:
            end_t = math.ceil(tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
            call_t = end_t - call.call_time
            return call_t, end_t, 0, k

    if call.dir == 1 and elev.floor_mng[k - 1] > elev.floor_mng[k]:
        if k + 1 < len(elev.floor_mng):
            while elev.floor_mng[k + 1] < elev.floor_mng[k]:
                k = k + 1
            if k + 1 < len(elev.floor_mng):
                while k + 1 < len(elev.floor_mng):
                    if call.dst > elev.floor_mng[k + 1]:
                        k = k + 1
                    elif call.dst == elev.floor_mng[k + 1]:
                        end_t = delay + elev.times[k + 1]
                        call_t = end_t - call.call_time
                        return call_t, end_t, delay, k + 1
                    elif call.dst < elev.floor_mng[k + 1]:
                        k = k - 1
                        break
                    else:
                        break
                end_t = elev.times[k] + math.ceil(
                    close_t + start_t + (abs(elev.floor_mng[k] - call.dst)) / speed + stop_t + open_t + delay)
                call_t = end_t - call.call_time
                return call_t, end_t, delay, k + 1
        else:
            end_t = math.ceil(tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
            call_t = end_t - call.call_time
            return call_t, end_t, 0, k

    if call.dir == -1 and elev.floor_mng[k - 1] > elev.floor_mng[k]:
        if k + 1 < len(elev.floor_mng):
            if elev.floor_mng[k + 1] == call.dst:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
                if end_t == elev.times[k + 1]:
                    return end_t - call.call_time, end_t, 0, k
                else:
                    return end_t - call.call_time, end_t, end_t - elev.times[k + 1], k
            if elev.floor_mng[k + 1] > call.src:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
                call_t = end_t - call.call_time
                delay = end_t + math.ceil(
                    close_t + start_t + (abs(call.dst - elev.floor_mng[k + 1])) + stop_t + open_t) - elev.times[k + 1]
                if delay < 0:
                    delay = 0
                return call_t, end_t, delay, k
            if call.dst > elev.floor_mng[k]:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
                call_t = end_t - call.call_time
                delay = math.ceil(open_t + stop_t) + math.ceil(start_t + close_t)
                return call_t, end_t, delay, k
            if call.dst < elev.floor_mng[k + 1]:
                delay = tmp_on_board - elev.times[k]
                while k + 1 < len(elev.floor_mng):
                    if call.dst < elev.floor_mng[k + 1]:
                        k = k + 1
                    elif call.dst == elev.floor_mng[k + 1]:
                        end_t = delay + elev.times[k + 1]
                        call_t = end_t - call.call_time
                        return call_t, end_t, delay, k + 1
                    elif call.dst > elev.floor_mng[k + 1]:
                        k = k - 1
                        break
                    else:
                        break
                end_t = elev.times[k] + math.ceil(
                    close_t + start_t + (abs(elev.floor_mng[k] - call.dst)) / speed + stop_t + open_t + delay)
                call_t = end_t - call.call_time
                return call_t, end_t, delay, k + 1
        else:
            end_t = math.ceil(tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
            call_t = end_t - call.call_time
            return call_t, end_t, 0, k

    if call.dir == -1 and elev.floor_mng[k - 1] < elev.floor_mng[k]:
        if k + 1 < len(elev.floor_mng):
            while elev.floor_mng[k + 1] > elev.floor_mng[k]:
                k = k + 1
            if k + 1 < len(elev.floor_mng):
                while k + 1 < len(elev.floor_mng):
                    if call.dst < elev.floor_mng[k + 1]:
                        k = k + 1
                    elif call.dst == elev.floor_mng[k + 1]:
                        end_t = delay + elev.times[k + 1]
                        call_t = end_t - call.call_time
                        return call_t, end_t, delay, k + 1
                    elif call.dst > elev.floor_mng[k + 1]:
                        k = k - 1
                        break
                    else:
                        break
                end_t = elev.times[k] + math.ceil(
                    close_t + start_t + (abs(elev.floor_mng[k] - call.dst)) / speed + stop_t + open_t + delay)
                call_t = end_t - call.call_time
                return call_t, end_t, delay, k + 1
        else:
            end_t = math.ceil(tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
            call_t = end_t - call.call_time
            return call_t, end_t, 0, k


# Calculation time for elevator on the way up and the call source is in the middle of this current call of the elevator
def calc_time_2(call: CallForElevator, elev: Elevator, k, tmp_on_board):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    start_t = elev.start_time
    stop_t = elev.stop_time
    delay = tmp_on_board - elev.times[k]
    # If the call direction is up as well
    if call.dir == 1:
        while k + 1 < len(elev.floor_mng):
            # If there is a stop on the destination floor already
            if elev.floor_mng[k + 1] == call.dst:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + stop_t + open_t)
                return end_t - call.call_time, end_t, end_t - elev.times[k + 1], k
            # If the current destination is closer then the next existing destination of the elevator
            if call.dst < elev.floor_mng[k + 1]:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
                call_t = end_t - call.call_time
                delay = end_t + math.ceil(
                    close_t + start_t + (abs(call.dst - elev.floor_mng[k + 1])) + stop_t + open_t) - elev.times[k + 1]
                if delay < 0:
                    delay = 0
                return call_t, end_t, delay, k
            # if the exxisting destination is lower than the current call destination go to the next call destination
            if call.dst > elev.floor_mng[k + 1]:
                k = k + 1
                continue;
                # q. Is it good?
            end_t = elev.times[k] + math.ceil(
                close_t + start_t + (abs(elev.floor_mng[k] - call.dst)) / speed + stop_t + open_t + delay)
            call_t = end_t - call.call_time
            return call_t, end_t, delay, k + 1
        else:
            end_t = math.ceil(tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
            call_t = end_t - call.call_time
            return call_t, end_t, 0, k
    #If the call direction is in the opposite direction
    if call.dir == -1:
        while elev.floor_mng[k + 1] > elev.floor_mng[k] and k + 1 < len(elev.floor_mng):
            k = k + 1
        while k + 1 < len(elev.floor_mng):
            if call.dst == elev.floor_mng[k + 1]:
                end_t = delay + elev.times[k + 1]
                call_t = end_t - call.call_time
                return call_t, end_t, delay, k + 1
            if call.dst < elev.floor_mng[k + 1]:
                k = k + 1
            elif call.dst > elev.floor_mng[k + 1]:
                k = k - 1
                break
        #q. is this good?
        end_t = elev.times[k] + math.ceil(
            close_t + start_t + (abs(elev.floor_mng[k] - call.dst)) / speed + stop_t + open_t + delay)
        call_t = end_t - call.call_time
        return call_t, end_t, delay, k + 1

def calc_time_3(call: CallForElevator, elev: Elevator, k, tmp_on_board):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    start_t = elev.start_time
    stop_t = elev.stop_time
    delay = tmp_on_board - elev.times[k]
    #If the call direction is down as well
    if call.dir == -1:
        while k + 1 < len(elev.floor_mng):
            # If there is a stop on the destination floor already
            if elev.floor_mng[k + 1] == call.dst:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + stop_t + open_t)
                return end_t - call.call_time, end_t, end_t - elev.times[k + 1], k
            # If the current destination is closer then the next existing destination of the elevator
            if call.dst > elev.floor_mng[k + 1]:
                end_t = math.ceil(
                    tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
                call_t = end_t - call.call_time
                delay = end_t + math.ceil(
                    close_t + start_t + (abs(call.dst - elev.floor_mng[k + 1])) + stop_t + open_t) - elev.times[k + 1]
                if delay < 0:
                    delay = 0
                return call_t, end_t, delay, k
            # if the exxisting destination is lower than the current call destination go to the next call destination
            if call.dst < elev.floor_mng[k + 1]:
                k = k + 1
                continue;
                # q. Is it good?
            end_t = elev.times[k] + math.ceil(
                close_t + start_t + (abs(elev.floor_mng[k] - call.dst)) / speed + stop_t + open_t + delay)
            call_t = end_t - call.call_time
            return call_t, end_t, delay, k + 1
        else:
            end_t = math.ceil(tmp_on_board + close_t + start_t + (abs(call.src - call.dst)) / speed + open_t + stop_t)
            call_t = end_t - call.call_time
            return call_t, end_t, 0, k
        # If the call direction is in the opposite direction
        if call.dir == 1:
            while elev.floor_mng[k + 1] < elev.floor_mng[k] and k + 1 < len(elev.floor_mng):
                k = k + 1
            while k + 1 < len(elev.floor_mng):
                if call.dst == elev.floor_mng[k + 1]:
                    end_t = delay + elev.times[k + 1]
                    call_t = end_t - call.call_time
                    return call_t, end_t, delay, k + 1
                if call.dst > elev.floor_mng[k + 1]:
                    k = k + 1
                elif call.dst < elev.floor_mng[k + 1]:
                    k = k - 1
                    break
            # q. is this good?
            end_t = elev.times[k] + math.ceil(
                close_t + start_t + (abs(elev.floor_mng[k] - call.dst)) / speed + stop_t + open_t + delay)
            call_t = end_t - call.call_time
            return call_t, end_t, delay, k + 1


def check_call_time_0(call: CallForElevator, elev: Elevator):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    start_t = elev.start_time
    stop_t = elev.stop_time
    src_t = 0
    dst_t = 0
    call_t = 0
    if elev.is_empty():
        if call.src == 0:
            src_t = math.ceil(call.call_time)
            dst_t = math.ceil(close_t + start_t + (abs(call.dst)) / speed + stop_t + open_t)
            call_t = dst_t - call.call_time
            return src_t, dst_t, call_t


def can_the_elevator_stop(call: CallForElevator, elev: Elevator, idx):
    speed = elev.speed
    open_t = elev.open_time
    close_t = elev.close_time
    start_t = elev.start_time
    stop_t = elev.stop_time
    return math.floor(
        close_t + start_t + (abs(elev.floor_mng[idx] - call.src)) / speed + stop_t + open_t) < call.call_time


# def time_check(call: CallForElevator, elev: Elevator):
#     if not elev.calls:
#         if call.src == 0:
#             return call.call_time
#         return call.call_time + elev.close_time + elev.start_time + (
#             abs(0 - call.src)) / elev.speed + elev.stop_time + elev.open_time
#     else:
#         if elev.calls[-1].data[8] > call.call_time:
#             return elev.calls[-1].data[8] + elev.close_time + elev.start_time + (
#                 abs(elev.calls[-1].data[3] - call.src)) / elev.speed + elev.stop_time + elev.open_time
#         else:
#             if elev.calls[-1].data[3] == call.src:
#                 return call.call_time
#             return call.call_time + elev.close_time + elev.start_time + (
#                 abs(elev.calls[-1].data[3] - call.src)) / elev.speed + elev.stop_time + elev.open_time
#
#
# def call_time(call: CallForElevator, elev: Elevator):
#     return elev.close_time + elev.start_time + (abs(call.dst - call.src)) / elev.speed + elev.stop_time + elev.open_time


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
    ex1('data\\Ex1_input\\Ex1_Buildings\\B5.json', 'data\\Ex1_input\\Ex1_calls\\Calls_a.csv', 'out.csv')
