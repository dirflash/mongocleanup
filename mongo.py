import configparser
from time import time, sleep
from datetime import datetime, timedelta
import certifi
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rich import print, box
from rich.console import Console
from rich.table import Table
from rich.progress import track

if __name__ == "__main__":

    starttime = int(time())
    first = True

    console = Console()

    config = configparser.ConfigParser()
    config.read("config.ini")
    key = config["DEFAULT"]["key"]
    user = config["DEFAULT"]["user_id"]
    system = config["DEFAULT"]["system"]
    mongoaddr = config["MONGO"]["mongo_addr"]
    mongodb = config["MONGO"]["mongo_db"]
    mongocollect = config["MONGO"]["mongo_collect"]
    mongouser = config["MONGO"]["user_name"]
    mongopw = config["MONGO"]["password"]

    maxMongoDBDelay = 500

    client = MongoClient(
        "mongodb+srv://"
        + mongouser
        + ":"
        + mongopw
        + "@"
        + mongoaddr
        + "/"
        + mongodb
        + "?retryWrites=true&w=majority",
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=maxMongoDBDelay,
    )

    db = client[mongodb]
    collection = db[mongocollect]

    while True:
        if first is False:
            start_time = time()

        docs = collection.estimated_document_count()

        t = time()
        easytime = datetime.fromtimestamp(t)
        ezytime = int(easytime.timestamp())

        minus2 = t - 345600  # 4-days
        easytime2 = datetime.fromtimestamp(minus2)
        ezytime2 = int(easytime2.timestamp())

        deldocs = collection.count_documents({"EpochLastReport": {"$lt": ezytime2}})

        coltable = Table(title="Before Statistics", box=box.SIMPLE, style="red")

        coltable.add_column("Type", style="red")
        coltable.add_column("Data", justify="right", style="red")

        coltable.add_row("Current time", str(ezytime))
        coltable.add_row("Pruning time", str(ezytime2))
        coltable.add_row("Number of docs", str(docs))
        coltable.add_row("Docs to delete", str(deldocs))

        if coltable.columns:
            console.print(coltable)
        else:
            print("[i]No data...[/i]")

        delold = collection.delete_many({"EpochLastReport": {"$lt": ezytime2}})

        newdocs = collection.estimated_document_count()
        docsdel = docs - newdocs

        coltable = Table(title="After Statistics", box=box.SIMPLE, style="cyan")

        coltable.add_column("Type", style="cyan3")
        coltable.add_column("Data", justify="right", style="cyan3")

        coltable.add_row("Number of docs", str(newdocs))
        coltable.add_row("Docs deleted", str(docsdel))

        if coltable.columns:
            console.print(coltable)
        else:
            print("[i]No data...[/i]")

        console.log(
            "--- Script ran in [bold cyan]%.3f seconds[/bold cyan] ---"
            % (time() - starttime)
        )

        nextrun = 12
        nextrunsec = (nextrun * 60) * 60

        ennext = datetime.now() + timedelta(hours=nextrun)
        nextrun = ennext.strftime("%m-%d-%Y %H:%M:%S")
        console.log(f"--- Next run: [bold cyan]{nextrun}[/bold cyan] ---")

        first = False

        for t in range(1):
            for n in track(
                range(nextrunsec), description="Count down", refresh_per_second=1
            ):
                sleep(1)
