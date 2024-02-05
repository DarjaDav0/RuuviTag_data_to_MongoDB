import asyncio
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import pymongo

macs = ["CE:1B:AC:05:D6:3F"]

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["Ruuvi_tag"]
mycol = mydb["ruuvi-tags_data"]

async def main():
    # Get data only for defineded MACs. Exit after 10 found results
    datas = []
    async for found_data in RuuviTagSensor.get_data_async(macs):
        print(f"MAC: {found_data[0]}")
        print(f"Data: {found_data[1]}")
        datas = found_data[1]
        mycol.insert_one(datas)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())