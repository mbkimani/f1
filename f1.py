import pandas as pd
import numpy as np
import requests
import random

import fastf1 as ff1
from fastf1.plotting import team_color
import seaborn as sns
import matplotlib.pyplot as plt

#define a function that calls the api and returns the response 
def retrieve_ergast_data(apiendpoint:str):
    url = f'https://ergast.com/api/f1/{apiendpoint}.json'
    response = requests.get(url).json()
    return response

#get number of rounds for the specific season
race = retrieve_ergast_data(f'2021/driverStandings')

rounds = int(race['MRData']['StandingsTable']['StandingsLists'][0]['round'])

#initialize a dataFrame to store our data
championship_standings = pd.DataFrame()

team_driver_mapping = {}

#loop through the season's rounds
for i in range(1,rounds+1):
    current_race = retrieve_ergast_data(f'2021/{i}/driverStandings')

#get current standings
    current_standings = current_race['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

#inititate current round standings dict
    current_round = {'round':i}

    #get the drivers, their codes and their positions
    for i in range(len(current_standings)):
        driver = current_standings[i]['Driver']['code']
        position = current_standings[i]['position']

        current_round[driver] = int(position)

        #team_driver_map for color coding teams

        team_driver_mapping[driver] = current_standings[i]['Constructors'][0]['name']

    #append round to championship standings
    championship_standings = championship_standings.append(current_round, ignore_index=True)

    #index round
championship_standings= championship_standings.set_index('round')

#melt the dataframe along the 'round' column

championship_standings_melted = pd.melt(championship_standings.reset_index(), 'round')

#print(championship_standings_melted)
sns.set(rc={'figure.figsize':(11.7, 8.27)})

fig, ax =  plt.subplots()



for driver in pd.unique(championship_standings_melted['variable']):
    sns.lineplot (
    x='round',
    y='value',
    data= championship_standings_melted.loc[championship_standings_melted['variable']==driver],
    color=team_color(team_driver_mapping[driver])
)

ax.set_title('2021 Final Championship Standings')

ax.invert_yaxis()
ax.set_xticks(range(1,rounds))
ax.set_yticks(range(1,22))

ax.set_xlabel('Round')
ax.set_ylabel('Championship Position')
ax.grid(False)

for line, name in zip(ax.lines, championship_standings.columns.tolist()):
    y= line.get_ydata()[-1]
    x= line.get_xdata()[-1]

    text = ax.annotate(
        name,
        xy=(x,y),
        xytext=(0,0),
        xycoords=(
            ax.get_xaxis_transform(),
            ax.get_yaxis_transform()    
        ),
        textcoords="offset points"
    )


plt.savefig('E:/Projects/Erghast/f1/championship_results_2021.png')
#print(pd.unique(championship_standings_melted['variable']))
#print(championship_standings_melted.loc[championship_standings_melted['variable']=='HAM'])