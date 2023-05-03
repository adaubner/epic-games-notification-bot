import epicstore_api
from logging import warning
from datetime import datetime

api = epicstore_api.EpicGamesStoreAPI()





# make a call to the epic store api and return parsed free games
def get_free_games():
    api_return = api.get_free_games()
    import json
    with open('temp.json', 'w') as f:
        f.write(json.dumps(api_return))
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
        if(game["offerType"] == "DLC"):
            continue
        
        # Game must cost 0 eur/usd/...
        if(game["price"]["totalPrice"]["discountPrice"] != 0):
            continue
        
        # Game must have a currently active promotion
        if(len(game["promotions"]["promotionalOffers"]) == 0):
            continue
        
        # TODO add more conditions
        
        # At this point we know that the game is currently free
        # Generate a universal game object
        free_until = datetime.fromisoformat(game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"])
        free_game = {
            "title": game["title"],
            "description":game["description"],
            "free_until":free_until.strftime("%d/%m/%Y")
        }
        games.append(free_game)
    return games
        
        
        


# maybe?
# TODO have a current promotions database, needs to be updated every time first.
def check_or_add_to_sql():
    return




# check if there are any NEW free games, return them
def check_games():
    free_games = get_free_games()


# TODO removeme
if __name__ == '__main__':
    games = get_free_games()
    pass
