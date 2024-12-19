import sqlite3
from datetime import datetime

def init_database(db_path: str = "market_data.db"):
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Market data table for storing real-time prices
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        price REAL NOT NULL,
        market_cap REAL,
        volume_24h REAL,
        timestamp INTEGER NOT NULL,
        UNIQUE(symbol, timestamp)
    )
    ''')

    # Technical indicators table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS technical_indicators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        sma_7 REAL,
        sma_25 REAL,
        sma_99 REAL,
        rsi_14 REAL,
        macd REAL,
        UNIQUE(symbol, timestamp)
    )
    ''')

    # AI predictions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        prediction_type TEXT NOT NULL,
        value REAL NOT NULL,
        confidence REAL NOT NULL,
        horizon TEXT NOT NULL,
        UNIQUE(symbol, timestamp, prediction_type)
    )
    ''')

    conn.commit()
    conn.close()