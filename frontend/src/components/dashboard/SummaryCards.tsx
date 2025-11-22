import { StatsSummary } from '@/types';
import { TrendingUp, AlertTriangle, Activity, AlertCircle } from 'lucide-react';

interface SummaryCardsProps {
  stats: StatsSummary;
}

export function SummaryCards({ stats }: SummaryCardsProps) {
  const highAndCritical = stats.findings_by_severity.high + stats.findings_by_severity.critical;
  const lowAndMedium = stats.findings_by_severity.low + stats.findings_by_severity.medium;

  const cards = [
    {
      label: 'Total Events',
      value: stats.total_events.toLocaleString(),
      icon: Activity,
      description: 'Events processed',
    },
    {
      label: 'Total Findings',
      value: stats.total_findings.toLocaleString(),
      icon: TrendingUp,
      description: 'Compliance findings',
    },
    {
      label: 'High & Critical',
      value: highAndCritical.toLocaleString(),
      icon: AlertCircle,
      description: 'Urgent attention required',
      highlight: highAndCritical > 0,
    },
    {
      label: 'Low & Medium',
      value: lowAndMedium.toLocaleString(),
      icon: AlertTriangle,
      description: 'Review recommended',
    },
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div
            key={card.label}
            className="group relative overflow-hidden rounded-xl border border-border bg-card p-6 shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:shadow-md"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-muted-foreground">{card.label}</p>
                <p className="mt-2 text-3xl font-semibold text-foreground md:text-4xl">
                  {card.value}
                </p>
                <p className="mt-1 text-xs text-muted-foreground">{card.description}</p>
              </div>
              <div
                className={`rounded-lg p-2 ${
                  card.highlight
                    ? 'bg-severity-critical-bg text-severity-critical'
                    : 'bg-primary/10 text-primary'
                }`}
              >
                <Icon className="h-5 w-5" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
