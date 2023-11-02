import json
import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
from collections import Counter

# uploader
upload = st.file_uploader("Upload your data")

# open the data file
if upload is not None:
    
    data = json.load(upload)

    #convert dates like 2020-2-3 to 2023 feb 3 
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

    time.sort() # easier to plot once its sorted

    # get times opened in a single hour
    for item in time:
        if item in frequencies:
            frequencies[item] +=1
        else:
            frequencies[item] = 0

    #plot it
    chart_data = pd.DataFrame({
        "Time in NPT": frequencies.keys(),
        "Opened": frequencies.values()
        
    })

    st.title(f"You opened tiktok {i} amount of times from {first_date} to {last_date}")
    st.bar_chart(chart_data, x="Time in NPT", y="Opened",)


    # for total number of videos
    Video = data["Activity"]["Video Browsing History"]["VideoList"]
    total_videos = len(Video)

    #calculate approximate screentime
    total_time = int((total_videos * 15)/60)    
    total_hours = int(total_time/60)

    st.caption(f"You watched over {total_videos} videos in just 3 months. Get A LIFE!!!\
            You might say 'WeLl I DoNt WaTcH A LoT I JuSt ScRoLl'. Even if you watch 15 seconds of a video\
                on avg that {total_time} minutes which is {total_hours} hours " )


    #for total number of shared videos
    shared = data["Activity"]["Share History"]["ShareHistoryList"]
    total_shared = len(shared)

    st.caption(f"You sent {total_shared} videos to others")


    # total comments
    comments = data["Comment"]["Comments"]["CommentsList"]
    total_comments = len(comments)
    st.caption(f"You commented on total of {total_comments} videos")


    # for top 3 people you text
    chats =data ["Direct Messages"]["Chat History"]["ChatHistory"]
    all_people = list(chats.keys())

    total_texts = {}

    for items in all_people:
        total_texts[items] = int(len(chats[items]))

    highest = Counter(total_texts) # counter uses dictionary to sort it by value
    top_three = highest.most_common(3) # return the highest 3 values
    names = [] 
    texts = []

    #to get only the names of top three people
    st.caption(f"Your top 3 frns are :")
    for j in range(0,3):
        names.append(top_three[j][0][18:-1])
        texts.append(top_three[j][1])
        st.caption(f"{names[j]} with {texts[j]} texts")

