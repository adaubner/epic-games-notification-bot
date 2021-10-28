import sqlite3
from sqlite3 import Error
from datetime import datetime, timezone
import epic_api_fetch
from epicstore_api import EpicGamesStoreAPI, OfferData

DB_PATH = r'C:\Users\Andy\Documents\_python\epic-games-bot\free_games.db'#TODO fix path, change to relative.
API=EpicGamesStoreAPI()
"""
class connectionError(Exception):
	#https://stackabuse.com/how-to-print-colored-text-in-python/
	print("\n\033[1;31;43m Please uncomment the connection (ctrl+f \"con\"), this exception is here to prevent accidental spamming of database. \033[0;0m\n")
raise connectionError
"""

def insert_data(data):
	"""Inserts one entry into games table of free_games.db
	@param: tuple containing date, api_return, api_return_change, free_games, free_games_change, notes
	Date+time is stored in ISO format
	Set notes to 'test' when making entry that should be deleted later
	"""
	#reference for sql https://www.w3schools.com/sql/sql_insert.asp
	cur.execute(f"INSERT INTO games VALUES (\"{data[0]}\",\"{data[1]}\",\"{data[2]}\",\"{data[3]}\",\"{data[4]}\",\"{data[5]}\")")#no semi colon needed, double vs single quotes does not matter
	con.commit()

def get_last_entry():
	last_id = cur.lastrowid
	last = cur.execute(f"SELECT * FROM games WHERE rowid = {last_id}")  #_FIXME do NOT select * pass the column as a parameter
	return last

def calculate_change(current):
	"""
	Precon: len(current) >= len(last)
	"""
	last = get_last_entry()
	difference = ''
	for i in range(len(current)):
		if current[i] != last[i]:
			difference += current[i]
	return difference

def main():
	global con, cur
	con = sqlite3.connect(DB_PATH)
	cur = con.cursor()
	#gathering variables
	time_stamp = datetime.now(timezone.utc).isoformat()
	api_return = str(API.get_free_games()).replace('"', "'")  #_TODO calculate api_return change
	api_return_change = calculate_change(api_return)
	free_games = epic_api_fetch.get_games()
	free_games_change = calculate_change(free_games)
	insert_data((time_stamp, api_return, api_return_change, free_games, free_games_change, 'test'))
	con.close()


#########Runtime#########

if __name__ == '__main__':
	main()
