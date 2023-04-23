import epicstore_api

api = epicstore_api.EpicGamesStoreAPI()





# make a call to the epic store api and return parsed free games
def get_free_games():
    api_return = api.get_free_games()
    import json
    with open('temp.json', 'w') as f:
        f.write(json.dumps(api_return))
    games = parse_games(api_return)
    return games


games = [
    {
        "title":"asdf",
        "description":"asdf"
    }
]

# TODO when to notify, twice per game? notify about upcoming free games? Ideally you want it once, right as it becomes free, and on request if later. Two channels?
# TODO log when data does not fit expected model
# parse api return to common object type
# will only return TRUE free games
def parse_games(api_return):
    return


# maybe?
# TODO have a current promotions database, needs to be updated every time first.
def check_or_add_to_sql():
    return




# check if there are any NEW free games, return them
def check_games():
    free_games = get_free_games()


# TODO removeme
if __name__ == '__main__':
    get_free_games()
