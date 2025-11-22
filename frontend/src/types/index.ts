export type Severity = 'low' | 'medium' | 'high' | 'critical';

export interface Event {
  id: number;
  source: string;
  event_type: string;
  user: string | null;
  created_at: string;
  raw_data?: Record<string, unknown>;
}

export interface Finding {
  id: number;
  rule_name: string;
  description: string;
  severity: Severity;
  user: string | null;
  created_at: string;
  risk_score?: number | null;
  ai_explanation?: string | null;
}

export interface StatsSummary {
  total_events: number;
  total_findings: number;
  findings_by_severity: {
    low: number;
    medium: number;
    high: number;
    critical: number;
  };
  events_over_time: Array<{
    date: string;
    count: number;
  }>;
}

export interface FindingsFilters {
  severity?: Severity;
  user?: string;
  from_date?: string;
  to_date?: string;
}

export interface EventsFilters {
  user?: string;
  event_type?: string;
  from_date?: string;
  to_date?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}
