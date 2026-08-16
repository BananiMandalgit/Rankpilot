export interface Recommendation {
  text: string;
}

export type AnalysisStatus = 'Ready for analysis';

export interface AnalysisResult {
  targetUrl: string;
  seoScore: number;
  aeoScore: number;
  issuesFound: number;
  status: AnalysisStatus;
  overview: string;
  recommendations: Recommendation[];
}

export const mockAnalysis: AnalysisResult = {
  targetUrl: 'https://example.com',
  seoScore: 78,
  aeoScore: 64,
  issuesFound: 9,
  status: 'Ready for analysis',
  overview:
    'Use this dashboard to stage website analysis results. The current version is a static frontend preview for the next module.',
  recommendations: [
    { text: 'Improve title tag uniqueness for key pages.' },
    { text: 'Add structured FAQ content for high-intent queries.' },
    { text: 'Increase internal links from blog posts to service pages.' },
    { text: 'Refine heading hierarchy for clearer answer extraction.' },
  ],
};
