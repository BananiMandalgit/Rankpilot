import { FormEvent, useMemo, useState } from 'react';
import { MetricCard } from '../components/dashboard/MetricCard';
import { SectionTitle } from '../components/dashboard/SectionTitle';
import { AnalyzeResponse, analyzeWebsite } from '../services/analyze';

type AnalysisStatus = 'ready' | 'loading' | 'success' | 'error';
type Priority = 'High' | 'Medium' | 'Low';
type CheckState = 'pass' | 'fail' | 'info';

type IssueDetail = {
  title: string;
  priority: Priority;
  whyItMatters: string;
  howToFix: string;
  status: CheckState;
};

type RecommendationGroup = {
  issue: string;
  recommendations: string[];
};

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

function getScoreTone(score: number) {
  if (score >= 80) {
    return 'text-emerald-700';
  }
  if (score >= 50) {
    return 'text-amber-700';
  }
  return 'text-rose-700';
}

function getPriorityForIssue(issue: string, score: number): Priority {
  const normalized = issue.toLowerCase();
  if (
    normalized.includes('missing title') ||
    normalized.includes('missing meta description') ||
    normalized.includes('missing h1') ||
    normalized.includes('content is too short') ||
    normalized.includes('images missing alt')
  ) {
    return score < 60 ? 'High' : 'Medium';
  }

  if (normalized.includes('heading') || normalized.includes('faq') || normalized.includes('question')) {
    return 'Medium';
  }

  return 'Low';
}

function issueToGuidance(issue: string) {
  const normalized = issue.toLowerCase();

  if (normalized.includes('missing title')) {
    return {
      whyItMatters: 'A clear page title helps people understand the page quickly and makes search listings more useful.',
      howToFix: 'Add a unique page title that clearly describes the page topic and includes the main keyword where appropriate.',
    };
  }

  if (normalized.includes('missing meta description')) {
    return {
      whyItMatters: 'Without a meta description, the search snippet is less informative and can reduce click-through rates.',
      howToFix: 'Write a concise summary that explains the page value and matches the user intent behind the page.',
    };
  }

  if (normalized.includes('missing h1')) {
    return {
      whyItMatters: 'A strong H1 makes the page structure easier to understand for both users and search engines.',
      howToFix: 'Add a single, clear H1 that matches the page purpose and main topic.',
    };
  }

  if (normalized.includes('images missing alt')) {
    return {
      whyItMatters: 'Missing ALT text reduces accessibility and makes image content harder for screen-reader users to understand.',
      howToFix: 'Add descriptive ALT text for every meaningful image and keep it brief and relevant.',
    };
  }

  if (normalized.includes('content is too short')) {
    return {
      whyItMatters: 'Short pages often do not provide enough context or depth to satisfy user intent or rank well.',
      howToFix: 'Expand the page with useful detail, supporting information, and clear answers to the main audience questions.',
    };
  }

  if (normalized.includes('faq') || normalized.includes('q&a') || normalized.includes('questions and answers')) {
    return {
      whyItMatters: 'FAQ and Q&A patterns help answer direct customer questions and improve answer-oriented search visibility.',
      howToFix: 'Add a clear FAQ section or answer-first headings that address the main questions your audience is asking.',
    };
  }

  if (normalized.includes('heading structure') || normalized.includes('question-heading') || normalized.includes('question')) {
    return {
      whyItMatters: 'A well-structured page makes information easier to scan and helps answer engines understand the content flow.',
      howToFix: 'Organize the page with logical headings and answer-style sections that follow natural customer questions.',
    };
  }

  if (normalized.includes('structured data') || normalized.includes('json-ld')) {
    return {
      whyItMatters: 'Structured data helps search engines interpret the page type and content more clearly.',
      howToFix: 'Add relevant JSON-LD schema such as WebPage, Article, or FAQPage where the page supports it.',
    };
  }

  if (normalized.includes('freshness')) {
    return {
      whyItMatters: 'Freshness signals can help demonstrate that the content is current and maintained.',
      howToFix: 'Update published dates or revision metadata where relevant to show the page stays current.',
    };
  }

  return {
    whyItMatters: 'This issue can reduce clarity for both users and search engines, making the page less effective at serving intent.',
    howToFix: 'Review the page content and improve the relevant element with a clear, customer-focused update.',
  };
}

function getAeoChecks(issues: string[]) {
  const rows = [
    {
      label: 'Heading structure',
      matcher: /heading structure|clear heading/i,
      detail: 'Headings help users and search engines scan the page quickly.',
    },
    {
      label: 'Question-based content',
      matcher: /question-like|question-heading|question/i,
      detail: 'Answer-style sections are useful for customer questions and AEO.',
    },
    {
      label: 'Content depth',
      matcher: /content is short|300\+|word count/i,
      detail: 'Longer, useful content gives more room to answer customer needs.',
    },
    {
      label: 'FAQ / Q&A signals',
      matcher: /faq|q&a|questions and answers/i,
      detail: 'FAQ content helps pages answer common customer questions directly.',
    },
    {
      label: 'Structured data',
      matcher: /structured data|json-ld|webpage|article|faqpage|howto/i,
      detail: 'Schema markup helps answer engines understand page context.',
    },
    {
      label: 'Freshness signals',
      matcher: /freshness|dateModified|modified_time|<time datetime/i,
      detail: 'Freshness signals show the content remains relevant and maintained.',
    },
  ];

  return rows.map((check) => {
    const failed = issues.some((issue) => check.matcher.test(issue));
    return {
      ...check,
      status: failed ? 'fail' : 'pass',
      passLabel: failed ? 'Needs attention' : 'Passed',
    };
  });
}

function buildPageSummary(analysis: AnalyzeResponse | null) {
  if (!analysis) {
    return {
      url: 'Waiting for analysis',
      title: 'Not returned by current API',
      metaDescription: 'Not returned by current API',
      h1Count: 'Not returned by current API',
      images: 'Not returned by current API',
      missingAlt: 'Not returned by current API',
      wordCount: 'Not returned by current API',
    };
  }

  return {
    url: analysis.url,
    title: 'Not returned by current API',
    metaDescription: 'Not returned by current API',
    h1Count: 'Not returned by current API',
    images: 'Not returned by current API',
    missingAlt: 'Not returned by current API',
    wordCount: 'Not returned by current API',
  };
}

function toNormalizedIssueList(items: unknown[]) {
  return items.map(toDisplayText).map((text) => text.trim()).filter(Boolean);
}

function groupRecommendations(issues: string[], recommendations: string[]) {
  const issueKeys = issues.length > 0 ? issues : ['General recommendations'];

  const groups = new Map<string, RecommendationGroup>();
  issueKeys.forEach((issue) => {
    groups.set(issue, { issue, recommendations: [] });
  });

  recommendations.forEach((recommendation) => {
    const normalized = recommendation.trim();
    const match = issues.find((issue) =>
      normalized.toLowerCase().includes(issue.toLowerCase()) ||
      issue.toLowerCase().includes(normalized.toLowerCase().replace(/^fix:\s*/i, ''))
    );

    const key = match ?? 'General recommendations';
    const existing = groups.get(key) ?? { issue: key, recommendations: [] };
    existing.recommendations.push(normalized);
    groups.set(key, existing);
  });

  return Array.from(groups.values()).filter((group) => group.recommendations.length > 0 || group.issue === 'General recommendations');
}

export function HomePage() {
  const [url, setUrl] = useState('');
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [seoOpen, setSeoOpen] = useState(true);
  const [aeoOpen, setAeoOpen] = useState(true);
  const [recommendationsOpen, setRecommendationsOpen] = useState(true);
  const [crawlerOpen, setCrawlerOpen] = useState(false);

  const status: AnalysisStatus = loading ? 'loading' : error ? 'error' : analysis ? 'success' : 'ready';

  const statusText =
    status === 'loading'
      ? 'Analyzing...'
      : status === 'success'
        ? 'Analysis completed'
        : status === 'error'
          ? 'Analysis failed'
          : 'Ready to analyze';

  const issueItems = useMemo(() => {
    if (!analysis) {
      return [] as string[];
    }

    return toNormalizedIssueList(analysis.issues);
  }, [analysis]);

  const recommendationItems = useMemo(() => {
    if (!analysis) {
      return [] as string[];
    }

    return toNormalizedIssueList(analysis.recommendations);
  }, [analysis]);

  const recommendationGroups = useMemo(
    () => groupRecommendations(issueItems, recommendationItems),
    [issueItems, recommendationItems],
  );

  const issueDetails = useMemo<IssueDetail[]>(() => {
    if (!issueItems.length) {
      return [
        {
          title: 'No issues reported',
          priority: 'Low',
          whyItMatters: 'The current backend response did not identify any issues for the submitted page.',
          howToFix: 'Continue monitoring the page and re-run the analysis after future changes.',
          status: 'pass',
        },
      ];
    }

    return issueItems.map((issue) => ({
      title: issue,
      priority: 'Low',
      whyItMatters:
        'This issue indicates the page currently does not fully meet the quality standard described by the analysis result, which can reduce clarity for visitors and search systems.',
      howToFix:
        'Review the affected page content or structure and update the relevant element so it is clearer, more complete, and better aligned with user intent.',
      status: 'fail',
    }));
  }, [issueItems]);

  const pageSummary = useMemo(() => buildPageSummary(analysis), [analysis]);

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
    <section className="w-full py-6 lg:py-8">
      <div className="space-y-4 sm:space-y-5">
        <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
          <div className="space-y-3">
            <div className="inline-flex rounded-full border border-teal-200 bg-teal-50 px-3 py-1.5 text-[10px] font-semibold tracking-[0.22em] text-teal-900 uppercase">
              RankPilot analysis dashboard
            </div>
            <h1 className="max-w-3xl text-3xl leading-tight font-semibold tracking-tight text-slate-950 sm:text-4xl">
              Analyze a website for SEO and AEO readiness.
            </h1>
            <p className="max-w-2xl text-sm leading-6 text-slate-600 sm:text-base">
              Submit a URL to review the current SEO and AEO findings in a clear, customer-friendly dashboard.
            </p>
          </div>

          <form className="mt-4 grid gap-3 sm:grid-cols-[1fr_auto]" onSubmit={handleSubmit}>
            <label className="sr-only" htmlFor="website-url">
              Website URL
            </label>
            <input
              id="website-url"
              type="url"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://yourwebsite.com"
              className="w-full rounded-xl border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-teal-500 focus:ring-2 focus:ring-teal-100"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="rounded-xl bg-teal-700 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-teal-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-300"
            >
              {loading ? 'Analyzing...' : 'Analyze Website'}
            </button>
          </form>

          {error ? (
            <div className="mt-3 rounded-xl border border-rose-200 bg-rose-50 px-3.5 py-2.5 text-sm text-rose-700">
              {error}
            </div>
          ) : null}
        </section>

        {status === 'ready' ? (
          <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
            <SectionTitle
              title="Ready to review"
              description="Enter a website URL to start the SEO and AEO analysis."
            />
            <div className="mt-4 rounded-xl border border-dashed border-slate-300 bg-slate-50 px-3.5 py-4 text-sm leading-6 text-slate-600">
              The dashboard will display summary scores, issue details, and recommended actions once a backend analysis is returned.
            </div>
          </section>
        ) : null}

        {analysis ? (
          <>
            <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
              <SectionTitle title="Overview" description="Current backend scores and issue count, with a simple live status." />

              <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                <div className="rounded-2xl border border-emerald-200 bg-emerald-50/80 p-3.5">
                  <p className="text-[10px] font-semibold tracking-[0.2em] text-emerald-700 uppercase">SEO score</p>
                  <p className="mt-2 text-2xl font-semibold text-emerald-900 sm:text-3xl">{analysis.seo_score}/100</p>
                </div>
                <div className="rounded-2xl border border-teal-200 bg-teal-50/80 p-3.5">
                  <p className="text-[10px] font-semibold tracking-[0.2em] text-teal-700 uppercase">AEO score</p>
                  <p className="mt-2 text-2xl font-semibold text-teal-900 sm:text-3xl">{analysis.aeo_score}/100</p>
                </div>
                <div className="rounded-2xl border border-amber-200 bg-amber-50/80 p-3.5">
                  <p className="text-[10px] font-semibold tracking-[0.2em] text-amber-700 uppercase">Issues</p>
                  <p className="mt-2 text-2xl font-semibold text-amber-900 sm:text-3xl">{issueItems.length}</p>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3.5">
                  <p className="text-[10px] font-semibold tracking-[0.2em] text-slate-500 uppercase">Status</p>
                  <p className="mt-2 text-base font-semibold text-slate-900">{statusText}</p>
                  <p className="mt-1 text-[11px] text-slate-600">{analysis.url}</p>
                </div>
              </div>
            </section>

            <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
              <SectionTitle
                title="Priority"
                description="Frontend-inferred priority based on the available score and issue data. The backend does not return explicit priority values."
              />
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <div className="rounded-xl border border-slate-200 bg-slate-50 p-3.5">
                  <p className="text-[10px] font-semibold tracking-[0.2em] text-slate-500 uppercase">Suggested priority</p>
                  <p className={`mt-2 text-2xl font-semibold ${getScoreTone(analysis.seo_score)}`}>
                    {analysis.seo_score < 50 ? 'High' : analysis.seo_score < 80 ? 'Medium' : 'Low'}
                  </p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {analysis.seo_score < 50
                      ? 'Most important SEO issues are currently reducing page quality and visibility.'
                      : analysis.seo_score < 80
                        ? 'A few SEO items need attention, but the page is not severely impaired.'
                        : 'The page is generally healthy and only low-priority improvements remain.'}
                  </p>
                </div>
                <div className="rounded-xl border border-slate-200 bg-slate-50 p-3.5">
                  <p className="text-[10px] font-semibold tracking-[0.2em] text-slate-500 uppercase">Suggested priority</p>
                  <p className={`mt-2 text-2xl font-semibold ${getScoreTone(analysis.aeo_score)}`}>
                    {analysis.aeo_score < 50 ? 'High' : analysis.aeo_score < 80 ? 'Medium' : 'Low'}
                  </p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {analysis.aeo_score < 50
                      ? 'AEO coverage and answer structure need immediate attention.'
                      : analysis.aeo_score < 80
                        ? 'AEO is usable, but the page could answer customer questions more clearly.'
                        : 'AEO fundamentals are in good shape with only minor opportunities left.'}
                  </p>
                </div>
              </div>
            </section>

            <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
              <button
                type="button"
                onClick={() => setSeoOpen((open) => !open)}
                className="flex w-full items-center justify-between gap-3 text-left"
              >
                <SectionTitle
                  title="SEO Issues"
                  description="The backend returns the score and issue list; the suggested priority below is inferred from the score and issue type."
                />
                <span className="inline-flex items-center rounded-full border border-slate-200 bg-slate-100 px-2.5 py-1 text-[10px] font-semibold text-slate-700">
                  {seoOpen ? 'Hide' : 'Show'}
                </span>
              </button>

              {seoOpen ? (
                <div className="mt-4 space-y-3">
                  {issueDetails.length > 0 ? (
                    issueDetails.map((issue) => (
                      <div key={issue.title} className="rounded-2xl border border-slate-200 bg-slate-50 p-3.5">
                        <div className="space-y-3">
                          <div>
                            <p className="text-[10px] font-semibold tracking-[0.18em] text-slate-500 uppercase">What is wrong</p>
                            <p className="mt-1 text-sm font-semibold text-slate-900">{issue.title}</p>
                          </div>

                          <div>
                            <p className="text-[10px] font-semibold tracking-[0.18em] text-slate-500 uppercase">Why it matters</p>
                            <p className="mt-1 text-sm leading-6 text-slate-700">{issue.whyItMatters}</p>
                          </div>

                          <div>
                            <p className="text-[10px] font-semibold tracking-[0.18em] text-slate-500 uppercase">How to fix</p>
                            <p className="mt-1 text-sm leading-6 text-slate-700">{issue.howToFix}</p>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-3.5 py-2.5 text-sm text-emerald-800">
                      No SEO issues were returned for this page.
                    </div>
                  )}
                </div>
              ) : null}
            </section>

            <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
              <button
                type="button"
                onClick={() => setAeoOpen((open) => !open)}
                className="flex w-full items-center justify-between gap-3 text-left"
              >
                <SectionTitle
                  title="AEO Analysis"
                  description="The current API returns the overall AEO score and the issue list. Individual AEO check results are not currently returned by the API."
                />
                <span className="inline-flex items-center rounded-full border border-slate-200 bg-slate-100 px-2.5 py-1 text-[10px] font-semibold text-slate-700">
                  {aeoOpen ? 'Hide' : 'Show'}
                </span>
              </button>

              {aeoOpen ? (
                <div className="mt-4 space-y-3">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3.5">
                    <p className="text-[10px] font-semibold tracking-[0.18em] text-slate-500 uppercase">Current AEO score</p>
                    <p className="mt-2 text-2xl font-semibold text-slate-900 sm:text-3xl">{analysis.aeo_score}/100</p>
                  </div>

                  <div className="rounded-xl border border-amber-200 bg-amber-50 px-3.5 py-2.5 text-sm leading-6 text-amber-900">
                    Individual AEO check results are not currently returned by the API.
                  </div>

                  {issueItems.length > 0 ? (
                    <div className="space-y-2">
                      {issueItems.map((issue) => (
                        <div key={issue} className="rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5">
                          <p className="text-sm font-semibold text-slate-900">{issue}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-600">
                      No AEO issues were returned by the API.
                    </div>
                  )}
                </div>
              ) : null}
            </section>

            <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
              <button
                type="button"
                onClick={() => setRecommendationsOpen((open) => !open)}
                className="flex w-full items-center justify-between gap-3 text-left"
              >
                <SectionTitle
                  title="AI Recommendations"
                  description="Recommendations returned by the API are grouped with their related issue where possible."
                />
                <span className="inline-flex items-center rounded-full border border-slate-200 bg-slate-100 px-2.5 py-1 text-[10px] font-semibold text-slate-700">
                  {recommendationsOpen ? 'Hide' : 'Show'}
                </span>
              </button>

              {recommendationsOpen ? (
                <div className="mt-4 space-y-3">
                  {recommendationGroups.length > 0 ? (
                    recommendationGroups.map((group) => (
                      <div key={group.issue} className="rounded-2xl border border-slate-200 bg-slate-50 p-3.5">
                        {group.issue !== 'General recommendations' ? (
                          <>
                            <p className="text-[10px] font-semibold tracking-[0.2em] text-slate-500 uppercase">Related issue</p>
                            <p className="mt-2 text-base font-semibold text-slate-900">{group.issue}</p>
                          </>
                        ) : null}

                        <div className="mt-3 space-y-2">
                          {group.recommendations.map((recommendation) => (
                            <div key={recommendation} className="rounded-xl border border-slate-200 bg-white p-3.5">
                              <div className="space-y-2.5">
                                <div>
                                  <p className="text-[10px] font-semibold tracking-[0.18em] text-slate-500 uppercase">Why it matters</p>
                                  <p className="mt-1 text-sm leading-6 text-slate-700">
                                    This recommendation is part of the analysis output for the current page and addresses the identified issue in the result set.
                                  </p>
                                </div>

                                <div>
                                  <p className="text-[10px] font-semibold tracking-[0.18em] text-slate-500 uppercase">Recommendation</p>
                                  <p className="mt-1 text-sm leading-6 text-slate-800">{recommendation}</p>
                                </div>

                                <div>
                                  <p className="text-[10px] font-semibold tracking-[0.18em] text-slate-500 uppercase">Suggested implementation</p>
                                  <p className="mt-1 text-sm leading-6 text-slate-700">
                                    Apply this recommendation to the relevant page content, metadata, or structure and re-run the analysis after the update.
                                  </p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm text-slate-600">
                      No AI recommendations were returned for the current result.
                    </div>
                  )}
                </div>
              ) : null}
            </section>

            <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
              <button
                type="button"
                onClick={() => setCrawlerOpen((open) => !open)}
                className="flex w-full items-center justify-between gap-3 text-left"
              >
                <SectionTitle title="Crawler Details" description="The analyzed URL is displayed here; detailed crawler metrics are not currently returned by the analysis API." />
                <span className="inline-flex items-center rounded-full border border-slate-200 bg-slate-100 px-2.5 py-1 text-[10px] font-semibold text-slate-700">
                  {crawlerOpen ? 'Hide' : 'Show'}
                </span>
              </button>

              {crawlerOpen ? (
                <div className="mt-4 space-y-3">
                  <div className="rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5">
                    <p className="text-[10px] font-semibold tracking-[0.18em] text-slate-500 uppercase">Analyzed URL</p>
                    <p className="mt-2 text-sm font-medium text-slate-800">{analysis.url}</p>
                  </div>

                  <div className="rounded-xl border border-amber-200 bg-amber-50 px-3.5 py-2.5 text-sm leading-6 text-amber-900">
                    Detailed crawler metrics are not currently returned by the analysis API.
                  </div>

                  <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-3.5 py-3 text-sm leading-6 text-slate-600">
                    This section is ready for future crawler fields such as title, meta description, H1 count, image data, missing ALT text, word count, and HTTP status when the API begins returning them.
                  </div>
                </div>
              ) : null}
            </section>
          </>
        ) : null}

        {status === 'loading' ? (
          <section className="rounded-[1.5rem] border border-slate-200 bg-white/90 p-4 shadow-soft backdrop-blur sm:p-5">
            <SectionTitle title="Analysis in progress" description="The dashboard is loading results from the backend API." />
            <div className="mt-4 flex items-center gap-3 rounded-xl border border-teal-200 bg-teal-50 px-3.5 py-2.5 text-sm text-teal-800">
              <span className="inline-flex h-3 w-3 animate-pulse rounded-full bg-teal-500" />
              {statusText}
            </div>
          </section>
        ) : null}

        {status === 'error' && !analysis ? (
          <section className="rounded-[1.5rem] border border-rose-200 bg-rose-50/80 p-4 shadow-soft backdrop-blur sm:p-5">
            <SectionTitle title="Unable to complete the analysis" description="The request was rejected or the backend could not return a valid response." />
            <div className="mt-4 rounded-xl border border-rose-200 bg-white px-3.5 py-2.5 text-sm leading-6 text-rose-700">
              Please check the URL format and try again. If the issue continues, the backend may be unavailable or the page may not be reachable.
            </div>
          </section>
        ) : null}
      </div>
    </section>
  );
}