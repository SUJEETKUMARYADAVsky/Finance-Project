import Link from "next/link";

export default function HomePage() {
  return (
    <main className="mx-auto min-h-screen max-w-5xl p-6">
      <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-100">
        <p className="text-sm font-semibold text-emerald-700">Golf Charity Draw Platform</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">Play, Contribute, and Win Monthly Rewards</h1>
        <p className="mt-3 text-slate-600">
          Manage subscriptions, submit Stableford scores, support charities, and participate in monthly draws.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link className="rounded-lg bg-slate-900 px-4 py-2 text-white" href="/auth">
            Sign up / Login
          </Link>
          <Link className="rounded-lg bg-emerald-600 px-4 py-2 text-white" href="/dashboard">
            User Dashboard
          </Link>
          <Link className="rounded-lg bg-indigo-600 px-4 py-2 text-white" href="/admin">
            Admin Panel
          </Link>
        </div>
      </div>
    </main>
  );
}
