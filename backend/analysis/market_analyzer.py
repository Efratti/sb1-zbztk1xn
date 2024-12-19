import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from ..database.db_manager import DatabaseManager

class MarketAnalyzer:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def analyze_market_data(self, symbol: str, days: int = 7) -> Dict:
        """Analyze market data and return insights"""
        historical_data = self.db.get_historical_data(symbol, days)
        
        if not historical_data:
            return {"error": "No data available"}

        timestamps, prices, market_caps, volumes = zip(*historical_data)
        
        analysis = {
            "symbol": symbol,
            "current_price": prices[-1],
            "price_change": self._calculate_price_change(prices),
            "volatility": self._calculate_volatility(prices),
            "trend": self._determine_trend(prices),
            "volume_analysis": self._analyze_volume(volumes),
            "support_resistance": self._calculate_support_resistance(prices),
            "market_cap_analysis": self._analyze_market_cap(market_caps)
        }
        
        return analysis

    def generate_predictions(self, symbol: str) -> Dict:
        """Generate price predictions using historical data"""
        historical_data = self.db.get_historical_data(symbol, 30)
        
        if not historical_data:
            return {"error": "No data available"}

        timestamps, prices, _, _ = zip(*historical_data)
        
        predictions = {
            "symbol": symbol,
            "short_term": self._calculate_sma(prices, 7),
            "medium_term": self._calculate_sma(prices, 14),
            "long_term": self._calculate_sma(prices, 30),
            "confidence": self._calculate_prediction_confidence(prices)
        }
        
        # Store predictions in database
        for horizon, value in predictions.items():
            if horizon != "symbol":
                self.db.insert_prediction(
                    symbol=symbol,
                    prediction_type="price",
                    value=value,
                    confidence=predictions["confidence"],
                    horizon=horizon
                )
        
        return predictions

    def _calculate_price_change(self, prices: List[float]) -> float:
        """Calculate percentage price change"""
        if len(prices) < 2:
            return 0
        return ((prices[-1] - prices[0]) / prices[0]) * 100

    def _calculate_volatility(self, prices: List[float]) -> float:
        """Calculate price volatility"""
        returns = np.diff(prices) / prices[:-1]
        return np.std(returns) * np.sqrt(365) * 100

    def _determine_trend(self, prices: List[float]) -> str:
        """Determine price trend using multiple indicators"""
        sma_short = self._calculate_sma(prices, 7)
        sma_long = self._calculate_sma(prices, 25)
        
        if sma_short > sma_long:
            return "bullish"
        elif sma_short < sma_long:
            return "bearish"
        return "neutral"

    def _analyze_volume(self, volumes: List[float]) -> Dict:
        """Analyze trading volume patterns"""
        avg_volume = np.mean(volumes)
        recent_volume = np.mean(volumes[-3:])
        
        return {
            "average": avg_volume,
            "recent": recent_volume,
            "trend": "increasing" if recent_volume > avg_volume else "decreasing"
        }

    def _analyze_market_cap(self, market_caps: List[float]) -> Dict:
        """Analyze market capitalization trends"""
        return {
            "current": market_caps[-1],
            "change": ((market_caps[-1] - market_caps[0]) / market_caps[0]) * 100,
            "average": np.mean(market_caps)
        }

    def _calculate_support_resistance(self, prices: List[float]) -> Dict:
        """Calculate support and resistance levels using percentiles"""
        sorted_prices = sorted(prices)
        return {
            "support": np.percentile(sorted_prices, 25),
            "resistance": np.percentile(sorted_prices, 75)
        }

    def _calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return prices[-1]
        return np.mean(prices[-period:])

    def _calculate_prediction_confidence(self, prices: List[float]) -> float:
        """Calculate confidence level for predictions"""
        volatility = self._calculate_volatility(prices)
        return max(0, min(100, 100 - volatility))