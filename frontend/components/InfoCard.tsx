type InfoCardProps = {
  title: string;
  description: string;
};

export default function InfoCard({ title, description }: InfoCardProps) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4">
      <h3 className="text-base font-semibold text-slate-900">{title}</h3>
      <p className="mt-2 text-sm text-slate-600">{description}</p>
    </article>
  );
}
