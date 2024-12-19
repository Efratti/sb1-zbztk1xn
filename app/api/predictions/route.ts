import { NextResponse } from 'next/server';
import { getHistoricalData } from '@/lib/market/api';
import { generatePredictions } from '@/lib/market/analysis';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get('symbol') || 'bitcoin';
  
  try {
    const historicalData = await getHistoricalData(symbol, 30);
    const predictions = generatePredictions(symbol, historicalData);
    return NextResponse.json(predictions);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to generate predictions' },
      { status: 500 }
    );
  }
}