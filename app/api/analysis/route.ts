import { NextResponse } from 'next/server';
import { getHistoricalData } from '@/lib/market/api';
import { analyzeMarketData } from '@/lib/market/analysis';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get('symbol') || 'bitcoin';
  const days = parseInt(searchParams.get('days') || '7', 10);
  
  try {
    const historicalData = await getHistoricalData(symbol, days);
    const analysis = analyzeMarketData(symbol, historicalData);
    return NextResponse.json(analysis);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to analyze market data' },
      { status: 500 }
    );
  }
}