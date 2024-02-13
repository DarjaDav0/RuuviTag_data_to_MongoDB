import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime

# Create a client connection to your MongoDB instance
client = MongoClient("mongodb://localhost:27017")

# Connect to your database
db = client["Ruuvi_tag"]

# Connect to your collection
collection = db["ruuvi-tags_data"]

# Define the selected day
selected_day = datetime.strptime(input("Enter the selected day (YYYY-MM-DD): "), "%Y-%m-%d")

pipeline = [
    {
        "$match": {
            "timestamp": {
                "$gte": selected_day,
                "$lt": datetime(selected_day.year, selected_day.month, selected_day.day + 1)
            }
        }
    },
    {   # Add the hour field to the documents and calculate the average of fields
        "$group": {
            "_id": { "hour": { "$hour": "$timestamp" } },
            "average_humidity_percent": { "$avg": "$humidity" },
            "average_temperature": { "$avg": "$temperature" },
            "average_pressure_hPa": { "$avg": "$pressure" }
        }
    },
    {   # Round the average results
        "$addFields": {
            "average_humidity_percent": { "$round": ["$average_humidity_percent", 2] },
            "average_temperature": { "$round": ["$average_temperature", 2] },
            "average_pressure_hPa": { "$round": ["$average_pressure_hPa", 2] }
        }
    },
    {   # Sort the output by hours
        "$sort": { "_id.hour": 1 }
    },
    {   # Group all documents and calculate the day's average
        "$group": {
            "_id": None,
            "day_average_humidity_percent": { "$avg": "$average_humidity_percent" },
            "day_average_temperature": { "$avg": "$average_temperature" },
            "day_average_pressure_hPa": { "$avg": "$average_pressure_hPa" },
            "hourly_averages": { "$push": "$$ROOT" }
        }
    },
    {   # Round the day's average results
        "$addFields": {
            "day_average_humidity_percent": { "$round": ["$day_average_humidity_percent", 2] },
            "day_average_temperature": { "$round": ["$day_average_temperature", 2] },
            "day_average_pressure_hPa": { "$round": ["$day_average_pressure_hPa", 2] }
        }
    }
]

aggregate_result = collection.aggregate(pipeline)

# Convert the aggregation results to a pandas DataFrame
df = pd.DataFrame(list(aggregate_result))

# Create a new DataFrame for the hourly averages
hourly_averages = pd.json_normalize(df['hourly_averages'][0])

# Set the hour as the index
hourly_averages.set_index('_id.hour', inplace=True)

# Hourly average humidity
hourly_averages['average_humidity_percent'].plot(kind='line')
plt.title('Hourly Average Humidity')
plt.xlabel('Hour')
plt.ylabel('Humidity (%)')
plt.show()

# Hourly average temperature
hourly_averages['average_temperature'].plot(kind='line')
plt.title('Hourly Average Temperature')
plt.xlabel('Hour')
plt.ylabel('Temperature (°C)')
plt.show()

# Hourly average pressure
hourly_averages['average_pressure_hPa'].plot(kind='line')
plt.title('Hourly Average Pressure')
plt.xlabel('Hour')
plt.ylabel('Pressure (hPa)')
plt.show()

# Day's averages
print(f"Day's average humidity: {df['day_average_humidity_percent'][0]}%")
print(f"Day's average temperature: {df['day_average_temperature'][0]}°C")
print(f"Day's average pressure: {df['day_average_pressure_hPa'][0]} hPa")

# Print the aggregation results
"""for document in aggregate_result:
    print(f"Day's average humidity: {document['day_average_humidity_percent']}%")
    print(f"Day's average temperature: {document['day_average_temperature']}°C")
    print(f"Day's average pressure: {document['day_average_pressure_hPa']} hPa")
    print("Hourly averages:")
    for hourly_average in document['hourly_averages']:
        print(f"  Hour: {hourly_average['_id']['hour']}")
        print(f"  Average humidity: {hourly_average['average_humidity_percent']}%")
        print(f"  Average temperature: {hourly_average['average_temperature']}°C")
        print(f"  Average pressure: {hourly_average['average_pressure_hPa']} hPa")"""