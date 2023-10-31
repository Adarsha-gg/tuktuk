import json
import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
# open the data file
with open("user_data.json","r",encoding="utf8") as f:
    data = json.load(f)

def date_formatter(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    year = date_obj.strftime("%Y")
    month = calendar.month_name[int(date_obj.strftime("%m"))]
    day = date_obj.strftime("%d")
    return f"{month} {day}, {year}"

i = 0 # counter 
time = [] # intialize a list to store time values
frequencies = {}  # to count total number of occurance of a num
Access = (data["Activity"]["Login History"]["LoginHistoryList"])
# format:[2023-10-22 16:23:02 UTC] we only need date so we split
first_date = date_formatter(Access[-1]["Date"].split()[0])
last_date = date_formatter(Access[0]["Date"].split()[0])

for items in Access:
    # store only the relevant date data to time list
    opened_time = ((int(Access[i]["Date"].split()[1][0:2]) +7) % 24)+1
    time.append(opened_time)
    i+=1

time.sort()
for item in time:
    if item in frequencies:
        frequencies[item] +=1
    else:
        frequencies[item] = 00

chart_data = pd.DataFrame({
    "Time in NPT": frequencies.keys(),
    "Opened": frequencies.values()
    
})

st.title(f"You opened tiktok {i} amount of times from {first_date} to {last_date}")
st.bar_chart(chart_data, x="Time in NPT", y="Opened",)