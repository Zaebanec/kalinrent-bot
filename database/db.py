# database/db.py

import sqlite3
from typing import Dict, List

DB_PATH = "kalinrent.db"

def add_apartment(apartment_data: Dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO apartments (title, description, price, district, rooms, photo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        apartment_data["title"],
        apartment_data["description"],
        apartment_data["price"],
        apartment_data["district"],
        apartment_data["rooms"],
        apartment_data.get("photo", None)  # Фото можно передавать или оставить пустым
    ))
    conn.commit()
    conn.close()

def delete_apartment(apartment_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM apartments WHERE id = ?", (apartment_id,))
    conn.commit()
    conn.close()

def find_apartments(filters: Dict) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM apartments WHERE 1=1"
    params = []

    if district := filters.get("district"):
        query += " AND district = ?"
        params.append(district)

    if price := filters.get("price"):
        if price == "до 5000":
            query += " AND price <= 5000"
        elif price == "5000-10000":
            query += " AND price BETWEEN 5000 AND 10000"
        elif price == "10000+":
            query += " AND price > 10000"

    if rooms := filters.get("rooms"):
        if rooms == "3+":
            query += " AND rooms >= 3"
        else:
            query += " AND rooms = ?"
            params.append(int(rooms))

    cursor.execute(query, params)
    apartments = cursor.fetchall()
    conn.close()

    return [dict(row) for row in apartments]
