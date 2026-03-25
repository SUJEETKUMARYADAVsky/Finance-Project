import Link from "next/link";
import InfoCard from "@/components/InfoCard";

export default function AboutPage() {
  return (
    <main className="mx-auto min-h-screen max-w-5xl p-6">
      <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-100">
        <p className="text-sm font-semibold text-emerald-700">About This Platform</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">How Golf, Giving, and Rewards Come Together</h1>
        <p className="mt-3 text-slate-600">
          This platform combines monthly golf draws with charitable contributions. Members can subscribe, submit scores,
          support charities, and track outcomes from one place.
        </p>

        <div className="mt-6 grid gap-3 md:grid-cols-3">
          <InfoCard
            title="Play"
            description="Submit Stableford scores and stay eligible for monthly participation."
          />
          <InfoCard
            title="Contribute"
            description="Select charities and direct part of your participation toward social impact."
          />
          <InfoCard
            title="Track"
            description="View draw outcomes and winnings with transparent status updates."
          />
        </div>

        <div className="mt-6">
          <Link className="rounded-lg bg-slate-900 px-4 py-2 text-white" href="/">
            Back to Home
          </Link>
        </div>
      </div>
    </main>
  );
}
