import { MarketData, HistoricalData } from './types';

const COINGECKO_API = 'https://api.coingecko.com/api/v3';

export async function getMarketData(symbol: string): Promise<MarketData> {
  const response = await fetch(
    `${COINGECKO_API}/coins/markets?vs_currency=usd&ids=${symbol}&sparkline=true`
  );
  const data = await response.json();
  return data[0];
}

export async function getHistoricalData(
  symbol: string,
  days: number = 7
): Promise<HistoricalData> {
  const response = await fetch(
    `${COINGECKO_API}/coins/${symbol}/market_chart?vs_currency=usd&days=${days}`
  );
  return response.json();
}