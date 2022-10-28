from gazpacho import get, Soup
import pandas as pd


# Initialize URL and parse html
url = "https://scores.nbcsports.com/epl/scoreboard_daily.asp"
html = get(url)

soup = Soup(html)
div = soup.find('div', {'class': 'shsScoreboardDaily'})

# Create columns that will be used in the csv file
cols = [
    'Home',
    'Away',
    'Kickoff Time (All times Pacific)'
]

# Main function
def main():
    print('***Scraping NBC Sports for Matchweek Data***')
    # Parsing web html for appropriate classes. Need to create
    # one for home and one for away since they have differing
    # classes.
    matchInfoHome = div.find('td', {'class': 'shsNamD'})
    matchInfoAway = div.find('td', {'class': 'shsNumD'})
    matchListHome = []
    matchListAway = []

    # Loop through both lists and append just text to above lists.
    for i in matchInfoHome:
        matchListHome.append(i.text)

    for i in matchInfoAway:
        matchListAway.append(i.text)

    # Slicing lists to get data we want
    matchInfoHome = matchListHome[2::3]
    matchInfoTime = matchListHome[1::3]
    matchInfoAway = matchListAway[1::2]

    # Creating data frame and exporting to csv
    df = pd.DataFrame(list(zip(matchInfoHome, matchInfoAway, matchInfoTime)), columns=cols)

    df = df.set_index('Home')

    output = df.to_csv()

    with open ('eplMatchweek.csv', 'w+') as of:
        of.write(output)
    
    print('Scrapte complete!')


if __name__ == "__main__":
    main()
