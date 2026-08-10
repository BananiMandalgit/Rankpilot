import { Link } from 'react-router-dom';

export function NotFoundPage() {
  return (
    <div className="flex w-full flex-col items-start justify-center gap-4 py-16">
      <h1 className="text-3xl font-semibold text-slate-950">Page not found</h1>
      <p className="max-w-xl text-slate-600">This route does not exist yet. The application shell only includes the foundation landing page for now.</p>
      <Link to="/" className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">
        Return home
      </Link>
    </div>
  );
}