import { MarketAnalysis, PricePrediction, HistoricalData } from './types';

export function analyzeMarketData(
  symbol: string,
  historicalData: HistoricalData
): MarketAnalysis {
  const prices = historicalData.prices.map(([, price]) => price);
  const currentPrice = prices[prices.length - 1];
  const initialPrice = prices[0];
  
  const priceChange = ((currentPrice - initialPrice) / initialPrice) * 100;
  const volatility = calculateVolatility(prices);
  const trend = determineTrend(prices);
  const supportResistance = calculateSupportResistance(prices);

  return {
    symbol,
    current_price: currentPrice,
    price_change: priceChange,
    volatility,
    trend,
    support_resistance: supportResistance
  };
}

export function generatePredictions(
  symbol: string,
  historicalData: HistoricalData
): PricePrediction {
  const prices = historicalData.prices.map(([, price]) => price);
  
  return {
    symbol,
    short_term: calculateSMA(prices, 7),
    medium_term: calculateSMA(prices, 14),
    long_term: calculateSMA(prices, 30),
    confidence: calculateConfidence(prices)
  };
}

function calculateVolatility(prices: number[]): number {
  const returns = prices.slice(1).map((price, i) => 
    (price - prices[i]) / prices[i]
  );
  return (standardDeviation(returns) * Math.sqrt(365)) * 100;
}

function determineTrend(prices: number[]): 'bullish' | 'bearish' | 'neutral' {
  const sma7 = calculateSMA(prices, 7);
  const sma14 = calculateSMA(prices, 14);
  
  if (sma7 > sma14) return 'bullish';
  if (sma7 < sma14) return 'bearish';
  return 'neutral';
}

function calculateSupportResistance(prices: number[]) {
  const sortedPrices = [...prices].sort((a, b) => a - b);
  return {
    support: percentile(sortedPrices, 25),
    resistance: percentile(sortedPrices, 75)
  };
}

function calculateSMA(prices: number[], period: number): number {
  if (prices.length < period) return prices[prices.length - 1];
  const slice = prices.slice(-period);
  return slice.reduce((sum, price) => sum + price, 0) / period;
}

function calculateConfidence(prices: number[]): number {
  const volatility = calculateVolatility(prices);
  return Math.max(0, Math.min(100, 100 - volatility));
}

function standardDeviation(values: number[]): number {
  const avg = values.reduce((sum, val) => sum + val, 0) / values.length;
  const squareDiffs = values.map(value => Math.pow(value - avg, 2));
  return Math.sqrt(squareDiffs.reduce((sum, val) => sum + val, 0) / values.length);
}

function percentile(values: number[], p: number): number {
  const index = Math.ceil((p / 100) * values.length) - 1;
  return values[index];
}