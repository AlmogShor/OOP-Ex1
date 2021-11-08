import json, csv

def Ex1(bld , calls , output):
    # Opening JSON file
    f = open(bld, "r")

    #Opening CSV file
    clls = open(calls,"r")

    #Opening CSV file
    outpt = open(output, "r+w")

    # returns JSON object as
    # a dictionary
    # data = json.load(

