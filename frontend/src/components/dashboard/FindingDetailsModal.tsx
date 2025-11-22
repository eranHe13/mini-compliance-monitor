import { Finding, Severity } from '@/types';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { X, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface FindingDetailsModalProps {
  finding: Finding | null;
  onClose: () => void;
}

const severityConfig: Record<Severity, { bg: string; text: string; label: string }> = {
  low: { bg: 'bg-severity-low-bg', text: 'text-severity-low', label: 'Low' },
  medium: { bg: 'bg-severity-medium-bg', text: 'text-severity-medium', label: 'Medium' },
  high: { bg: 'bg-severity-high-bg', text: 'text-severity-high', label: 'High' },
  critical: { bg: 'bg-severity-critical-bg', text: 'text-severity-critical', label: 'Critical' },
};

export function FindingDetailsModal({ finding, onClose }: FindingDetailsModalProps) {
  if (!finding) return null;

  const severity = severityConfig[finding.severity];

  return (
    <Dialog open={!!finding} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-start justify-between">
            <span className="pr-8 text-xl">{finding.rule_name}</span>
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          <div className="flex flex-wrap items-center gap-4">
            <span
              className={cn(
                'inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold',
                severity.bg,
                severity.text
              )}
            >
              {severity.label} Severity
            </span>
            {finding.risk_score !== null && finding.risk_score !== undefined && (
              <div className="flex items-center gap-2 rounded-lg bg-muted px-3 py-1">
                <AlertCircle className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm font-medium">
                  Risk Score: {finding.risk_score}
                </span>
              </div>
            )}
          </div>

          <div className="space-y-2">
            <h4 className="text-sm font-medium text-muted-foreground">Created At</h4>
            <p className="text-foreground">
              {new Date(finding.created_at).toLocaleString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              })}
            </p>
          </div>

          {finding.user && (
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-muted-foreground">User</h4>
              <p className="text-foreground">{finding.user}</p>
            </div>
          )}

          <div className="space-y-2">
            <h4 className="text-sm font-medium text-muted-foreground">Description</h4>
            <p className="text-foreground leading-relaxed">{finding.description}</p>
          </div>

          <div className="space-y-2 rounded-lg border border-border bg-muted/30 p-4">
            <h4 className="flex items-center gap-2 text-sm font-medium text-foreground">
              <AlertCircle className="h-4 w-4 text-primary" />
              AI Explanation
            </h4>
            {finding.ai_explanation ? (
              <p className="text-sm text-muted-foreground leading-relaxed">
                {finding.ai_explanation}
              </p>
            ) : (
              <p className="text-sm italic text-muted-foreground">
                No AI explanation available yet.
              </p>
            )}
          </div>

          <div className="flex justify-end">
            <Button onClick={onClose}>Close</Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
