import sqlite3
from sqlite3 import Error
import difflib as diff
from datetime import datetime, timezone
import epic_api_fetch
from epicstore_api import EpicGamesStoreAPI, OfferData

DB_PATH = r'free_games.db'
API = EpicGamesStoreAPI()
DB_NAME = 'games'


def insert_data(data):
	"""Inserts one entry into games table of free_games.db
	@param: tuple containing index, date, api_return, api_return_change, free_games, free_games_change, notes
	Date+time is stored in ISO format
	Set notes to 'test' when making entry that should be deleted later
	"""
	# reference for sql https://www.w3schools.com/sql/sql_insert.asp
	# no semi colon needed, double vs single quotes does not matter, use ? for values
	cur.execute(f"INSERT INTO {DB_NAME} VALUES (?, ?, ?, ?, ?, ?, ?)", data)
	con.commit()


def get_last_entry(column):
	"""Make request to database for last entry of given column

	"""
	cur.execute(f'SELECT {column} FROM {DB_NAME} ORDER BY id DESC LIMIT 1')  # Get last entry by id column
	last = cur.fetchall()[0][0]  # [0][0] required to remove list and tuple onion
	return last


def get_last_index():
	cur.execute(f'SELECT id From {DB_NAME} ORDER BY id DESC LIMIT 1')
	return int(cur.fetchall()[0][0])  # [0][0] required to remove list and tuple onion


def calculate_change(current, column):
	"""Finds the additions and deletions (delta) between two strings
	@Param: String latest entry, String column name
	Function will access the last entry in the specified column in the data base,
	it will then compare the last entry to the current entry using the difflib library
	"""
	last = get_last_entry(column)
	difference_gen = diff.ndiff(last, current)
	difference = ''.join(difference_gen)
	return difference


def main():
	global con, cur
	con = sqlite3.connect(DB_PATH)
	cur = con.cursor()
	#  gathering variables
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
