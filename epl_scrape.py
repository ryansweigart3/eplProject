from datetime import date
from typing import final
from gazpacho import get, Soup
import pandas as pd
import itertools
import psycopg2

# initialize date
datetime = date.today()
timestamp = datetime.strftime("%d%m%y")

# initialize database
conn = psycopg2.connect(
    database='test_db',
    user='****',
    password='**********',
    host='0.0.0.0'
)

# Initialize URL and parse html
url = "https://scores.nbcsports.com/epl/standings.asp"
html = get(url)

soup = Soup(html)
div = soup.find('div', {'id': 'shsIFBStandings'})

#Initialize dataframe columns used later
cols = [
        'team',
        'games_played',
        'wins',
        'draws',
        'losses',
        'goals_forced',
        'goals_allowed',
        'goal_difference',
        'points']

# Function scrapes NBC sports to gather
# current EPL table and imports into pgsql db
def main():
    print('*** Beginning web scrape of NBC Sports to get most up-to-date EPL Standings ***')

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
    points = standingsList[9::10]

    # Grab team names (have to pull even and odd since they have different classes)
    teamEven = div.find('tr', {'class': 'shsRow0Row'})
    teamEvenList = []
    for i in teamEven:
        evenResult = i.text
        teamEvenList.append(evenResult)

    teamOdd = div.find('tr', {'class': 'shsRow1Row'})
    teamOddList = []
    for i in teamOdd:
        oddResult = i.text
        teamOddList.append(oddResult)

    # Merge two lists while keeping original indices
    finalStandings = [item for sublist in zip(teamEvenList, teamOddList) for item in sublist]

    df = pd.DataFrame(list(zip(finalStandings, gamesPlayed, wins, draws, losses, goalsForced, goalsAllowed, goalDifference, points)), 
                    columns = cols)

   
    # reset index    
    df = df.set_index('team')
    print(df.dtypes)
    output = df.to_csv()
    

    with open ('eplFullStandings' + timestamp + '.csv', 'w+') as of:
        of.write(output)
        of.close()
    
    cur = conn.cursor()

    # create table
    cur.execute('CREATE TABLE standings (team char(100), games_played char(100), wins char(100), draws char(100), losses char(100), goals_forced char(100), goals_allowed char(100), goal_difference char(100), points char(100));')

    # add df to database
    with open('eplFullStandings' + timestamp + '.csv', 'r') as f:    
        next(f) # Skip the header row.
        cur.copy_from(f, 'standings', sep=',')
    
    conn.commit()
    conn.close()
    cur.close()
    
    print("That's it! Scrape is complete!")
    

if __name__ == "__main__":
    main()
