const API_BASE = 'https://api.coingecko.com/api/v3';

export async function getTopCryptos(limit: number = 10): Promise<CryptoPrice[]> {
  const response = await fetch(
    `${API_BASE}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=${limit}&sparkline=false`
  );
  return response.json();
}

export async function getCryptoHistory(id: string, days: number = 7): Promise<ChartData[]> {
  const response = await fetch(
    `${API_BASE}/coins/${id}/market_chart?vs_currency=usd&days=${days}`
  );
  const data = await response.json();
  return data.prices.map(([timestamp, price]: [number, number]) => ({
    timestamp,
    price,
  }));
}