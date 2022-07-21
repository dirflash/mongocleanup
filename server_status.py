import configparser
import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

config = configparser.ConfigParser()
config.read("config.ini")
mongoaddr = config["MONGO"]["mongo_addr"]
mongodb = config["MONGO"]["mongo_db"]
mongocollect = config["MONGO"]["mongo_collect"]
mongouser = config["MONGO"]["user_name"]
mongopw = config["MONGO"]["password"]

MAX_MONGODB_DELAY = 500

Mongo_Client = MongoClient(
    f"mongodb+srv://{mongouser}:{mongopw}@{mongoaddr}/{mongodb}?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=MAX_MONGODB_DELAY,
)

db = Mongo_Client[mongodb]
collection = db[mongocollect]
dbase = db["counter"]

try:
    dbase.command("serverStatus")
except Exception as e:
    print(e)
else:
    print("You are connected!")
dbase.close()
