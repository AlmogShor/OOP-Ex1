import csv , json  # This is a sample Python script.


from Building import Building
from Elevator import Elevator
from CallForElevator import CallForElevator


def allocate(callList : CallForElevator, B : Building, output):
    out_file = open("out.csv", "w", newline="")
    writer = csv.writer(out_file)
    mission=0
    onboard=0
    endtime=0
    bestelv=-1
    boazidiot=B.list_elvators[0].id

    for i in callList:
        chosenElev = -1
        minTime = 1500

        if(i.src<B.minFloor or i.src>B.maxFloor or i.dst<B.minFloor or i.dst>B.maxFloor):
            i.data[5]=-1
            writer.writerow(i.data)
            continue

        for j in B.list_elvators:



            if(timecheck(i,j)<minTime):
                bestelv=j.id
                minTime=timecheck(i,j)
                onboard=minTime
                endtime=minTime+calltime(i, j)

        i.data[5]=bestelv
        i.data[7]=onboard
        i.data[8]=endtime
        B.list_elvators[bestelv-boazidiot].calls.append(i)
        writer.writerow(i.data)
    out_file.close()


def timecheck(call : CallForElevator,elev : Elevator):
    if(elev.calls):
        if (elev.calls[-1].data[8] > call.callTime):
            return elev.calls[-1].data[8]+elev.closeTime+elev.startTime+(abs(elev.calls[-1].data[3]-call.src))/elev.speed+elev.stopTime+elev.openTime
        else:
            if(elev.calls[-1].data[3]==call.src):
                return call.callTime
            return call.callTime+elev.closeTime+elev.startTime+(abs(elev.calls[-1].data[3]-call.src))/elev.speed+elev.stopTime+elev.openTime
    else:
        if(call.src==0):
            return call.callTime
        return call.callTime+elev.closeTime+elev.startTime+(abs(0-call.src))/elev.speed+elev.stopTime+elev.openTime

def calltime(call : CallForElevator, elev : Elevator):
    return elev.closeTime + elev.startTime + (abs(call.dst - call.src)) / elev.speed + elev.stopTime + elev.openTime


def Ex1(bld , calls , output):
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
    #Closing the json file
    f.close()
    # Opening CSV file
    c = open(calls)
    csvreader = csv.reader(c)
    #Creating the callForElevators objects
    idx = 0
    callsList =[]
    for row in csvreader:
        call = CallForElevator(row[1], row[2], row[3], idx)
        idx = +1
        callsList.append(call)

    allocate(callsList, B, output)
    #Closing the CSV file
    c.close()


if __name__ == '__main__':
    Ex1('data\\Ex1_input\\Ex1_Buildings\\B3.json', 'data\\Ex1_input\\Ex1_calls\\Calls_a.csv', 'out.csv')