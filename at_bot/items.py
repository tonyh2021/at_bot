# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

# "make":"Acura",
# "model":"MDX",
# "year":"2020",
# "trim":"Tech SH-AWD (7Year 160K Factory Warranty Included)",
# "vin":"XXXXXXXXXXXXXXXXX",
# "price":"38,588",
# "location":"Aurora",
# "mileage":"60,022 km",
# "priceAnalysis":"GreatPrice",
# "vehicleAge":"",
# "priceAnalysisDescription":"$4,922 BELOW MARKET",
# "status":"Used",
# "stockNumber":"L3241",
# "carfax":"FreeCarFax",
class ATBotItem(Item):
    # define the fields for your item here like:
    adId = Field()

    trim = Field()
    price = Field()
    location = Field()
    mileage = Field()
    stockNumber = Field()
    conditions = Field()

    carfax = Field()
    vin = Field()
    damaged = Field()
    serviceRecords = Field()
    openRecall = Field()
    stolen = Field()
    oneOwner = Field()
    
    item_url = Field()