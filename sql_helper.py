import sqlite3


def start():
    global con
    global cur
    con = sqlite3.connect("persistent_data/database.db")
    cur = con.cursor()


def stop():
    global con
    global cur
    cur.close()
    con.close()


# TODO throw exception when keys don't match

def select_game(game: dict):
    cur.execute(
        """SELECT * FROM free_games WHERE 
        id = ? AND 
        title = ? AND
        free_after = ? AND 
        free_until = ?;""",
        (
            game["id"],
            game["title"],
            game["free_after"],
            game["free_until"],
        ),
    )
    return cur.fetchall()


def contains_game(game: dict):
    return len(select_game(game)) > 0


def insert_game(game: dict):
    cur.execute(
        """INSERT INTO free_games (id, title, description, image, free_after, free_until) VALUES(?,?,?,?,?,?);""",
        (
            game["id"],
            game["title"],
            game["description"],
            game["image"],
            game["free_after"],
            game["free_until"],
        ),
    )
    con.commit()
