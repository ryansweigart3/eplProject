import itertools
from datetime import date
from typing import final
from gazpacho import get, Soup
import pandas as pd
import itertools
import psycopg2

datetime = date.today()
timestamp = datetime.strftime("%d%m%y")

# initialize database
conn = psycopg2.connect(
    database='test_db',
    user='root',
    password='root',
    host='0.0.0.0'
)


# sql2 = '''COPY standings(team,games_played,wins,draws,\
#     losses,goals_forced,goals_allowed,goal_difference,points)
# FROM '/Desktop/eplScrape/eplFullStandings.csv'
# DELIMITER ','
# CSV HEADER;'''

# cur.execute(sql2)

# try:
#     cur.execute('CREATE TABLE standings (team char, games_played char, wins char, draws char, losses char, goals_forced char, goals_allowed char, goal_difference char, points char);')
# except:
#     print('Cannot create table')





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


# # Helper function to find team data
# def findTeam(favTeam, df):
#     for index, value in df.iterrows():
#         if index == favTeam:
#             print(f"Here are the stats for {favTeam} this year: \n")
#             print(value)

# # Helper functions for user input
# def scheduleChoice(favTeam, gameDf):
#     for index, value in gameDf.iterrows():
#         if index == favTeam:
#             print(f"{favTeam}'s next game is:  \n")
#             print(value)

def main():
    print('*** Beginning web scrape of NBC Sports to get most up-to-date EPL Standings ***')
    # favTeam = input("Please enter your favorite EPL team: ")
    # gameChoice = input("Would you like to view your team's stats or next match? (Enter 1 for stats or 2 for next match): \n")
    # print("Favorite EPL team is: " + favTeam)

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

    teamOdd = div.find('tr', {'class': 'shsRow1Row'})
    teamOddList = []
    for i in teamOdd:
        oddResult = i.text
        teamOddList.append(oddResult)

    # Merge two lists while keeping original indices
    finalStandings = [item for sublist in zip(teamEvenList, teamOddList) for item in sublist]

    df = pd.DataFrame(list(zip(finalStandings, gamesPlayed, wins, draws, losses, goalsForced, goalsAllowed, goalDifference, points)), 
                    columns = cols)

    
    # df['id'] = range(1, len(df) + 1)
    df = df.set_index('team')
    print(df.dtypes)
    output = df.to_csv()

    # scheduleChoice(favTeam, gameChoice, gameDf)

    with open ('eplFullStandings' + timestamp + '.csv', 'w+') as of:
        of.write(output)
        of.close()
    
    cur = conn.cursor()

    
    cur.execute('CREATE TABLE standings (team char(100), games_played char(100), wins char(100), draws char(100), losses char(100), goals_forced char(100), goals_allowed char(100), goal_difference char(100), points char(100));')


    with open('eplFullStandings' + timestamp + '.csv', 'r') as f:    
        # Notice that we don't need the `csv` module.
        next(f) # Skip the header row.
        cur.copy_from(f, 'standings', sep=',')
    
    conn.commit()
    conn.close()
    cur.close()
    
    print("That's it! Scrape is complete!")


    

if __name__ == "__main__":
    main()
