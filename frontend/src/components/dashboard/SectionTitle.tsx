type SectionTitleProps = {
  title: string;
  description?: string;
};

export function SectionTitle({ title, description }: SectionTitleProps) {
  return (
    <header className="space-y-1">
      <h2 className="text-xl font-semibold tracking-tight text-slate-950 sm:text-2xl">{title}</h2>
      {description ? <p className="text-sm leading-6 text-slate-600">{description}</p> : null}
    </header>
  );
}
