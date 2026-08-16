import { http } from '../lib/http';

export interface AnalyzeResponse {
	url: string;
	seo_score: number;
	aeo_score: number;
	issues: unknown[];
	recommendations: unknown[];
}

export async function analyzeWebsite(url: string): Promise<AnalyzeResponse> {
	const response = await http.post<AnalyzeResponse>('/analyze', { url });
	return response.data;
}
