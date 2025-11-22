import { apiClient } from './client';
import { StatsSummary } from '../types';

export async function getStatsSummary(): Promise<StatsSummary> {
  return apiClient<StatsSummary>('/stats/summary');
}
