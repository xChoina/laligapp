import sqlite3
def setup_database():
    # 1. Połączenie z bazą (plik laliga.db stworzy się sam)
    conn = sqlite3.connect('laliga.db')
    cursor = conn.cursor()

    # Włączenie relacji (kluczy obcych) w SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 2. Tabela KLUBÓW
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            name TEXT,
            short_name TEXT,
            stadium TEXT,
            founded INTEGER
        )
    ''')

    # 3. Tabela ZAWODNIKÓW (Dowód osobisty gracza)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            team_id INTEGER,
            name TEXT,
            position TEXT,
            nationality TEXT,
            FOREIGN KEY (team_id) REFERENCES teams (team_id) ON DELETE CASCADE
        )
    ''')

    # 4. Tabela MECZÓW
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY,
            match_date TEXT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            home_goals INTEGER,
            away_goals INTEGER,
            round TEXT,
            FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
            FOREIGN KEY (away_team_id) REFERENCES teams (team_id)
        )
    ''')

    # 5. Tabela STATYSTYK MECZOWYCH ZAWODNIKÓW (Analityczne mięso)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_match_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            player_id INTEGER,

            -- Nasze zebrane statystyki:
            goals INTEGER DEFAULT 0,
            assists INTEGER DEFAULT 0,
            shots_total INTEGER DEFAULT 0,
            shots_on_target INTEGER DEFAULT 0,
            offsides INTEGER DEFAULT 0,
            yellow_cards INTEGER DEFAULT 0,
            red_cards INTEGER DEFAULT 0,
            fouls INTEGER DEFAULT 0,

            FOREIGN KEY (match_id) REFERENCES matches (match_id) ON DELETE CASCADE,
            FOREIGN KEY (player_id) REFERENCES players (player_id) ON DELETE CASCADE
        )
    ''')

    # 6. Zapisanie zmian i zamknięcie połączenia
    conn.commit()
    conn.close()
    print("Baza danych laliga.db została utworzona i jest gotowa na dane!")


if __name__ == "__main__":
    setup_database()