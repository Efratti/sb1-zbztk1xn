'use client';

import { LineChart, Wallet2, Settings } from 'lucide-react';
import { ModeToggle } from '@/components/mode-toggle';
import { Button } from '@/components/ui/button';

export function Header() {
  return (
    <header className="border-b">
      <div className="flex h-16 items-center px-4 container mx-auto">
        <div className="flex items-center gap-2 font-bold text-xl">
          <LineChart className="h-6 w-6" />
          <span>CryptoAI</span>
        </div>
        <nav className="flex items-center space-x-4 lg:space-x-6 mx-6">
          <Button variant="ghost" className="text-sm font-medium transition-colors">
            Dashboard
          </Button>
          <Button variant="ghost" className="text-sm font-medium transition-colors">
            Markets
          </Button>
          <Button variant="ghost" className="text-sm font-medium transition-colors">
            Analysis
          </Button>
          <Button variant="ghost" className="text-sm font-medium transition-colors">
            Portfolio
          </Button>
        </nav>
        <div className="ml-auto flex items-center space-x-4">
          <Button variant="ghost" size="icon">
            <Wallet2 className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <Settings className="h-5 w-5" />
          </Button>
          <ModeToggle />
        </div>
      </div>
    </header>
  );
}