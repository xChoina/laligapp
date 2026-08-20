from curl_cffi import requests
import sqlite3


def fetch_teams_sofascore():
    print("Zakładamy maskę na poziomie szyfrowania (curl_cffi). Uderzamy w Sofascore...")

    # Nagłówki wciąż są potrzebne
    headers = {
        "Origin": "https://www.sofascore.com",
        "Referer": "https://www.sofascore.com/"
    }

    # 1. Pobieramy listę sezonów La Ligi (ID 8)
    seasons_url = "https://api.sofascore.com/api/v1/unique-tournament/8/seasons"

    # MAGIA DZIEJE SIĘ TUTAJ: impersonate="chrome"
    res_seasons = requests.get(seasons_url, headers=headers, impersonate="chrome")

    if res_seasons.status_code != 200:
        print(f"Błąd! Sofascore wciąż nas blokuje. Kod: {res_seasons.status_code}")
        return

    latest_season_id = res_seasons.json()['seasons'][0]['id']
    print(f"Złamałem zabezpieczenia! ID najnowszego sezonu to: {latest_season_id}")

    # 2. Uderzamy po tabelę ligową
    standings_url = f"https://api.sofascore.com/api/v1/unique-tournament/8/season/{latest_season_id}/standings/total"
    res_standings = requests.get(standings_url, headers=headers, impersonate="chrome")

    data = res_standings.json()

    conn = sqlite3.connect('laliga.db')
    cursor = conn.cursor()
    teams_added = 0

    for row in data['standings'][0]['rows']:
        team = row['team']

        team_id = team['id']
        name = team['name']
        short_name = team.get('shortName', name[:3].upper())
        stadium = 'Brak danych'
        founded = 0

        cursor.execute('''
        INSERT OR REPLACE INTO teams (team_id, name, short_name, stadium, founded) 
        VALUES (?,?,?,?,?)''', (team_id, name, short_name, stadium, founded))

        teams_added += 1
        print(f"Zapisano w bazie: {name} (ID: {team_id})")

    conn.commit()
    conn.close()
    print(f"\nSukces! Zapisano {teams_added} drużyn. Sofascore pokonane.")


if __name__ == '__main__':
    fetch_teams_sofascore()