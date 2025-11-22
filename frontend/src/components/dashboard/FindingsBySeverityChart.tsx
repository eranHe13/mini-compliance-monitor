import { StatsSummary } from '@/types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface FindingsBySeverityChartProps {
  stats: StatsSummary;
}

export function FindingsBySeverityChart({ stats }: FindingsBySeverityChartProps) {
  const data = [
    { severity: 'Low', count: stats.findings_by_severity.low, fill: 'hsl(var(--severity-low))' },
    { severity: 'Medium', count: stats.findings_by_severity.medium, fill: 'hsl(var(--severity-medium))' },
    { severity: 'High', count: stats.findings_by_severity.high, fill: 'hsl(var(--severity-high))' },
    { severity: 'Critical', count: stats.findings_by_severity.critical, fill: 'hsl(var(--severity-critical))' },
  ];

  return (
    <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-foreground">Findings by Severity</h3>
      <ResponsiveContainer width="100%" height={288}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis
            dataKey="severity"
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'hsl(var(--popover))',
              border: '1px solid hsl(var(--border))',
              borderRadius: '0.5rem',
            }}
            labelStyle={{ color: 'hsl(var(--foreground))' }}
            itemStyle={{ color: 'hsl(var(--foreground))' }}
          />
          <Bar dataKey="count" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
