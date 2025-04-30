# database/db.py

import sqlite3

def add_apartment(data):
    conn = sqlite3.connect("kalinrent.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO apartments (title, description, price, district, rooms, photo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        data["price"],
        data["district"],
        data["rooms"],
        data["photo"]
    ))
    conn.commit()
    conn.close()

def delete_apartment(apartment_id):
    conn = sqlite3.connect("kalinrent.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM apartments WHERE id = ?", (apartment_id,))
    conn.commit()
    conn.close()

def get_all_apartments():
    conn = sqlite3.connect("kalinrent.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apartments ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def find_apartments(filters: dict):
    conn = sqlite3.connect("kalinrent.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM apartments WHERE 1=1"
    params = []

    if filters.get("district"):
        query += " AND district = ?"
        params.append(filters["district"])

    if filters.get("price"):
        price_range = filters["price"]
        if price_range == "до 2000":
            query += " AND price <= 2000"
        elif price_range == "2000-3500":
            query += " AND price > 2000 AND price <= 3500"
        elif price_range == "3500-5000":
            query += " AND price > 3500 AND price <= 5000"
        elif price_range == "5000-10000":
            query += " AND price > 5000 AND price <= 10000"
        elif price_range == "10000+":
            query += " AND price > 10000"

    if filters.get("rooms"):
        rooms = filters["rooms"]
        if rooms == "1":
            query += " AND rooms = 1"
        elif rooms == "2":
            query += " AND rooms = 2"
        elif rooms == "3+":
            query += " AND rooms >= 3"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
