import { Link, Outlet } from 'react-router-dom';

export function RootLayout() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(15,118,110,0.14),_transparent_32%),radial-gradient(circle_at_bottom_right,_rgba(217,119,6,0.12),_transparent_28%),linear-gradient(180deg,_#f8fafc_0%,_#eef2ff_100%)] text-slate-900">
      <header className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-6 lg:px-8">
        <Link to="/" className="text-lg font-semibold tracking-[0.24em] text-slate-900 uppercase">
          RankPilot
        </Link>
        <span className="rounded-full border border-slate-200 bg-white/80 px-4 py-2 text-xs font-medium tracking-[0.2em] text-slate-600 uppercase shadow-sm">
          Foundation build
        </span>
      </header>
      <main className="mx-auto flex w-full max-w-6xl flex-1 px-6 pb-16 lg:px-8">
        <Outlet />
      </main>
      <footer className="mx-auto w-full max-w-6xl px-6 pb-8 text-sm text-slate-500 lg:px-8">
        Initial skeleton only. Product features will be added incrementally.
      </footer>
    </div>
  );
}