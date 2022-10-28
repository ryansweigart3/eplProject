from gazpacho import get, Soup
import pandas as pd


# Initialize URL and parse html
url = "https://scores.nbcsports.com/epl/scoreboard_daily.asp"
html = get(url)

soup = Soup(html)
div = soup.find('div', {'class': 'shsScoreboardDaily'})

cols = [
    'Home',
    'Away',
    'Kickoff Time (All times Pacific)'
]
def main():
    matchInfoHome = div.find('td', {'class': 'shsNamD'})
    matchInfoAway = div.find('td', {'class': 'shsNumD'})
    matchListHome = []
    matchListAway = []

    for i in matchInfoHome:
        matchListHome.append(i.text)

    for i in matchInfoAway:
        matchListAway.append(i.text)

    matchInfoHome = matchListHome[2::3]
    matchInfoTime = matchListHome[1::3]
    matchInfoAway = matchListAway[1::2]

    df = pd.DataFrame(list(zip(matchInfoHome, matchInfoAway, matchInfoTime)), columns=cols)

    df = df.set_index('Home')

    output = df.to_csv()

    with open ('eplMatchweek.csv', 'w+') as of:
        of.write(output)



if __name__ == "__main__":
    main()
