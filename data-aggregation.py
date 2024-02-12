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

# Find and print the documents that match the selected day
'''matched_documents = collection.find({
    "timestamp": {
        "$gte": selected_day,
        "$lt": datetime(selected_day.year, selected_day.month, selected_day.day + 1)
    }
})

for document in matched_documents:
    print(document)'''

pipeline = [
    {
        "$match": {
            "timestamp": {
                "$gte": selected_day,
                "$lt": datetime(selected_day.year, selected_day.month, selected_day.day + 1)
            }
        }
    },
    {   # Add the hour field to the documents
        "$addFields": {
            "hour": { "$hour": "$timestamp" }
        }
    },
    {   # Group the documents by the hour field and calculate the average of field
        "$group": {
            "_id": { "hour": "$hour" },
            "average_humidity": { "$avg": "$humidity" },
            "average_temperature": { "$avg": "$temperature" },
            "average_pressure": { "$avg": "$pressure" }
        }
    },
    {   # Round the average results
        "$addFields": {
            "average_humidity": { "$round": ["$average_humidity", 2] },
            "average_temperature": { "$round": ["$average_temperature", 2] },
            "average_pressure": { "$round": ["$average_pressure", 2] }
        }
    }
]

aggregate_result = collection.aggregate(pipeline)

# Print the aggregation results
for document in aggregate_result:
    print(document)