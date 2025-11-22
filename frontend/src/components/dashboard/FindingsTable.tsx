import { Finding, PaginatedResponse, Severity } from '@/types';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight, Eye } from 'lucide-react';
import { cn } from '@/lib/utils';

interface FindingsTableProps {
  response: PaginatedResponse<Finding> | null;
  loading: boolean;
  error?: string | null;
  onPageChange: (page: number) => void;
  onViewDetails: (finding: Finding) => void;
}

const severityConfig: Record<Severity, { bg: string; text: string; label: string }> = {
  low: { bg: 'bg-severity-low-bg', text: 'text-severity-low', label: 'Low' },
  medium: { bg: 'bg-severity-medium-bg', text: 'text-severity-medium', label: 'Medium' },
  high: { bg: 'bg-severity-high-bg', text: 'text-severity-high', label: 'High' },
  critical: { bg: 'bg-severity-critical-bg', text: 'text-severity-critical', label: 'Critical' },
};

export function FindingsTable({
  response,
  loading,
  error,
  onPageChange,
  onViewDetails,
}: FindingsTableProps) {
  if (loading) {
    return (
      <div className="rounded-xl border border-border bg-card p-8 text-center">
        <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
        <p className="mt-4 text-sm text-muted-foreground">Loading findings...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-border bg-card p-8 text-center">
        <p className="text-destructive">{error}</p>
        <Button onClick={() => onPageChange(1)} className="mt-4" variant="outline">
          Try again
        </Button>
      </div>
    );
  }

  if (!response || response.items.length === 0) {
    return (
      <div className="rounded-xl border border-border bg-card p-8 text-center">
        <p className="text-muted-foreground">No findings found</p>
      </div>
    );
  }

  const startItem = (response.page - 1) * response.page_size + 1;
  const endItem = Math.min(response.page * response.page_size, response.total);

  return (
    <div className="space-y-4">
      <div className="overflow-hidden rounded-xl border border-border bg-card shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-border bg-muted/50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">
                  Rule Name
                </th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">
                  Description
                </th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">
                  Severity
                </th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">
                  User
                </th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">
                  Created At
                </th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">
                  Risk Score
                </th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {response.items.map((finding) => {
                const severity = severityConfig[finding.severity];
                return (
                  <tr key={finding.id} className="transition-colors hover:bg-muted/30">
                    <td className="px-4 py-3 text-sm font-medium text-foreground">
                      {finding.rule_name}
                    </td>
                    <td className="max-w-md px-4 py-3 text-sm text-muted-foreground">
                      <div className="line-clamp-2">{finding.description}</div>
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={cn(
                          'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold',
                          severity.bg,
                          severity.text
                        )}
                      >
                        {severity.label}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">
                      {finding.user || '—'}
                    </td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">
                      {new Date(finding.created_at).toLocaleString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </td>
                    <td className="px-4 py-3 text-sm text-muted-foreground">
                      {finding.risk_score ?? '—'}
                    </td>
                    
                    <td className="px-4 py-3">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onViewDetails(finding)}
                        className="h-8"
                      >
                        <Eye className="mr-1 h-3.5 w-3.5" />
                        View
                      </Button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
        <p className="text-sm text-muted-foreground">
          Showing {startItem}–{endItem} of {response.total}
        </p>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onPageChange(response.page - 1)}
            disabled={response.page === 1}
          >
            <ChevronLeft className="mr-1 h-4 w-4" />
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => onPageChange(response.page + 1)}
            disabled={response.page * response.page_size >= response.total}
          >
            Next
            <ChevronRight className="ml-1 h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
