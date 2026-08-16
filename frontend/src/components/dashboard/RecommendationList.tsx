type RecommendationListProps = {
  items: string[];
};

export function RecommendationList({ items }: RecommendationListProps) {
  return (
    <ul className="space-y-3">
      {items.map((item) => (
        <li key={item} className="rounded-xl border border-slate-200 bg-white/80 px-4 py-3 text-sm leading-6 text-slate-700">
          {item}
        </li>
      ))}
    </ul>
  );
}
