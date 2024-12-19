import asyncio
from datetime import datetime
from database.db_manager import DatabaseManager
from database.schema import init_database
from collectors.market_collector import MarketDataCollector
from analysis.market_analyzer import MarketAnalyzer

class CryptoAnalysisSystem:
    def __init__(self):
        # Initialize database
        self.db_path = "market_data.db"
        init_database(self.db_path)
        
        # Initialize components
        self.db = DatabaseManager(self.db_path)
        self.collector = MarketDataCollector(self.db)
        self.analyzer = MarketAnalyzer(self.db)
        
        # Configuration
        self.symbols = [
            "bitcoin",
            "ethereum",
            "solana",
            "cardano",
            "polkadot"
        ]
        
    async def collect_data(self):
        """Collect market data for all tracked symbols"""
        print(f"[{datetime.now()}] Collecting market data...")
        await self.collector.collect_market_data(self.symbols)
        
    async def run_analysis(self):
        """Run market analysis for all symbols"""
        print(f"[{datetime.now()}] Running market analysis...")
        for symbol in self.symbols:
            analysis = self.analyzer.analyze_market_data(symbol)
            predictions = self.analyzer.generate_predictions(symbol)
            print(f"Analysis completed for {symbol}")
            
    async def run(self):
        """Main execution loop"""
        while True:
            try:
                await self.collect_data()
                await self.run_analysis()
                await asyncio.sleep(300)  # Wait 5 minutes before next update
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

if __name__ == "__main__":
    system = CryptoAnalysisSystem()
    asyncio.run(system.run())