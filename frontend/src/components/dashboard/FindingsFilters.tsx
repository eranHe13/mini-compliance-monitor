import { FindingsFilters as Filters, Severity } from '@/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { X } from 'lucide-react';

interface FindingsFiltersProps {
  filters: Filters;
  onChange: (filters: Filters) => void;
}

export function FindingsFilters({ filters, onChange }: FindingsFiltersProps) {
  const handleSeverityChange = (value: string) => {
    onChange({
      ...filters,
      severity: value === 'all' ? undefined : (value as Severity),
    });
  };

  const handleUserChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange({
      ...filters,
      user: e.target.value || undefined,
    });
  };

  const handleFromDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange({
      ...filters,
      from_date: e.target.value || undefined,
    });
  };

  const handleToDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange({
      ...filters,
      to_date: e.target.value || undefined,
    });
  };

  const handleClearFilters = () => {
    onChange({});
  };

  const hasActiveFilters = filters.severity || filters.user || filters.from_date || filters.to_date;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end gap-4">
        <div className="w-full space-y-2 sm:w-auto sm:min-w-[180px]">
          <Label htmlFor="severity" className="text-sm font-medium">
            Severity
          </Label>
          <Select value={filters.severity || 'all'} onValueChange={handleSeverityChange}>
            <SelectTrigger id="severity">
              <SelectValue placeholder="All severities" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All severities</SelectItem>
              <SelectItem value="low">Low</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="high">High</SelectItem>
              <SelectItem value="critical">Critical</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="w-full space-y-2 sm:w-auto sm:min-w-[200px]">
          <Label htmlFor="user" className="text-sm font-medium">
            User
          </Label>
          <Input
            id="user"
            type="text"
            placeholder="Filter by user"
            value={filters.user || ''}
            onChange={handleUserChange}
          />
        </div>

        <div className="w-full space-y-2 sm:w-auto">
          <Label htmlFor="from_date" className="text-sm font-medium">
            From
          </Label>
          <Input
            id="from_date"
            type="date"
            value={filters.from_date || ''}
            onChange={handleFromDateChange}
          />
        </div>

        <div className="w-full space-y-2 sm:w-auto">
          <Label htmlFor="to_date" className="text-sm font-medium">
            To
          </Label>
          <Input
            id="to_date"
            type="date"
            value={filters.to_date || ''}
            onChange={handleToDateChange}
          />
        </div>

        {hasActiveFilters && (
          <Button
            variant="outline"
            size="default"
            onClick={handleClearFilters}
            className="w-full sm:w-auto"
          >
            <X className="mr-2 h-4 w-4" />
            Clear filters
          </Button>
        )}
      </div>
    </div>
  );
}
