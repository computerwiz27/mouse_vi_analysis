import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math

file: str
data: pd.DataFrame
active_sens: str

left_poke_events = ['Left', 'LeftShort', 'LeftWithPellet', 'LeftinTimeout', 'LeftDuringDispense']
right_poke_events = ['Right', 'RightShort', 'RightWithPellet', 'RightinTimeout', 'RightDuringDispense']
poke_events = left_poke_events + right_poke_events
pellet_events = ['Pellet', 'LeftWithPellet', 'RightWithPellet']

def get_wrong_pokes() -> int:
    wrong_pokes = 0
    for event in data['Event']:
        if active_sens == 'Left' and event in right_poke_events:
            wrong_pokes += 1
        if active_sens == 'Right' and event in left_poke_events:
            wrong_pokes += 1

    print('Wrong pokes:', wrong_pokes)
    return wrong_pokes

def get_impulsive_pokes() -> int:
    impulsive_pokes = 0
    count_down_active = False
    for i, row in data.iterrows():
        if row['Event'] == 'Set VI':
            count_down_active = True
        if count_down_active:
            if row['Event'] in left_poke_events and active_sens == 'Left':
                impulsive_pokes += 1
            if row['Event'] in right_poke_events and active_sens == 'Right':
                impulsive_pokes += 1
        if row['Event'] in pellet_events:
            count_down_active = False

    print('Impulsive pokes:', impulsive_pokes)
    return impulsive_pokes

def get_avg_retrieval_t() -> int:
    retrievals = 0
    retrieval_t_avg = 0
    for retrieval_t in data['Retrieval_Time']:
        try:
            retrieval_t = float(retrieval_t)
        except:
            continue
        if math.isnan(retrieval_t): continue
        if retrieval_t < 0.2: continue

        retrieval_t_avg += retrieval_t
        retrievals += 1
    if retrievals > 0:
        retrieval_t_avg = retrieval_t_avg / retrievals

    print('Average retrieval time:', retrieval_t_avg, 's')
    return retrieval_t_avg


def get_activity_graph() -> None:
    datetime_format = '%m/%d/%Y %H:%M:%S'
    time_bucket_start = datetime.strptime(data['MM:DD:YYYY hh:mm:ss'][0], datetime_format)
    time_bucket_start_srt = str(time_bucket_start.hour) + ':' + str(time_bucket_start.minute)
    time_step = timedelta(minutes=10)
    buckets = {time_bucket_start_srt: []}
    for i, row in data.iterrows():
        event_datetime = datetime.strptime(row['MM:DD:YYYY hh:mm:ss'], datetime_format)
        if event_datetime < time_bucket_start + time_step:
            if row['Event'] in poke_events:
                buckets[time_bucket_start_srt].append(row['Event'])
            else:
                time_bucket_start = time_bucket_start + time_step
                time_bucket_start_srt = str(time_bucket_start.hour) + ':' + str(time_bucket_start.minute)
                buckets[time_bucket_start_srt] = []
                if row['Event'] in poke_events:
                    buckets[time_bucket_start_srt].append(row['Event'])

    event_freq = []
    for bucket in buckets:
        event_freq.append(len(buckets[bucket]))

    plt.bar(buckets.keys(), event_freq)
    plt.show()

def init():
    global data 
    global active_sens
    data = pd.read_csv(file)
    active_sens = data['Active_Poke'][0]

def run_analysis():
    global data 
    global active_sens
    data = pd.read_csv(file)
    active_sens = data['Active_Poke'][0]

    get_wrong_pokes()
    get_impulsive_pokes()
    get_avg_retrieval_t()
    get_activity_graph()