type MetricTone = 'emerald' | 'teal' | 'amber';

type MetricCardProps = {
  label: string;
  value: string;
  helperText: string;
  tone: MetricTone;
};

const toneClasses: Record<MetricTone, string> = {
  emerald: 'border-emerald-200 bg-emerald-50/80 text-emerald-900',
  teal: 'border-teal-200 bg-teal-50/80 text-teal-900',
  amber: 'border-amber-200 bg-amber-50/80 text-amber-900',
};

export function MetricCard({ label, value, helperText, tone }: MetricCardProps) {
  return (
    <article className={`rounded-2xl border p-4 shadow-soft ${toneClasses[tone]}`}>
      <p className="text-xs font-semibold tracking-[0.2em] uppercase">{label}</p>
      <p className="mt-2 text-3xl font-semibold tracking-tight">{value}</p>
      <p className="mt-2 text-sm text-slate-700">{helperText}</p>
    </article>
  );
}
