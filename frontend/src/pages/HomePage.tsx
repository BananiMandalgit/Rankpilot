import { FormEvent, useMemo, useState } from 'react';
import { MetricCard } from '../components/dashboard/MetricCard';
import { RecommendationList } from '../components/dashboard/RecommendationList';
import { SectionTitle } from '../components/dashboard/SectionTitle';
import { AnalyzeResponse, analyzeWebsite } from '../services/analyze';

type AnalysisStatus = 'ready' | 'loading' | 'success' | 'error';

function toDisplayText(item: unknown): string {
  if (typeof item === 'string') {
    return item;
  }

  if (item && typeof item === 'object') {
    if ('text' in item && typeof item.text === 'string') {
      return item.text;
    }
    if ('message' in item && typeof item.message === 'string') {
      return item.message;
    }

    try {
      return JSON.stringify(item);
    } catch {
      return 'Unsupported item format';
    }
  }

  return String(item);
}

export function HomePage() {
  const [url, setUrl] = useState('');
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const status: AnalysisStatus = loading ? 'loading' : error ? 'error' : analysis ? 'success' : 'ready';

  const statusText =
    status === 'loading'
      ? 'Analyzing...'
      : status === 'success'
        ? 'Analysis completed'
        : status === 'error'
          ? 'Analysis failed'
          : 'Ready to analyze';

  const recommendationItems = useMemo(() => {
    if (!analysis) {
      return [];
    }

    return analysis.recommendations.map(toDisplayText);
  }, [analysis]);

  const issueItems = useMemo(() => {
    if (!analysis) {
      return [];
    }

    return analysis.issues.map(toDisplayText);
  }, [analysis]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (loading) {
      return;
    }

    const trimmedUrl = url.trim();

    if (!trimmedUrl) {
      setError('Please enter a website URL.');
      return;
    }

    try {
      const parsedUrl = new URL(trimmedUrl);
      if (parsedUrl.protocol !== 'http:' && parsedUrl.protocol !== 'https:') {
        throw new Error('Unsupported protocol');
      }
    } catch {
      setError('Please enter a valid HTTP or HTTPS URL.');
      return;
    }


    setLoading(true);
    setError(null);

    try {
      const response = await analyzeWebsite(trimmedUrl);
      setAnalysis(response);
    } catch {
      setError('Unable to complete analysis right now. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="w-full py-10 lg:py-14">
      <div className="space-y-8">
        <section className="rounded-[2rem] border border-slate-200 bg-white/90 p-6 shadow-soft backdrop-blur sm:p-8">
          <div className="space-y-5">
            <div className="inline-flex rounded-full border border-teal-200 bg-teal-50 px-4 py-2 text-xs font-semibold tracking-[0.24em] text-teal-900 uppercase">
              RankPilot analysis dashboard
            </div>
            <h1 className="max-w-3xl text-4xl leading-tight font-semibold tracking-tight text-slate-950 sm:text-5xl">
              Analyze a website for SEO and AEO readiness.
            </h1>
            <p className="max-w-2xl text-base leading-7 text-slate-600">
              Submit a URL to run backend analysis and view live SEO and AEO response data.
            </p>
          </div>

          <form className="mt-6 grid gap-3 sm:grid-cols-[1fr_auto]" onSubmit={handleSubmit}>
            <label className="sr-only" htmlFor="website-url">
              Website URL
            </label>
            <input
              id="website-url"
              type="url"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://yourwebsite.com"
              className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-teal-500 focus:ring-2 focus:ring-teal-100"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="rounded-xl bg-teal-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-teal-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-300"
            >
              {loading ? 'Analyzing...' : 'Analyze Website'}
            </button>
          </form>
          {error ? <p className="mt-3 text-sm font-medium text-rose-700">{error}</p> : null}
        </section>

        <section className="rounded-[2rem] border border-slate-200 bg-white/90 p-6 shadow-soft backdrop-blur sm:p-8">
          <SectionTitle title="Analysis Overview" description="A snapshot of the current backend analysis result for the submitted domain." />

          <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <MetricCard
              label="SEO score"
              value={analysis ? `${analysis.seo_score}/100` : '--'}
              helperText="Core on-page SEO checks are mostly healthy with room for metadata refinement."
              tone="emerald"
            />
            <MetricCard
              label="AEO score"
              value={analysis ? `${analysis.aeo_score}/100` : '--'}
              helperText="Answer-oriented structure needs stronger question-based content coverage."
              tone="teal"
            />
            <MetricCard
              label="Issues found"
              value={analysis ? `${analysis.issues.length}` : '--'}
              helperText="These include missing schema opportunities, heading depth, and link flow issues."
              tone="amber"
            />
          </div>
          {analysis ? (
            <p className="mt-4 text-sm leading-6 text-slate-600">
              URL: <span className="font-medium text-slate-900">{analysis.url}</span>
            </p>
          ) : null}
        </section>

        <section className="grid gap-5 lg:grid-cols-[1.3fr_0.7fr]">
          <article className="rounded-[2rem] border border-slate-200 bg-white/90 p-6 shadow-soft backdrop-blur sm:p-8">
            <SectionTitle
              title="Recommendations"
              description="Priority actions based on backend SEO/AEO findings."
            />
            <div className="mt-5">
              {analysis ? (
                recommendationItems.length > 0 ? (
                  <RecommendationList items={recommendationItems} />
                ) : (
                  <p className="rounded-xl border border-slate-200 bg-white/80 px-4 py-3 text-sm leading-6 text-slate-700">
                    No recommendations were returned.
                  </p>
                )
              ) : (
                <p className="rounded-xl border border-slate-200 bg-white/80 px-4 py-3 text-sm leading-6 text-slate-700">
                  Run an analysis to view recommendations.
                </p>
              )}
            </div>
          </article>

          <article className="rounded-[2rem] border border-slate-200 bg-white/90 p-6 shadow-soft backdrop-blur sm:p-8">
            <SectionTitle title="Analysis Status" description="Execution state for this dashboard." />
            <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Current status</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{statusText}</p>
              {analysis ? (
                <div className="mt-3">
                  <p className="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Issues</p>
                  {issueItems.length > 0 ? (
                    <ul className="mt-2 space-y-2">
                      {issueItems.map((issue, index) => (
                        <li key={`issue-${index}`} className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm leading-6 text-slate-700">
                          {issue}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="mt-2 text-sm leading-6 text-slate-600">No issues were returned.</p>
                  )}
                </div>
              ) : (
                <p className="mt-2 text-sm leading-6 text-slate-600">Run an analysis to view issues.</p>
              )}
            </div>
          </article>
        </section>
      </div>
    </section>
  );
}