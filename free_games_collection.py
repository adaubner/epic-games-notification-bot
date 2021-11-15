import sqlite3
from sqlite3 import Error
import difflib as diff
from datetime import datetime, timezone
import epic_api_fetch
from epicstore_api import EpicGamesStoreAPI, OfferData

# DB_PATH = r'C:\Users\Andy\Documents\_python\epic-games-bot\free_games.db'#_TODO fix path, change to relative.
DB_PATH_LINUX = r'/home/andy/PycharmProjects/epic-games-notification-bot/free_games.db'
API=EpicGamesStoreAPI()
DB_NAME = 'games'
"""
class connectionError(Exception):
	#https://stackabuse.com/how-to-print-colored-text-in-python/
	print("\n\033[1;31;43m Please uncomment the connection (ctrl+f \"con\"), this exception is here to prevent accidental spamming of database. \033[0;0m\n")
raise connectionError
"""


def insert_data(data):
	"""Inserts one entry into games table of free_games.db
	@param: tuple containing index, date, api_return, api_return_change, free_games, free_games_change, notes
	Date+time is stored in ISO format
	Set notes to 'test' when making entry that should be deleted later
	"""
	#reference for sql https://www.w3schools.com/sql/sql_insert.asp
	cur.execute(f"INSERT INTO {DB_NAME} VALUES (?, ?, ?, ?, ?, ?, ?)", data)  #no semi colon needed, double vs single quotes does not matter, use ? for values
	con.commit()


def get_last_entry(column):
	"""Make request to database for

	"""
	cur.execute(f'SELECT {column} FROM {DB_NAME} ORDER BY id DESC LIMIT 1')  #Get last entry by id column
	last = cur.fetchall()[0][0]  #[0][0] reqired to remove list and tuple onion
	return last


def get_last_index():
	cur.execute(f'SELECT id From {DB_NAME} ORDER BY id DESC LIMIT 1')
	return int(cur.fetchall()[0][0])  #[0][0] reqired to remove list and tuple onion


def calculate_change(current, column):
	"""
	Docs blablabla
	"""
	last = get_last_entry(column)
	difference_gen = diff.ndiff(last, current)
	difference = ''.join(difference_gen)
	return difference


def main():
	global con, cur
	con = sqlite3.connect(DB_PATH_LINUX)
	cur = con.cursor()
	#gathering variables
	time_stamp = datetime.now(timezone.utc).isoformat()
	api_return = str(API.get_free_games())
	api_return_change = calculate_change(api_return, 'api_return')
	free_games = str(epic_api_fetch.get_games())
	free_games_change = calculate_change(free_games, 'free_games')
	insert_data((get_last_index() + 1, time_stamp, api_return, api_return_change, free_games, free_games_change, 'test'))
	con.close()


#########Runtime#########

if __name__ == '__main__':
	main()
