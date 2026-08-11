import { MetricCard } from '../components/dashboard/MetricCard';
import { RecommendationList } from '../components/dashboard/RecommendationList';
import { SectionTitle } from '../components/dashboard/SectionTitle';

const mockAnalysis = {
  targetUrl: 'https://example.com',
  seoScore: 78,
  aeoScore: 64,
  issuesFound: 9,
  status: 'Ready for analysis',
  overview:
    'Use this dashboard to stage website analysis results. The current version is a static frontend preview for the next module.',
  recommendations: [
    'Improve title tag uniqueness for key pages.',
    'Add structured FAQ content for high-intent queries.',
    'Increase internal links from blog posts to service pages.',
    'Refine heading hierarchy for clearer answer extraction.',
  ],
};

export function HomePage() {
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
            <p className="max-w-2xl text-base leading-7 text-slate-600">{mockAnalysis.overview}</p>
          </div>

          <form className="mt-6 grid gap-3 sm:grid-cols-[1fr_auto]" onSubmit={(event) => event.preventDefault()}>
            <label className="sr-only" htmlFor="website-url">
              Website URL
            </label>
            <input
              id="website-url"
              type="url"
              defaultValue={mockAnalysis.targetUrl}
              placeholder="https://yourwebsite.com"
              className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-teal-500 focus:ring-2 focus:ring-teal-100"
            />
            <button
              type="submit"
              className="rounded-xl bg-teal-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-teal-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-300"
            >
              Analyze Website
            </button>
          </form>
        </section>

        <section className="rounded-[2rem] border border-slate-200 bg-white/90 p-6 shadow-soft backdrop-blur sm:p-8">
          <SectionTitle title="Analysis Overview" description="A snapshot of the current mock analysis result for the submitted domain." />

          <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <MetricCard
              label="SEO score"
              value={`${mockAnalysis.seoScore}/100`}
              helperText="Core on-page SEO checks are mostly healthy with room for metadata refinement."
              tone="emerald"
            />
            <MetricCard
              label="AEO score"
              value={`${mockAnalysis.aeoScore}/100`}
              helperText="Answer-oriented structure needs stronger question-based content coverage."
              tone="teal"
            />
            <MetricCard
              label="Issues found"
              value={`${mockAnalysis.issuesFound}`}
              helperText="These include missing schema opportunities, heading depth, and link flow issues."
              tone="amber"
            />
          </div>
        </section>

        <section className="grid gap-5 lg:grid-cols-[1.3fr_0.7fr]">
          <article className="rounded-[2rem] border border-slate-200 bg-white/90 p-6 shadow-soft backdrop-blur sm:p-8">
            <SectionTitle
              title="Recommendations"
              description="Priority actions based on mock SEO/AEO findings."
            />
            <div className="mt-5">
              <RecommendationList items={mockAnalysis.recommendations} />
            </div>
          </article>

          <article className="rounded-[2rem] border border-slate-200 bg-white/90 p-6 shadow-soft backdrop-blur sm:p-8">
            <SectionTitle title="Analysis Status" description="Execution state for this initial static dashboard." />
            <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Current status</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{mockAnalysis.status}</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                Backend integration is intentionally disabled in this module. The UI currently uses static preview data.
              </p>
            </div>
          </article>
        </section>
      </div>
    </section>
  );
}