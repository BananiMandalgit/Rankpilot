import { http } from '../lib/http';

export interface BackendHealthResponse {
  status: string;
  service: string;
  environment: string;
}

export async function getBackendHealth(): Promise<BackendHealthResponse> {
  const response = await http.get<BackendHealthResponse>('/health');
  return response.data;
}