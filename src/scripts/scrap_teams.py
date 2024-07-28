import requests
from bs4 import BeautifulSoup as bs
import re
from db.database import cursor, conn
from enums.player_position import Player_position


def insert_gk(team: str):
    response = requests.get(get_team_url(team))
    position = Player_position.GK.value

    if response.status_code == 200:
        goalkeepers = get_players(response)

        for gk in goalkeepers:
            gk_td = gk.find_all("td")
            name = (
                gk_td[1]
                .find("span", class_="personCardCell__name")
                .get_text(strip=True)
            )
            age_text = (
                gk_td[1]
                .find("span", class_="personCardCell__description")
                .get_text(strip=True)
            )
            age = (
                int(re.search(r"\d+", age_text).group())
                if re.search(r"\d+", age_text)
                else None
            )

            pj = 0 if gk_td[2].text.strip() == "-" else int(gk_td[2].text.strip())
            goals = 0 if gk_td[3].text.strip() == "-" else int(gk_td[3].text.strip())
            assist = 0 if gk_td[4].text.strip() == "-" else int(gk_td[4].text.strip())

            query_insert_player(position, name, age, pj, goals, assist)


def query_insert_player(position, name, age, pj, goals, assist):
    insert_query = """
            INSERT INTO players (name, age, pj, goal, assist, position)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
    cursor.execute(insert_query, (name, age, pj, goals, assist, position))
    conn.commit()


def get_players(response):
    soup = bs(response.text, "html.parser")
    table_goalkeeper = soup.find("table", id="squadTableGoalkeeper")
    data_goalkeepers = table_goalkeeper.find("tbody")
    goalkeepers = data_goalkeepers.find_all("tr")
    return goalkeepers


def get_team_url(team: str) -> str:
    return f"https://www.fichajes.com/equipo/{team}/plantilla/"
