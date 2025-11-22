import { Shield } from 'lucide-react';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
      <div className="container flex h-16 items-center justify-between px-4 md:px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
            <Shield className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-foreground md:text-2xl">
              Mini Compliance Monitor
            </h1>
            <p className="text-xs text-muted-foreground">Real-time compliance tracking</p>
          </div>
        </div>
        <div className="rounded-full bg-muted px-3 py-1.5 text-xs font-medium text-muted-foreground">
          Demo Dashboard
        </div>
      </div>
    </header>
  );
}
