from scripts.scrap_teams import insert_gk
from enums.team import Team

if __name__ == "__main__":
    for team in Team:
        insert_gk(team.value)
