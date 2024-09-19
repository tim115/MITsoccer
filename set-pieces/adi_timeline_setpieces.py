" Timeline of Setpieces "

### SNIPPET 484
#https://gitlab.ethz.ch/socceranalytics/uefa-euro-2020/-/snippets/484

# With the following code, we are trying to draw a timelines of the events that took place during the match
# We will do that using the data from wyscout.

import numpy as np
import json
import pprint

import pandas as pd

# We are loading the data from Wyscout
with open('../../data/wyscout/5111384/5111384_events.json', "r") as f:
    data_wyscout = json.load(f)

events_wyscout = data_wyscout['events']

# We spot the set pieces and put them in one dataframe. We also keep track of their timestamps
# We first create some lists to put all the detils in
n = len(events_wyscout)
country_total = []
setpieces_total = []
timestamps_total = []

setpieces = ['throw_in', 'goal_kick', 'free_kick', 'corner', 'penalty', 'penalty_kick']
countries = ['Austria', 'North Macedonia']
for i in range(n):
    if ((events_wyscout[i].get('team').get('name') in countries) and (events_wyscout[i].get('type').get('primary') in setpieces)):
        setpieces_total.append(events_wyscout[i].get('type').get('primary'))
        timestamps_total.append(events_wyscout[i].get('minute')) # We only keep the minute
        country_total.append(events_wyscout[i].get('team').get('name'))
    
# We store thw results in two dataframes
setpieces_df = pd.DataFrame(list(zip(timestamps_total, country_total, setpieces_total)),
                                     columns = ['Minute','Country', 'Setpiece Type'])

# We create the plots
import seaborn as sns
import matplotlib.pyplot as plt

print(setpieces_df)

sns.set_theme(style = "dark", font_scale= 2, color_codes=True)
sns.catplot(x="Minute", y="Country", hue="Setpiece Type", kind="swarm", data=setpieces_df, height = 6, aspect = 4, s = 12)
plt.show()
