from epicstore_api import EpicGamesStoreAPI, OfferData
import pandas as pd
import datetime

API=EpicGamesStoreAPI()

def get_games():#FIXME set defauls store country 
	games=API.get_free_games()['data']['Catalog']['searchStore']['elements']#games is a python list of games, each item in that list is a dict
	#nice_data.to_csv('out.csv')#TODO remove debug lines
	free_games=[]
	for game in games:
		if is_free_game(game):
			print(clean_game_data(game))
			free_games.append(clean_game_data(game))
			print('-'*50)
	return free_games

def clean_game_data(data):
	clean_data={#TODO get developer and publisher info from customAttributes and photo urls
		"title": data["title"],
		"subtitle": "Subtitles are yet to come! This is temporary",
		"promotion_end_time": datetime.datetime.strptime(data["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"],"%Y-%m-%dT%H:%M:%S.%fZ")
	}
	return clean_data

def is_free_game(game):#FIXME I need some testing, should evaluate to true if a game has a "promotions" disctionary and then the promotionalOffers key contains a list at least 1 in length.
	if game["promotions"] is not None:
		if len(game["promotions"]["promotionalOffers"]) > 0:
			return True
	return False

##############runtime################

""" #temp debug variable remove
#example_game={'title': 'The Spectrum Retreat','id': '2cb68a86262b4e0a91dbe0625cbbb242', 'namespace': '32ef234417314b65a4f76041b684f4d0', 'description': 'The Spectrum Retreat', 'effectiveDate': '2021-07-01T15:00:00.000Z', 'offerType': 'BASE_GAME', 'expiryDate': None, 'status': 'ACTIVE', 'isCodeRedemptionOnly': False, 'keyImages': [{'type': 'CodeRedemption_340x440', 'url': 'https://cdn1.epicgames.com/salesEvent/salesEvent/bf525c62-bc8c-4a51-9d30-799186ab1293_1200x1600-166b997f74a0f926ffe562d8b3dc67b9'}, {'type': 'Thumbnail', 'url': 'https://cdn1.epicgames.com/salesEvent/salesEvent/bf525c62-bc8c-4a51-9d30-799186ab1293_1200x1600-166b997f74a0f926ffe562d8b3dc67b9'}, {'type': 'OfferImageTall', 'url': 'https://cdn1.epicgames.com/salesEvent/salesEvent/bf525c62-bc8c-4a51-9d30-799186ab1293_1200x1600-166b997f74a0f926ffe562d8b3dc67b9'}, {'type': 'OfferImageWide', 'url': 'https://cdn1.epicgames.com/salesEvent/salesEvent/52b99d72-9223-4524-ab74-240ae808c489_2560x1440-d583c45997a46d39e1a31525ae883b84'}, {'type': 'DieselStoreFrontTall', 'url': 'https://cdn1.epicgames.com/salesEvent/salesEvent/bf525c62-bc8c-4a51-9d30-799186ab1293_1200x1600-166b997f74a0f926ffe562d8b3dc67b9'}, {'type': 'DieselStoreFrontWide', 'url': 'https://cdn1.epicgames.com/salesEvent/salesEvent/52b99d72-9223-4524-ab74-240ae808c489_2560x1440-d583c45997a46d39e1a31525ae883b84'}], 'seller': {'id': 'o-fbx9l7z95axq9s73trhbttadbareuq', 'name': 'Ripstone Ltd'}, 'productSlug': 'the-spectrum-retreat', 'urlSlug': 'capsicum-general-audience', 'url': None, 'items': [{'id': '7a643c21ff114df8a553a3685ae5f5e7', 'namespace': '32ef234417314b65a4f76041b684f4d0'}], 'customAttributes': [{'key': 'com.epicgames.app.blacklist', 'value': '[]'}, {'key': 'publisherName', 'value': 'Ripstone Ltd'}, {'key': 'developerName', 'value': 'Dan Smith'}, {'key': 'com.epicgames.app.productSlug', 'value': 'the-spectrum-retreat'}], 'categories': [{'path': 'freegames'}, {'path': 'games'}, {'path': 'games/edition'}, {'path': 'games/edition/base'}, {'path': 'applications'}], 'tags': [{'id': ': 0, 'discount': 1299, 'currencyCode': 'USD', 'currencyInfo': {'decimals': 2}, 'fmtPrice': {'originalPrice': '$12.99', 'discountPrice': '0', 'intermediatePrice': '0'}}, 'lineOffers': [{'appliedRules': [{'id': '0e6c4423663c49c7bbfe97225f67448d', 'endDate': '2021-07-08T15:00:00.000Z', 'discountSetting': {'discountType': 'PERCENTAGE'}}]}]}, 'promotions': {'promotionalOffers': [{'promotionalOffers': [{'startDate': '2021-07-01T15:00:00.000Z', 'endDate': '2021-07-08T15:00:00.000Z', 'discountSetting': {'discountType': 'PERCENTAGE', 'discountPercentage': 0}}]}], 'upcomingPromotionalOffers': []}}
 """
if __name__=="__main__":
	print(get_games())
