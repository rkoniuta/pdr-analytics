# Sales by time interval (9, 10, 11, 12), stacked with mean order, order volume
# Sales by day (M T W R F Sa Su), stacked with mean order, order volume
# Sales by 
# Sales by month ()
# Sales by user, unique transactions, repeat customers
# Sales by user 
# Most common note

# August 31st to November 29th 2021

# read in CSV
# convert date to human readable
# maintain dictionary for months, days, hours
# plot as a bar graph

import datetime
import calendar
import collections
import matplotlib.pyplot as plt
import numpy as np


def plot(d: dict, xlabel: str, title: str) -> None:
    X = list(d.keys())
    X_axis = np.arange(len(X))

    total_value = [ d[key]["total_value"] for key in d.keys() ]
    total_transactions = [ d[key]["total_transactions"] for key in d.keys() ]
    avg_value = [ d[key]["avg_value"] for key in d.keys() ] # this is unreadable

    plt.bar(X_axis - 0.3, total_value, 0.3, label='revenue ($)')
    plt.bar(X_axis + 0.0, total_transactions, 0.3, label='transactions')
    plt.bar(X_axis + 0.3, avg_value, 0.3, label='avg transaction (¢)')

    plt.xticks(X_axis, X)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.legend()
    plt.show()

def calc_mean(d: dict) -> None:
    for key in d.keys():
        d[key]["avg_value"] = d[key]["total_value"] / d[key]["total_transactions"] * 100


with open("venmo.txt", "r") as f:
    lines = f.readlines()

fields = {
    "id": 0,
    "timestamp": 1,
    "note": 4,
    "value": 7,
}

months = collections.defaultdict(lambda: {"total_value": 0, "total_transactions": 0})
days = collections.defaultdict(lambda: {"total_value": 0, "total_transactions": 0})
hours = collections.defaultdict(lambda: {"total_value": 0, "total_transactions": 0})
users = collections.defaultdict(lambda: {"total_value": 0, "total_transactions": 0})

for line in lines:
    entry = {
        key: val
        for key, val in zip(fields.keys(), [val for i, val in enumerate(line.split(',')[1:]) if i in list(fields.values())])
    } # this will break on note commas, just manually remove

    value = float(entry["value"].strip()[1:])
    timestamp = datetime.datetime.fromisoformat(entry["timestamp"])
    month = calendar.month_name[timestamp.month]
    day_of_week = calendar.day_name[(timestamp.weekday()-1)%7] # because timezone
    hour = (timestamp.hour - 4)%12 # timezone UTC
    hour = f"{hour if hour != 0 else 12}pm"

    months[month]["total_value"] += value
    months[month]["total_transactions"] += 1

    days[day_of_week]["total_value"] += value
    days[day_of_week]["total_transactions"] += 1

    hours[hour]["total_value"] += value
    hours[hour]["total_transactions"] += 1

    users[entry["id"]]["total_value"] += value
    users[entry["id"]]["total_transactions"] += 1

calc_mean(months)
calc_mean(days)
calc_mean(hours)

plot(months, "Months", "Sales by month")
plot(days, "Days", "Sales by day")
plot(hours, "Hours", "Sales by hour")
