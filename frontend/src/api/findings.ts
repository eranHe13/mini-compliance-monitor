import { apiClient } from './client';
import { Finding, FindingsFilters, PaginatedResponse } from '../types';


// =========================
//  GET findings (existing)
// =========================

export async function getFindings(
  page: number = 1,
  pageSize: number = 20,
  filters?: FindingsFilters
): Promise<PaginatedResponse<Finding>> {
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  });

  if (filters?.severity) params.append('severity', filters.severity);
  if (filters?.user) params.append('user', filters.user);
  if (filters?.from_date) params.append('from_date', filters.from_date);
  if (filters?.to_date) params.append('to_date', filters.to_date);

  return apiClient<PaginatedResponse<Finding>>(`/findings?${params.toString()}`);
}



// =========================
//  ENRICH SINGLE FINDING
// =========================

export async function enrichFinding(id: number): Promise<Finding> {
  return apiClient<Finding>(`/findings/${id}/enrich_with_ai`, {
    method: 'POST',
  });
}



// =========================
//  ENRICH ALL MISSING
// =========================

export async function enrichAllMissing(limit: number = 50): Promise<Finding[]> {
  return apiClient<Finding[]>(`/findings/enrich_all_missing?limit=${limit}`, {
    method: 'POST',
  });
}
