import itertools
from typing import final
from gazpacho import get, Soup
import pandas as pd
import itertools


# Initialize URL and parse html
url = "https://scores.nbcsports.com/epl/standings.asp"
html = get(url)

soup = Soup(html)
div = soup.find('div', {'id': 'shsIFBStandings'})

#Initialize dataframe columns used later
cols = ['Team',
        'Games Played',
        'Wins',
        'Draws',
        'Losses',
        'Goals Forced',
        'Goals Allowed',
        'Goal Difference',
        #'Home Record',
        #'Away Record',
        'Points']

def main():
    standing = div.find('td', {'class': 'shsNumD'})
    standingsList = []
    #print(standingEven)
    for i in standing:
        standResult = i.text
        standingsList.append(standResult)

    # Cleaning up standingsList
    k = 10

    standingsList = standingsList[k: ]
    # print(standingsList)

    gamesPlayed = standingsList[0::10]
    wins = standingsList[1::10]
    draws = standingsList[2::10]
    losses = standingsList[3::10]
    goalsForced = standingsList[4::10]
    goalsAllowed = standingsList[5::10]
    goalDifference = standingsList[6::10]
    # homeRecord = standingsList[7::10]
    # awayRecord = standingsList[8::10]
    points = standingsList[9::10]

    # Grab team names (have to pull even and odd since they have different classes)
    teamEven = div.find('tr', {'class': 'shsRow0Row'})
    teamEvenList = []
    for i in teamEven:
        evenResult = i.text
        teamEvenList.append(evenResult)

    # print(teamEvenList)

    teamOdd = div.find('tr', {'class': 'shsRow1Row'})
    teamOddList = []
    for i in teamOdd:
        oddResult = i.text
        teamOddList.append(oddResult)

    # print(teamOddList)

    # Merge two lists while keeping original indices
    finalStandings = [item for sublist in zip(teamEvenList, teamOddList) for item in sublist]

    # print(finalStandings)

    df = pd.DataFrame(list(zip(finalStandings, gamesPlayed, wins, draws, losses, goalsForced, goalsAllowed, goalDifference, points)), 
                    columns = cols)

    df = df.set_index('Team')
    print(df)
    output = df.to_csv()

    with open ('eplFullStandings.csv', 'w+') as of:
        of.write(output)
    print("Complete!")


if __name__ == "__main__":
    main()
