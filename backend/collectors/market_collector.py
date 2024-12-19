import time
from datetime import datetime
from typing import Dict, List
import json
from urllib.request import urlopen, Request
from ..database.db_manager import DatabaseManager

class MarketDataCollector:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.base_url = "https://api.coingecko.com/api/v3"
        self.update_interval = 300  # 5 minutes

    async def collect_market_data(self, symbols: List[str]) -> Dict:
        """Collect and store market data for specified symbols"""
        data = {}
        for symbol in symbols:
            try:
                url = f"{self.base_url}/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(req)
                market_data = json.loads(response.read())
                
                if symbol in market_data:
                    price = market_data[symbol]['usd']
                    market_cap = market_data[symbol]['usd_market_cap']
                    volume = market_data[symbol]['usd_24h_vol']
                    
                    # Store in database
                    self.db.insert_market_data(
                        symbol=symbol,
                        price=price,
                        market_cap=market_cap,
                        volume_24h=volume
                    )
                    
                    data[symbol] = market_data[symbol]
            
            except Exception as e:
                print(f"Error collecting data for {symbol}: {str(e)}")
        
        return data

    async def collect_historical_data(self, symbol: str, days: int = 30) -> List[Dict]:
        """Collect and store historical price data"""
        try:
            url = f"{self.base_url}/coins/{symbol}/market_chart?vs_currency=usd&days={days}"
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(req)
            data = json.loads(response.read())
            
            # Store historical data points
            for timestamp, price in data['prices']:
                market_cap = next((mc[1] for mc in data['market_caps'] if mc[0] == timestamp), None)
                volume = next((vol[1] for vol in data['total_volumes'] if vol[0] == timestamp), None)
                
                self.db.insert_market_data(
                    symbol=symbol,
                    price=price,
                    market_cap=market_cap,
                    volume_24h=volume,
                    timestamp=int(timestamp/1000)  # Convert milliseconds to seconds
                )
            
            return data
        except Exception as e:
            print(f"Error collecting historical data for {symbol}: {str(e)}")
            return []