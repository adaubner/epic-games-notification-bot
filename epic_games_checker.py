import epicstore_api
import sqlite3
from logging import warning

api = epicstore_api.EpicGamesStoreAPI()


# make a call to the epic store api and return parsed free games
# TODO is this needed?
def get_free_games():
    api_return = api.get_free_games()
    games = parse_games(api_return)
    return games


# TODO when to notify, twice per game? notify about upcoming free games? Ideally you want it once, right as it becomes free, and on request if later. Two channels?
# TODO log when data does not fit expected model
# TODO return current, and upcoming promotions?
# TODO model api return
# parse api return to common object type
# will only return TRUE free games
def parse_games(api_return):
    games = list()
    try:
        api_return = api_return["data"]["Catalog"]["searchStore"]["elements"]
    except KeyError:
        warning("Could not parse epic games api_return: " + api_return)
    for game in api_return:
        # Check if game is valid free game
        # Game cannot be DLC
        if game["offerType"] == "DLC":
            continue

        # Game must cost 0 eur/usd/...
        if game["price"]["totalPrice"]["discountPrice"] != 0:
            continue

        # Game must have a currently active promotion
        if len(game["promotions"]["promotionalOffers"]) == 0:
            continue

        # TODO add more conditions

        # At this point we know that the game is currently free
        # Generate a universal game object
        free_game = { 
            "title": game["title"],
            "description": game["description"],
            "free_after": game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["startDate"],
            "free_until": game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"],
        }
        games.append(free_game)
    return games


def is_new_free_game(game):
    # check if game is already in the database
    # TODO have a better check for existing game, if details change you want to update it
    cur.execute(
        """SELECT * FROM free_games WHERE title = ? AND free_after = ? AND free_until = ?;""",
        (game["title"], game["free_after"], game["free_until"]),
    )
    if len(cur.fetchall()) == 0:
        cur.execute(
            """INSERT INTO free_games (title, description, free_after, free_until) VALUES(?,?,?,?);""",
            (
                game["title"],
                game["description"],
                game["free_after"],
                game["free_until"],
            ),
        )
        con.commit()
        return True
    return False


# TODO sql methods?


# check if there are any NEW free games, return them
def check_games():
    # Prepare SQL
    global con
    global cur
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    # Get new Free games
    free_games = get_free_games()
    new_free_games = list()
    for game in free_games:
        if is_new_free_game(game):
            new_free_games.append(game)
    # Close SQL
    cur.close()
    return new_free_games
