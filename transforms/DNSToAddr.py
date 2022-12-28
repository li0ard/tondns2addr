import socket, requests

from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

class DNSToAddr(DiscoverableTransform):
	@classmethod
	def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
		domain = request.Value
		try:
			siteInfo = requests.get("https://tonapi.io/v1/dns/getInfo?name=" + domain).json()
			if "error" in siteInfo:
				response.addUIMessage(f"Error: Domain not found", UIM_TYPES["fatal"])
			else:
				walletInfo = requests.get("https://tonapi.io/v1/account/getInfo?account=" + siteInfo["nft_item"]["owner"]["address"]).json()
				if walletInfo["address"]["bounceable"]:
					a = response.addEntity("maltego.CryptocurrencyAddress", walletInfo["address"]["bounceable"])
				elif walletInfo["address"]["non_bounceable"]:
					a = response.addEntity("maltego.CryptocurrencyAddress", walletInfo["address"]["non_bounceable"])
				else:
					a = response.addEntity("maltego.CryptocurrencyAddress", walletInfo["address"]["raw"])
				a.setIconURL("https://ton.org/download/ton_symbol.png")
		except:
			response.addUIMessage(f"Error", UIM_TYPES["partial"])
