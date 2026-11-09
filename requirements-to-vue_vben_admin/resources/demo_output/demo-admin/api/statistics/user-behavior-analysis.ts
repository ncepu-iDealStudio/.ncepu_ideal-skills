import type { Recordable } from '@vben/types';

import { requestClient } from '#/api/request';

export namespace StatisticsUserBehaviorAnalysisApi {
  export interface StatisticsUserBehaviorAnalysis {
    [key: string]: any;
    id: string;
    overview: string;
    trend: string;
    category: string;
  }
}

export async function getStatisticsUserBehaviorAnalysisList(params: Recordable<any>) {
  return requestClient.get<Array<StatisticsUserBehaviorAnalysisApi.StatisticsUserBehaviorAnalysis>>('/statistics/user-behavior-analysis/list', { params });
}

export async function createStatisticsUserBehaviorAnalysis(data: Omit<StatisticsUserBehaviorAnalysisApi.StatisticsUserBehaviorAnalysis, 'id'>) {
  return requestClient.post('/statistics/user-behavior-analysis', data);
}

export async function updateStatisticsUserBehaviorAnalysis(id: string, data: Omit<StatisticsUserBehaviorAnalysisApi.StatisticsUserBehaviorAnalysis, 'id'>) {
  return requestClient.put(`/statistics/user-behavior-analysis/${id}`, data);
}

export async function deleteStatisticsUserBehaviorAnalysis(id: string) {
  return requestClient.delete(`/statistics/user-behavior-analysis/${id}`);
}
