type PanelProps = {
  title: string;
  children: React.ReactNode;
};

export default function Panel({ title, children }: PanelProps) {
  return (
    <section className="rounded-xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h2 className="mb-4 text-lg font-semibold">{title}</h2>
      {children}
    </section>
  );
}
