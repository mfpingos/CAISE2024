# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 18:36:21 2023

@author: mpingos
"""

import random
from faker import Faker
from datetime import datetime, timedelta
import time

fake = Faker()

def generate_data(source_id, location, variety, velocity):
    start_date = fake.date_between_dates(date_start=datetime(2022, 1, 1), date_end=datetime(2022, 12, 31))
    max_end_date = start_date + timedelta(days=120)  # Maximum 4 months difference
    end_date = fake.date_between_dates(date_start=start_date, date_end=max_end_date)

    data = {
        "ex:source_name": f"{source_id}_FLOCK_{velocity}_EXPORT-{start_date.strftime('%d-%m-%Y')}",
        "ex:flockid": source_id,
        "ex:location": location,
        "ex:feedcycle_start": start_date.strftime('%Y-%m-%d'),
        "ex:feedcycle_end": end_date.strftime('%Y-%m-%d'),
        "ex:keywords": "growDay, hour, requiredTemperature, coldTemperatureAlarm, hotTemperatureAlarm, sensor1, sensor2, sensor3, sensor4, sensor5, outsideTemp, currentAverageTemp, humidity, staticPressure, currentCO2, CO2HourMax, CO2HourMin",
        "ex:variety": variety,
        "ex:velocity": velocity,
        "ex:source_path": f"hdfs://your-hadoop-namenode:9000/user/sources/daily_flock_{source_id}_data"
    }

    return data

def generate_volume(size, unit):
    sizes = {
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3
    }
    return f"{size} {unit}"

def save_to_ttl(data, filename):
    with open(filename, 'a') as file:
        file.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n")
        file.write("@prefix ex: <http://example.org/>.\n\n")

        for source_id, details in data.items():
            file.write(f"ex:source{source_id}\n")
            file.write("  rdf:type ex:Description ;\n")
            for key, value in details.items():
                file.write(f"  {key} \"{value}\" ;\n")
            file.write("  .\n\n")

if __name__ == "__main__":
    start_time = time.time()

    data_size = int(input("Enter the number of sources to generate: "))
    unit = input("Enter the unit for data size (KB, MB, or GB): ")

    data = {}

    for source_id in range(1, data_size + 1):
        location = random.choice(["Larnaca", "Famagusta", "Nicosia", "Pafos", "Limassol"])
        variety = random.choice(["structured", "unstructured", "semi-structured"])
        velocity = random.choice(["Hourly", "Daily", "Monthly", "Yearly"])

        data[source_id] = generate_data(source_id, location, variety, velocity)

    for source_id, details in data.items():
        volume_size = random.randint(1, 100)
        volume = generate_volume(volume_size, unit)
        details["ex:volume"] = volume

    ttl_filename = input("Enter the TTL file name to save the data (e.g., output.ttl): ")
    save_to_ttl(data, ttl_filename)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Random data has been generated and saved to {ttl_filename}.")
    print(f"Execution time: {execution_time} seconds.")
