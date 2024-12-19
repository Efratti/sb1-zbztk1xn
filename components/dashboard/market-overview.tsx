'use client';

import { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { LineChart, TrendingUp, Activity } from 'lucide-react';
import { CryptoPrice } from '@/lib/types/market';
import { getTopCryptos } from '@/lib/api/market';
import { formatCurrency, formatPercentage } from '@/lib/utils/format';

export function MarketOverview() {
  const [marketData, setMarketData] = useState<CryptoPrice | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getTopCryptos(1);
        setMarketData(data[0]);
      } catch (error) {
        console.error('Failed to fetch market data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  if (!marketData) return null;

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <Card className="p-6">
        <div className="flex items-center gap-2">
          <LineChart className="h-5 w-5 text-primary" />
          <h3 className="font-semibold">Market Overview</h3>
        </div>
        <div className="mt-4">
          <p className="text-2xl font-bold">{formatCurrency(marketData.current_price)}</p>
          <p className="text-sm text-muted-foreground">{marketData.name} Price</p>
        </div>
      </Card>
      <Card className="p-6">
        <div className="flex items-center gap-2">
          <TrendingUp className="h-5 w-5 text-primary" />
          <h3 className="font-semibold">24h Change</h3>
        </div>
        <div className="mt-4">
          <p className={`text-2xl font-bold ${marketData.price_change_percentage_24h >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {formatPercentage(marketData.price_change_percentage_24h)}
          </p>
          <p className="text-sm text-muted-foreground">Price Change</p>
        </div>
      </Card>
      <Card className="p-6">
        <div className="flex items-center gap-2">
          <Activity className="h-5 w-5 text-primary" />
          <h3 className="font-semibold">Market Cap</h3>
        </div>
        <div className="mt-4">
          <p className="text-2xl font-bold">{formatCurrency(marketData.market_cap)}</p>
          <p className="text-sm text-muted-foreground">Total Value</p>
        </div>
      </Card>
    </div>
  );
}