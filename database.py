import sqlite3
from typing import List
from pydantic import BaseModel
from math import radians, sin, cos, sqrt, atan2

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("address_book.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS addresses (
                                id INTEGER PRIMARY KEY,
                                latitude REAL,
                                longitude REAL,
                                address TEXT
                            )''')
        self.conn.commit()

    def create_address(self, address):
        self.cursor.execute('''INSERT INTO addresses (latitude, longitude, address)
                               VALUES (?, ?, ?)''', (address.latitude, address.longitude, address.address))
        self.conn.commit()
        return address

    def get_addresses(self):
        self.cursor.execute('''SELECT * FROM addresses''')
        rows = self.cursor.fetchall()
        return [{"id": row[0], "latitude": row[1], "longitude": row[2], "address": row[3]} for row in rows]

    def delete_address(self, address_id):
        self.cursor.execute('''DELETE FROM addresses WHERE id=?''', (address_id,))
        self.conn.commit()

    def get_addresses_within_distance(self, latitude, longitude, distance):
        self.cursor.execute('''SELECT * FROM addresses''')
        rows = self.cursor.fetchall()
        addresses_within_distance = []
        for row in rows:
            if self.calculate_distance(latitude, longitude, row[1], row[2]) <= distance:
                addresses_within_distance.append({"id": row[0], "latitude": row[1], "longitude": row[2], "address": row[3]})
        return addresses_within_distance

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371.0  # approximate radius of Earth in km
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance
