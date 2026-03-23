"use client";

import { ChangeEvent, FormEvent, useEffect, useState } from "react";
import Panel from "@/components/Panel";
import { apiRequest } from "@/lib/api";

type Score = { id: number; value: number; played_at: string };
type Charity = { id: number; name: string; category: string; country: string; featured: boolean; description: string };
type Draw = { id: number; month_key: string; draw_numbers_csv: string; logic_used: string; simulation: boolean };
type Winning = { id: number; match_count: number; amount: number; proof_status: string; payout_status: string };

export default function DashboardPage() {
  const [token, setToken] = useState("");
  const [status, setStatus] = useState<string>("Not loaded");
  const [scores, setScores] = useState<Score[]>([]);
  const [scoreValue, setScoreValue] = useState<number>(30);
  const [charities, setCharities] = useState<Charity[]>([]);
  const [draws, setDraws] = useState<Draw[]>([]);
  const [winnings, setWinnings] = useState<Winning[]>([]);
  const [donationAmount, setDonationAmount] = useState<number>(10);

  useEffect(() => {
    const savedToken = sessionStorage.getItem("token") || "";
    setToken(savedToken);
  }, []);

  const loadStatus = async () => {
    try {
      const response = await apiRequest<{ status: string } | null>("/subscription/status", {}, token);
      setStatus(response ? response.status : "No subscription");
    } catch (error) {
      const err = error as Error;
      setStatus(err.message);
    }
  };

  const subscribe = async (plan: "monthly" | "yearly") => {
    await apiRequest("/subscription/subscribe", { method: "POST", body: JSON.stringify({ plan }) }, token);
    await loadStatus();
  };

  const addScore = async (event: FormEvent) => {
    event.preventDefault();
    const response = await apiRequest<Score[]>("/scores", { method: "POST", body: JSON.stringify({ value: scoreValue }) }, token);
    setScores(response);
  };

  const loadScores = async () => {
    const response = await apiRequest<Score[]>("/scores", {}, token);
    setScores(response);
  };

  const loadCharities = async () => {
    const response = await apiRequest<Charity[]>("/charity");
    setCharities(response);
  };

  const selectCharity = async (charityId: number) => {
    await apiRequest(`/charity/select/${charityId}?charity_percent=10`, { method: "POST" }, token);
  };

  const loadDrawResults = async () => {
    const response = await apiRequest<Draw[]>("/draw/results", {}, token);
    setDraws(response);
  };

  const loadWinnings = async () => {
    const response = await apiRequest<Winning[]>("/draw/my-winnings", {}, token);
    setWinnings(response);
  };

  const donate = async (charityId: number) => {
    await apiRequest(
      "/charity/donate",
      { method: "POST", body: JSON.stringify({ charity_id: charityId, amount: donationAmount }) },
      token
    );
  };

  return (
    <main className="mx-auto max-w-6xl space-y-5 p-6">
      <h1 className="text-3xl font-bold">User Dashboard</h1>
      <Panel title="Subscription Status">
        <p className="mb-3 text-sm text-slate-700">Current status: {status}</p>
        <div className="flex gap-2">
          <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={loadStatus}>Refresh</button>
          <button className="rounded bg-emerald-600 px-3 py-2 text-white" onClick={() => subscribe("monthly")}>Subscribe Monthly</button>
          <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={() => subscribe("yearly")}>Subscribe Yearly</button>
        </div>
      </Panel>

      <Panel title="Stableford Score Entry (Last 5 only)">
        <form className="flex items-center gap-2" onSubmit={addScore}>
          <input type="number" min={1} max={45} value={scoreValue} onChange={(e: ChangeEvent<HTMLInputElement>) => setScoreValue(Number(e.target.value))} className="w-24 rounded border p-2" />
          <button className="rounded bg-slate-900 px-3 py-2 text-white" type="submit">Submit Score</button>
          <button className="rounded bg-slate-200 px-3 py-2" type="button" onClick={loadScores}>Load Scores</button>
        </form>
        <ul className="mt-3 space-y-2 text-sm">
          {scores.map((score) => (
            <li key={score.id} className="rounded border p-2">{score.value} • {new Date(score.played_at).toLocaleString()}</li>
          ))}
        </ul>
      </Panel>

      <Panel title="Charity Selection">
        <div className="mb-3 flex gap-2">
          <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={loadCharities}>Load Charities</button>
        </div>
        <ul className="space-y-2 text-sm">
          {charities.map((charity) => (
            <li key={charity.id} className="rounded border p-3">
              <p className="font-semibold">{charity.name} {charity.featured ? "(Featured)" : ""}</p>
              <p>{charity.category} • {charity.country}</p>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <button className="rounded bg-emerald-600 px-3 py-1 text-white" onClick={() => selectCharity(charity.id)}>Select (10%)</button>
                <input className="w-20 rounded border p-1" type="number" min={1} value={donationAmount} onChange={(e: ChangeEvent<HTMLInputElement>) => setDonationAmount(Number(e.target.value))} />
                <button className="rounded bg-indigo-600 px-3 py-1 text-white" onClick={() => donate(charity.id)}>Donate</button>
              </div>
            </li>
          ))}
        </ul>
      </Panel>

      <Panel title="Draw Participation">
        <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={loadDrawResults}>Load Monthly Results</button>
        <ul className="mt-3 space-y-2 text-sm">
          {draws.map((draw) => (
            <li key={draw.id} className="rounded border p-2">
              {draw.month_key} • {draw.draw_numbers_csv} • {draw.logic_used}
            </li>
          ))}
        </ul>
      </Panel>

      <Panel title="Winnings Overview">
        <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={loadWinnings}>Load Winnings</button>
        <ul className="mt-3 space-y-2 text-sm">
          {winnings.map((winning) => (
            <li key={winning.id} className="rounded border p-2">
              Match {winning.match_count} • ${winning.amount.toFixed(2)} • Proof {winning.proof_status} • Payout {winning.payout_status}
            </li>
          ))}
        </ul>
      </Panel>
    </main>
  );
}
