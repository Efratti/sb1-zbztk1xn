import sqlite3
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_path: str = "market_data.db"):
        self.db_path = db_path

    def insert_market_data(self, symbol: str, price: float, market_cap: float, 
                          volume_24h: float, timestamp: Optional[int] = None) -> None:
        """Insert market data into database"""
        if timestamp is None:
            timestamp = int(datetime.now().timestamp())

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT OR REPLACE INTO market_data 
            (symbol, price, market_cap, volume_24h, timestamp)
            VALUES (?, ?, ?, ?, ?)
            ''', (symbol, price, market_cap, volume_24h, timestamp))
            conn.commit()
        except Exception as e:
            print(f"Error inserting market data: {str(e)}")
        finally:
            conn.close()

    def get_historical_data(self, symbol: str, days: int = 30) -> List[Tuple]:
        """Retrieve historical market data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        start_time = int((datetime.now() - timedelta(days=days)).timestamp())
        
        cursor.execute('''
        SELECT timestamp, price, market_cap, volume_24h 
        FROM market_data 
        WHERE symbol = ? AND timestamp >= ?
        ORDER BY timestamp ASC
        ''', (symbol, start_time))
        
        data = cursor.fetchall()
        conn.close()
        return data

    def insert_prediction(self, symbol: str, prediction_type: str, 
                         value: float, confidence: float, 
                         horizon: str) -> None:
        """Insert AI prediction into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = int(datetime.now().timestamp())

        try:
            cursor.execute('''
            INSERT OR REPLACE INTO predictions 
            (symbol, timestamp, prediction_type, value, confidence, horizon)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (symbol, timestamp, prediction_type, value, confidence, horizon))
            conn.commit()
        except Exception as e:
            print(f"Error inserting prediction: {str(e)}")
        finally:
            conn.close()

    def get_latest_predictions(self, symbol: str) -> Dict:
        """Get latest predictions for a symbol"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT prediction_type, value, confidence, horizon
        FROM predictions 
        WHERE symbol = ? 
        AND timestamp = (
            SELECT MAX(timestamp) 
            FROM predictions 
            WHERE symbol = ?
        )
        ''', (symbol, symbol))
        
        predictions = cursor.fetchall()
        conn.close()

        return {
            pred[0]: {
                'value': pred[1],
                'confidence': pred[2],
                'horizon': pred[3]
            } for pred in predictions
        }