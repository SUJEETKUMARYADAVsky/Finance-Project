"use client";

import { ChangeEvent, FormEvent, useState } from "react";
import { apiRequest } from "@/lib/api";

type AuthMode = "signup" | "login";

type TokenResponse = {
  access_token: string;
};

export default function AuthPage() {
  const [mode, setMode] = useState<AuthMode>("signup");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string>("");

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage("");

    try {
      const path = mode === "signup" ? "/auth/signup" : "/auth/login";
      const body =
        mode === "signup"
          ? { email, password, full_name: fullName, charity_percent: 10 }
          : { email, password };

      const result = await apiRequest<TokenResponse>(path, {
        method: "POST",
        body: JSON.stringify(body),
      });

      sessionStorage.setItem("token", result.access_token);
      setMessage("Authentication successful. Token saved in browser.");
    } catch (error) {
      const err = error as Error;
      setMessage(err.message);
    }
  };

  return (
    <main className="mx-auto min-h-screen max-w-md p-6">
      <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-100">
        <h1 className="text-2xl font-bold">{mode === "signup" ? "Create account" : "Login"}</h1>
        <form onSubmit={onSubmit} className="mt-4 space-y-3">
          <input className="w-full rounded-lg border p-2" placeholder="Email" type="email" value={email} onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)} required />
          {mode === "signup" && (
            <input className="w-full rounded-lg border p-2" placeholder="Full name" value={fullName} onChange={(e: ChangeEvent<HTMLInputElement>) => setFullName(e.target.value)} required />
          )}
          <input className="w-full rounded-lg border p-2" placeholder="Password" type="password" value={password} onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)} required />
          <button className="w-full rounded-lg bg-slate-900 p-2 text-white" type="submit">
            {mode === "signup" ? "Sign up" : "Login"}
          </button>
        </form>
        <button className="mt-3 text-sm text-indigo-700" onClick={() => setMode(mode === "signup" ? "login" : "signup")}> 
          Switch to {mode === "signup" ? "Login" : "Signup"}
        </button>
        {message && <p className="mt-4 text-sm text-slate-700">{message}</p>}
      </div>
    </main>
  );
}
