export interface MarketData {
  id: string;
  symbol: string;
  name: string;
  current_price: number;
  market_cap: number;
  total_volume: number;
  price_change_percentage_24h: number;
  sparkline_in_7d: {
    price: number[];
  };
}

export interface HistoricalData {
  prices: [number, number][];
  market_caps: [number, number][];
  total_volumes: [number, number][];
}

export interface MarketAnalysis {
  symbol: string;
  current_price: number;
  price_change: number;
  volatility: number;
  trend: 'bullish' | 'bearish' | 'neutral';
  support_resistance: {
    support: number;
    resistance: number;
  };
}

export interface PricePrediction {
  symbol: string;
  short_term: number;
  medium_term: number;
  long_term: number;
  confidence: number;
}