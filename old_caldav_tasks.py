#!/usr/bin/env python3
""" check for old caldav tasks """

import os
import datetime

def completed(data):
    """ check if task is completed"""
    status = ""
    for line in data:
        if "STATUS:" in line:
            status = line
            break
    if status == "STATUS:NEEDS-ACTION\n":
        return False
    return True

def older_than_days(data,days):
    """ check if task is older than days"""
    time_line = ""
    for line in data:
        if "CREATED" in line:
            time_line = line
            break
    date = time_line.split(":")[-1]
    date = date[:8]
    date_time_obj = datetime.datetime.strptime(date,'%Y%m%d')
    date_now = datetime.datetime.now()
    delta = date_time_obj + datetime.timedelta(days = days)

    return bool(delta < date_now)

def get_summary(task):
    """ get summary of task"""
    summary = ""
    for line in task:
        if "SUMMARY" in line:
            summary = line[8:]
            break
    return summary

def main():
    """ read all tasks in dir
        * look for uncompleted tasks
        * check if they are older than 'days'
        * output summary old tasks
    """

    #path to caldav tasks dir
    path = ""
    days = 50

    tasks = os.listdir(path)

    candidates= 0
    output = ""

    for task_file in tasks:
        if "caldavsyncadapter" in task_file:
            continue
        with open(path+task_file, "r") as task:
            data = task.readlines()
            if not completed(data):
                if older_than_days(data,days):
                    candidates += 1
                    output += "* "+get_summary(data)
            task.close()

    if candidates > 0:
        print("The following %s tasks are older than %s days:" \
                % (candidates, days))
        print(output)

if __name__ == "__main__":
    main()
