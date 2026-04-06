# RuuviTag to MongoDB Data Logger & Analyzer

## What This Codebase Does
This project provides a set of Python scripts designed to capture environmental data (humidity, temperature, and atmospheric pressure) from RuuviTag sensors and store it in a local MongoDB database for long-term tracking. It also includes an aggregation script tailored for analyzing and visualizing that data.

The project is divided into two primary functions:
1. **Data Collection (`inserting_data.py`)**: This script continuously scans for Bluetooth Low Energy (BLE) broadcasts from a configured RuuviTag. Upon receiving a broadcast, it extracts the sensor readings (including temperature, humidity, and atmospheric pressure), applies a local timestamp and timezone (`Europe/Helsinki`), and inserts the document into a MongoDB database named `Ruuvi_tag`.
2. **Data Aggregation and Visualization (`data-aggregation.py`)**: This script interacts with the stored MongoDB data for analytical purposes. It prompts the user for a specific date and utilizes a MongoDB aggregation pipeline to compute the hourly and overall daily averages for the sensor metrics. Using `pandas` and `matplotlib`, it then displays interactive line graphs of the hourly trends and prints the daily averages to the console.

---

## How to Use With a RuuviTag Device

### Prerequisites
- A RuuviTag device actively broadcasting data.
- A host machine (PC, Mac, or Raspberry Pi) with Python 3 and a working Bluetooth adapter.
- [MongoDB](https://www.mongodb.com/try/download/community) installed and running locally on the default port (`localhost:27017`).

### 1. Install Dependencies
Clone this repository and install the required Python packages from the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Configure Your RuuviTag MAC Address
Before running the collector, you need to configure the script to target your specific RuuviTag. 
1. Find the MAC address of your RuuviTag (often found via the Ruuvi Station mobile app or a BLE scanning tool).
2. Open `inserting_data.py`.
3. Locate the `macs` list on line 10 and replace `YOUR:MAC:ADDRESS:HERE` with your device's MAC address:
   ```python
   macs = ['YOUR:MAC:ADDRESS:HERE']
   ```
4. Update the dictionary key insertion in the `main` loop to reflect your MAC address as well:
   ```python
   sensor_data["YOUR:MAC:ADDRESS:HERE"] = mac_address
   ```

### 3. Start Collecting Data
Run the insertion script. Ensure Bluetooth is enabled on your host machine.
```bash
python inserting_data.py
```
The script will run asynchronously, listening for your RuuviTag's broadcasts. Every time it reads and saves a data point, it will print `Data was inserted with ID: <ObjectId>` to the console. Leave this process running for as long as you want to log data.

### 4. Visualize the Data
Once you have collected data for a given day, you can run the aggregation script to view the trends:
```bash
python data-aggregation.py
```
The console will prompt you to enter a date:
```text
Enter the selected day (YYYY-MM-DD): 
```
Type your desired date (e.g., `2024-04-06`) and press Enter. The script will render line graphs for the hourly average temperature, humidity, and pressure, and will print out the total averages for the day in the terminal.