import { useEffect, useState } from 'react';
import { StatsSummary, Finding, FindingsFilters, PaginatedResponse } from '@/types';
import { getStatsSummary } from '@/api/stats';
import { getFindings } from '@/api/findings';
import { SummaryCards } from '@/components/dashboard/SummaryCards';
import { FindingsBySeverityChart } from '@/components/dashboard/FindingsBySeverityChart';
import { EventsOverTimeChart } from '@/components/dashboard/EventsOverTimeChart';
import { FindingsFilters as FindingsFiltersComponent } from '@/components/dashboard/FindingsFilters';
import { FindingsTable } from '@/components/dashboard/FindingsTable';
import { FindingDetailsModal } from '@/components/dashboard/FindingDetailsModal';
import { useToast } from '@/hooks/use-toast';
import { MOCK_STATS_SUMMARY, MOCK_FINDINGS_RESPONSE } from '@/mocks/demoData';
import { enrichAllMissing, enrichFinding } from '@/api/findings';
import { Button } from '@/components/ui/button';

// Toggle to use mock data instead of real API calls
const USE_MOCK_DATA = false;

export default function DashboardPage() {
  const { toast } = useToast();
  const [stats, setStats] = useState<StatsSummary | null>(null);
  const [filters, setFilters] = useState<FindingsFilters>({});
  const [findingsResponse, setFindingsResponse] = useState<PaginatedResponse<Finding> | null>(null);
  const [page, setPage] = useState(1);
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingFindings, setLoadingFindings] = useState(true);
  const [errorFindings, setErrorFindings] = useState<string | null>(null);
  const [selectedFinding, setSelectedFinding] = useState<Finding | null>(null);

  const pageSize = 20;

  // Fetch stats on mount
  useEffect(() => {
    async function fetchStats() {
      try {
        setLoadingStats(true);
        
        // Use mock data if enabled
        if (USE_MOCK_DATA) {
          // Simulate network delay for realistic UI behavior
          await new Promise(resolve => setTimeout(resolve, 500));
          setStats(MOCK_STATS_SUMMARY);
          setLoadingStats(false);
          return;
        }
        
        const data = await getStatsSummary();
        setStats(data);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
        toast({
          title: 'Error',
          description: 'Failed to load statistics. Please try again.',
          variant: 'destructive',
        });
      } finally {
        setLoadingStats(false);
      }
    }

    fetchStats();
  }, [toast]);

  // Fetch findings when filters or page changes
  useEffect(() => {
    async function fetchFindingsData() {
      try {
        setLoadingFindings(true);
        setErrorFindings(null);
        
        // Use mock data if enabled
        if (USE_MOCK_DATA) {
          // Simulate network delay for realistic UI behavior
          await new Promise(resolve => setTimeout(resolve, 300));
          setFindingsResponse(MOCK_FINDINGS_RESPONSE);
          setLoadingFindings(false);
          return;
        }
        
        const data = await getFindings(page, pageSize, filters);
        setFindingsResponse(data);
      } catch (error) {
        console.error('Failed to fetch findings:', error);
        setErrorFindings('Failed to load findings. Please try again.');
        toast({
          title: 'Error',
          description: 'Failed to load findings. Please try again.',
          variant: 'destructive',
        });
      } finally {
        setLoadingFindings(false);
      }
    }

    fetchFindingsData();
  }, [filters, page, toast]);

  const handleFiltersChange = (newFilters: FindingsFilters) => {
    setFilters(newFilters);
    setPage(1); // Reset to first page when filters change
  };

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleEnrichFinding = async (id: number) => {
    try {
      const updated = await enrichFinding(id);
      setFindingsResponse((prev) =>
        prev
          ? {
              ...prev,
              items: prev.items.map((f) =>
                f.id === updated.id ? updated : f
              ),
            }
          : prev
      );
      toast({
        title: 'Finding updated',
        description: `AI enrichment completed.`,
      });
    } catch (e) {
      toast({
        title: 'Error',
        description: 'Failed to enrich finding with AI.',
        variant: 'destructive',
      });
    }
  };

  const handleEnrichAllMissing = async () => {
  try {
    toast({
      title: 'Processing',
      description: 'Enriching all findings with AI...',
    });

    const updatedList = await enrichAllMissing(100); // limit=100

    if (!updatedList.length) {
      toast({
        title: 'No findings need enrichment',
        description: 'All findings already enriched.',
      });
      return;
    }

    setFindingsResponse((prev) =>
      prev
        ? {
            ...prev,
            items: prev.items.map((f) =>
              updatedList.find((u) => u.id === f.id) || f
            ),
          }
        : prev
    );

    toast({
      title: 'Completed',
      description: `Updated ${updatedList.length} findings with AI`,
    });
  } catch (e) {
    toast({
      title: 'Error',
      description: 'Failed to enrich findings with AI.',
      variant: 'destructive',
    });
  }
};

  const handleViewDetails = (finding: Finding) => {
    setSelectedFinding(finding);
  };

  const handleCloseModal = () => {
    setSelectedFinding(null);
  };

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <h2 className="text-3xl font-bold tracking-tight text-foreground">
          Compliance Dashboard
        </h2>
        <p className="text-muted-foreground">
          Monitor and analyze compliance findings 
        </p>
      </div>

      {loadingStats ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <div
              key={i}
              className="h-32 animate-pulse rounded-xl border border-border bg-card"
            />
          ))}
        </div>
      ) : stats ? (
        <SummaryCards stats={stats} />
      ) : null}

      {stats && (
        <div className="grid gap-6 lg:grid-cols-2">
          <FindingsBySeverityChart stats={stats} />
          <EventsOverTimeChart stats={stats} />
        </div>
      )}

      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-semibold text-foreground">Findings</h3>
          <Button variant="default" onClick={handleEnrichAllMissing}>
            Enrich All with AI
          </Button>
        </div>

        <FindingsFiltersComponent filters={filters} onChange={handleFiltersChange} />

        <FindingsTable
  response={findingsResponse}
  loading={loadingFindings}
  error={errorFindings}
  onPageChange={handlePageChange}
  onViewDetails={handleViewDetails}
  onEnrichFinding={handleEnrichFinding}
/>
      </div>

      <FindingDetailsModal finding={selectedFinding} onClose={handleCloseModal} />
    </div>
  );
}
