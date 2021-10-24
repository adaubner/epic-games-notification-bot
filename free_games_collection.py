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



def main():
	global con, cur
	con = sqlite3.connect(DB_PATH)
	cur = con.cursor()
	insert_data((datetime.now(timezone.utc).isoformat(),str(API.get_free_games()).replace('"',"'"),'3',epic_api_fetch.get_games(),'5','test'))#TODO find diference from last entry into database.
	con.close()



#########Runtime#########

if __name__=='__main__':
	main()