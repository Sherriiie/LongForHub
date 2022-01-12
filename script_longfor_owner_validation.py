# coding:utf8
import sys
import json

# import xlrd
import re
import os
import sys
import uuid
import json
from TextSimilarity import StringSimilarity
import numpy as np
import codecs
import collections
import hashlib
# import xlrd
from sklearn import metrics
import click

'''
Process:
    step 1 extract data in from excel and write into tsv file
    step 2 expand regex    
    step 3 write knowledge into file    
    step 4 get the knowledge schema and all entities.
'''

invalid_room_number = []
valid_room_number = []
invalid_room_number_verified = []
valid_room_number_verified = []

def extract_room_no(string):
    try:
        string = string.strip().replace("~", "-").replace("－", "-").replace("—", "-")\
            .replace("一", "-").replace("–", "-").replace("_", "-").replace("～", "-")
        # string = "史迪仔3-1-403"
        p1 = re.compile(r"\d-\d-[0-9]+")
        matcher1 = re.search(p1, string)
        if not matcher1 and "4-" in string:
            # Building #4
            p1 = re.compile(r"\d-[0-9]+")
            matcher1 = re.search(p1, string)
            assert string[matcher1.start(): matcher1.end()].startswith("4-")
        test = string[matcher1.start(): matcher1.end()]
    except:
        print("Error room No:", string)
        return "Error room No"
        # exit()
    return test

def validate_room_no(room_no):
    room_no_ori = room_no
    room_no = room_no.split("-")
    if len(room_no) == 2:
        # building #4
        if room_no[0] not in ["4"]:
            print("Invalid room NO. {}".format(room_no_ori))
            return False
    else:
        if len(room_no) != 3:
            print("Invalid room NO. {}".format(room_no_ori))
            return False
        if room_no[0] not in ["1", "2", "3", "4", "5"]:
            print("Invalid room NO. {}".format(room_no_ori))
            return False
        if room_no[1] not in ["1", "2"]:
            print("Invalid room NO. {}".format(room_no_ori))
            return False

    return True

def improve_name_for_building4(names):
    new_names = []
    for name in names:
        parts = name.split("-")
        if parts[0] == "4" and len(parts) == 3:
            name = "-".join([parts[0], parts[2]])
        new_names.append(name)

    return new_names

if __name__ == '__main__':
    # all_member = "4-703,1-1-1203 猪猪宝,1-2-1103,3-2-603,牛牛牛~3-1-1601,1-1-603 halyang,5-1-1703,梅梅3-2-1303,陈小陈5-1-1703,1-1-1203 猪猪宝,5-1-203,3-2-16,S. 5-2-1103,史迪仔3-1-403"
    # all_member = all_member.split(",")

    date = "0105"
    f = open("E:\\download\\LongForMembersAll-{}.txt".format(date), encoding="utf-8").readlines()
    all_member = f[0].split(",")
    for mem in all_member:
        room_no = extract_room_no(mem)
        if room_no == "Error room No":
            invalid_room_number.append(mem)
            continue
        if validate_room_no(room_no):
            valid_room_number.append(room_no)
        else:
            invalid_room_number.append(room_no)

    valid_room_number = list(set(valid_room_number))
    print("\n{} valid room No.".format(len(valid_room_number)))
    print(valid_room_number)
    print("{} invalid room No.".format(len(invalid_room_number)))
    print(invalid_room_number)
    print("\n" + "*"*40 + "\n")

####################### 没有做业主验证的
    print("Begin to process customer verification...")
    # all_member_verified = "1. blueblue 1-1-1503   已发,2. 5-2-1503 已发,3. 刘川疯 5-2-902 已发,4. 1-2-1301 屁美 和PP一家,5. 1-1-602 已发,6. 5-1-301 已发 和LC一家,7. 1-1-1303  已发 俩人,8. 1-1-502已发和1-1-502段是一家"
    # all_member_verified = all_member_verified.split(",")

    f = open("E:\\download\\LongForMembersVerified-{}.txt".format(date), encoding="utf-8").readlines()
    all_member_verified = f[0].split(",")

    for mem in all_member_verified:
        room_no = extract_room_no(mem)
        if room_no == "Error room No":
            invalid_room_number_verified.append(mem)
            continue
        if validate_room_no(room_no):
            valid_room_number_verified.append(room_no)
        else:
            invalid_room_number_verified.append(room_no)

    valid_room_number_verified = list(set(valid_room_number_verified))
    print("\n{} valid room No. of verified customer".format(len(valid_room_number_verified)))
    print(valid_room_number_verified)
    print("\n{} invalid room No. of verified customer".format(len(invalid_room_number_verified)))
    print(invalid_room_number_verified)

    print("\n" + "*" * 40 + "\n")
    # get the customers who are not verified.
    # improve building #4 name
    valid_room_number = improve_name_for_building4(valid_room_number)
    valid_room_number_verified = improve_name_for_building4(valid_room_number_verified)
    not_verified_customer = set(valid_room_number).difference(set(valid_room_number_verified))
    not_verified_customer = list(not_verified_customer)
    print("{} room No. not verified.".format(len(not_verified_customer)))
    print(", ".join(sorted(not_verified_customer)))







