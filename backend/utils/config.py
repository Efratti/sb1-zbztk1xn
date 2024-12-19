class Config:
    def __init__(self):
        self.db_path = "market_data.db"
        self.api_keys = {
            "coingecko": None,  # Free tier doesn't require API key
        }
        self.supported_symbols = [
            "bitcoin",
            "ethereum",
            "solana",
            "cardano",
            "polkadot"
        ]
        self.update_interval = 300  # 5 minutes
        self.analysis_settings = {
            "sma_periods": [7, 14, 30],
            "volatility_window": 14,
            "prediction_confidence_threshold": 70
        }