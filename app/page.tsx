import { Header } from '@/components/layout/header';
import { MarketOverview } from '@/components/dashboard/market-overview';
import { PriceChart } from '@/components/dashboard/price-chart';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-6 space-y-6">
        <MarketOverview />
        <PriceChart cryptoId="bitcoin" />
      </main>
    </div>
  );
}