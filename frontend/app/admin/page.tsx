"use client";

import { ChangeEvent, FormEvent, useState } from "react";
import Panel from "@/components/Panel";
import { apiRequest } from "@/lib/api";

type Draw = {
  id: number;
  month_key: string;
  draw_numbers_csv: string;
  logic_used: string;
  simulation: boolean;
};

type User = { id: number; email: string; full_name: string; role: string; charity_percent: number };
type Charity = { id: number; name: string; category: string; country: string; description: string; featured: boolean };

export default function AdminPage() {
  const [token, setToken] = useState("");
  const [logicType, setLogicType] = useState("random");
  const [simulation, setSimulation] = useState(true);
  const [result, setResult] = useState<Draw | null>(null);
  const [analytics, setAnalytics] = useState<Record<string, number> | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [charities, setCharities] = useState<Charity[]>([]);
  const [charityName, setCharityName] = useState("");
  const [winningId, setWinningId] = useState<number>(0);

  const loadToken = () => {
    const saved = sessionStorage.getItem("token") || "";
    setToken(saved);
  };

  const runDraw = async (event: FormEvent) => {
    event.preventDefault();
    const response = await apiRequest<Draw>(
      "/admin/run-draw",
      { method: "POST", body: JSON.stringify({ logic_type: logicType, simulation }) },
      token
    );
    setResult(response);
  };

  const loadAnalytics = async () => {
    const response = await apiRequest<Record<string, number>>("/admin/analytics", {}, token);
    setAnalytics(response);
  };

  const loadUsers = async () => {
    const response = await apiRequest<User[]>("/admin/users", {}, token);
    setUsers(response);
  };

  const loadCharities = async () => {
    const response = await apiRequest<Charity[]>("/charity", {}, token);
    setCharities(response);
  };

  const createCharity = async (event: FormEvent) => {
    event.preventDefault();
    if (!charityName.trim()) {
      return;
    }
    await apiRequest(
      "/admin/charity",
      {
        method: "POST",
        body: JSON.stringify({
          name: charityName,
          category: "Community",
          country: "Global",
          description: "Admin created charity",
          featured: false,
        }),
      },
      token
    );
    setCharityName("");
    await loadCharities();
  };

  const verifyWinning = async (proofStatus: "approved" | "rejected") => {
    await apiRequest(
      "/admin/winning/verify",
      { method: "POST", body: JSON.stringify({ winning_id: winningId, proof_status: proofStatus }) },
      token
    );
  };

  const markPaid = async () => {
    await apiRequest(
      "/admin/winning/payout",
      { method: "POST", body: JSON.stringify({ winning_id: winningId, payout_status: "paid" }) },
      token
    );
  };

  return (
    <main className="mx-auto max-w-5xl space-y-5 p-6">
      <h1 className="text-3xl font-bold">Admin Panel</h1>
      <Panel title="Admin Session">
        <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={loadToken}>Load Token from browser</button>
      </Panel>

      <Panel title="Draw Management">
        <form className="space-y-3" onSubmit={runDraw}>
          <select className="w-full rounded border p-2" value={logicType} onChange={(e: ChangeEvent<HTMLSelectElement>) => setLogicType(e.target.value)}>
            <option value="random">Random</option>
            <option value="frequency-based">Frequency-based</option>
          </select>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={simulation} onChange={(e: ChangeEvent<HTMLInputElement>) => setSimulation(e.target.checked)} />
            Simulation mode
          </label>
          <button className="rounded bg-indigo-600 px-3 py-2 text-white" type="submit">Run Draw</button>
        </form>
        {result && (
          <div className="mt-3 rounded border p-3 text-sm">
            <p>Month: {result.month_key}</p>
            <p>Numbers: {result.draw_numbers_csv}</p>
            <p>Logic: {result.logic_used}</p>
            <p>Simulation: {String(result.simulation)}</p>
          </div>
        )}
      </Panel>

      <Panel title="Analytics">
        <button className="rounded bg-emerald-600 px-3 py-2 text-white" onClick={loadAnalytics}>Load Analytics</button>
        {analytics && <pre className="mt-3 rounded bg-slate-900 p-3 text-xs text-white">{JSON.stringify(analytics, null, 2)}</pre>}
      </Panel>

      <Panel title="User Management">
        <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={loadUsers}>Load Users</button>
        <ul className="mt-3 space-y-2 text-sm">
          {users.map((user) => (
            <li key={user.id} className="rounded border p-2">
              {user.full_name} • {user.email} • {user.role}
            </li>
          ))}
        </ul>
      </Panel>

      <Panel title="Charity Management">
        <form className="flex gap-2" onSubmit={createCharity}>
          <input className="flex-1 rounded border p-2" placeholder="New charity name" value={charityName} onChange={(e: ChangeEvent<HTMLInputElement>) => setCharityName(e.target.value)} />
          <button className="rounded bg-indigo-600 px-3 py-2 text-white" type="submit">Add</button>
          <button className="rounded bg-slate-200 px-3 py-2" type="button" onClick={loadCharities}>Refresh</button>
        </form>
        <ul className="mt-3 space-y-2 text-sm">
          {charities.map((charity) => (
            <li key={charity.id} className="rounded border p-2">{charity.name} • {charity.category} • {charity.country}</li>
          ))}
        </ul>
      </Panel>

      <Panel title="Winner Verification">
        <div className="flex flex-wrap gap-2">
          <input className="w-28 rounded border p-2" type="number" placeholder="Winning ID" value={winningId} onChange={(e: ChangeEvent<HTMLInputElement>) => setWinningId(Number(e.target.value))} />
          <button className="rounded bg-emerald-600 px-3 py-2 text-white" onClick={() => verifyWinning("approved")}>Approve Proof</button>
          <button className="rounded bg-amber-600 px-3 py-2 text-white" onClick={() => verifyWinning("rejected")}>Reject Proof</button>
          <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={markPaid}>Mark Paid</button>
        </div>
      </Panel>
    </main>
  );
}
