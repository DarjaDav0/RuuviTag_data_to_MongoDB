import asyncio
import pymongo
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from datetime import datetime
from pytz import timezone

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["Ruuvi_tag"]
mycol = mydb["ruuvi-tags_data"]

macs = ['CE:1B:AC:05:D6:3F']

async def main():
    async for data in RuuviTagSensor.get_data_async(macs):
        mac_address = data[0] 
        sensor_data = data[1]

        sensor_data["CE:1B:AC:05:D6:3F"] = mac_address

        # Add the current timestamp and timezone to the sensor data
        sensor_data["timestamp"] = datetime.now()
        sensor_data["timezone"] = datetime.now(pytz.timezone('Europe/Helsinki')).strftime('%Z%z')

        # Insert the sensor data into the MongoDB collection
        result = mycol.insert_one(sensor_data)

        # Check if the data was inserted
        if result.acknowledged:
            print(f"Data was inserted with ID: {result.inserted_id}")
        else:
            print("Data was not inserted")

if __name__ == "__main__":
    asyncio.run(main())