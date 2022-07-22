import configparser
import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

config = configparser.ConfigParser()
config.read("svr_stat_config.ini")
mongoaddr = config["MONGO"]["mongo_addr"]
mongodb = config["MONGO"]["mongo_db"]
mongouser = config["MONGO"]["user_name"]
mongopw = config["MONGO"]["password"]

MAX_MONGODB_DELAY = 500

Mongo_Client = MongoClient(
    f"mongodb+srv://{mongouser}:{mongopw}@{mongoaddr}/{mongodb}?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=MAX_MONGODB_DELAY,
)

db = Mongo_Client.admin


try:
    svr_status = db.command("serverStatus")
    print(svr_status)
except Exception as e:
    print(e)
else:
    print("You are connected!")
