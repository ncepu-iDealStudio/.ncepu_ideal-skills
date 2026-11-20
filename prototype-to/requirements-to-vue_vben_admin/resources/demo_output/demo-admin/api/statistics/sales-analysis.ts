import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace StatisticsSalesAnalysisApi {
  export interface StatisticsSalesAnalysis {
    [key: string]: any;
    id: string;
    overview: string;
    trend: string;
    category: string;
  }
}

export async function getStatisticsSalesAnalysisList(params: Recordable<any>) {
  return requestClient.get<Array<StatisticsSalesAnalysisApi.StatisticsSalesAnalysis>>('/statistics/sales-analysis/list', { params });
}

export async function createStatisticsSalesAnalysis(data: Omit<StatisticsSalesAnalysisApi.StatisticsSalesAnalysis, 'id'>) {
  return requestClient.post('/statistics/sales-analysis', data);
}

export async function updateStatisticsSalesAnalysis(id: string, data: Omit<StatisticsSalesAnalysisApi.StatisticsSalesAnalysis, 'id'>) {
  return requestClient.put(`/statistics/sales-analysis/${id}`, data);
}

export async function deleteStatisticsSalesAnalysis(id: string) {
  return requestClient.delete(`/statistics/sales-analysis/${id}`);
}
