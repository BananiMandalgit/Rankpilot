import { useEffect, useState } from 'react';
import { getBackendHealth } from '../services/backendHealth';

type HealthState = 'loading' | 'connected' | 'unavailable';

const foundationItems = [
  {
    title: 'Frontend shell',
    description: 'React, TypeScript, Tailwind CSS, routing, and API wiring are ready for future screens.',
  },
  {
    title: 'Backend shell',
    description: 'FastAPI, Pydantic, and SQLAlchemy are structured for a clean service-first API layer.',
  },
  {
    title: 'Crawler shell',
    description: 'Playwright and BeautifulSoup will be introduced later when crawl logic is actually needed.',
  },
  {
    title: 'AI shell',
    description: 'Gemini, Groq, and Ollama integrations are reserved for future service-layer work.',
  },
];

export function HomePage() {
  const [healthState, setHealthState] = useState<HealthState>('loading');

  useEffect(() => {
    let isMounted = true;

    const checkBackend = async () => {
      try {
        await getBackendHealth();

        if (isMounted) {
          setHealthState('connected');
        }
      } catch {
        if (isMounted) {
          setHealthState('unavailable');
        }
      }
    };

    void checkBackend();

    return () => {
      isMounted = false;
    };
  }, []);

  const statusLabel =
    healthState === 'loading'
      ? 'Checking backend...'
      : healthState === 'connected'
        ? 'Backend Connected'
        : 'Backend Unavailable';

  const statusStyles =
    healthState === 'connected'
      ? 'border-emerald-200 bg-emerald-50 text-emerald-900'
      : healthState === 'unavailable'
        ? 'border-rose-200 bg-rose-50 text-rose-900'
        : 'border-slate-200 bg-slate-50 text-slate-700';

  return (
    <section className="grid w-full gap-8 py-10 lg:grid-cols-[1.3fr_0.7fr] lg:items-start lg:py-16">
      <div className="space-y-8">
        <div className="inline-flex rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-xs font-semibold tracking-[0.24em] text-emerald-900 uppercase">
          SEO and AEO platform foundation
        </div>

        <div className="space-y-5">
          <h1 className="max-w-3xl text-5xl leading-tight font-semibold tracking-tight text-slate-950 sm:text-6xl lg:text-7xl" style={{ fontFamily: 'Georgia, serif' }}>
            RankPilot is being assembled as a clean, modular base for future optimization workflows.
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-600">
            This page is intentionally minimal. It confirms the frontend stack, routing, and layout structure without introducing any product logic yet.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          {['React + TypeScript', 'FastAPI backend', 'PostgreSQL + Redis'].map((item) => (
            <div key={item} className="rounded-2xl border border-white/70 bg-white/85 px-5 py-4 shadow-soft backdrop-blur">
              <div className="text-sm font-medium text-slate-500">Stack</div>
              <div className="mt-1 text-base font-semibold text-slate-900">{item}</div>
            </div>
          ))}
        </div>

        <div className={`inline-flex rounded-full border px-4 py-2 text-sm font-semibold shadow-sm ${statusStyles}`}>
          {statusLabel}
        </div>
      </div>

      <aside className="rounded-[2rem] border border-slate-200 bg-white/90 p-6 shadow-soft backdrop-blur">
        <div className="flex items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Current stage</p>
            <p className="mt-1 text-xl font-semibold text-slate-950">Foundation only</p>
          </div>
          <div className="rounded-2xl bg-amber-50 px-4 py-3 text-right">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-700">Status</p>
            <p className="mt-1 text-sm font-medium text-amber-900">No product features yet</p>
          </div>
        </div>

        <div className="mt-6 space-y-4">
          {foundationItems.map((item) => (
            <article key={item.title} className="rounded-2xl border border-slate-100 bg-slate-50/80 p-4">
              <h2 className="text-base font-semibold text-slate-900">{item.title}</h2>
              <p className="mt-2 text-sm leading-6 text-slate-600">{item.description}</p>
            </article>
          ))}
        </div>
      </aside>
    </section>
  );
}