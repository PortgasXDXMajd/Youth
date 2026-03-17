"use client";

import { useState } from "react";
import { AuthService } from "@/services/auth-service";

interface AuthFormProps {
  error: string;
  onLogin: (email: string, password: string) => void;
  onRegister: (email: string, password: string) => void;
  onClearError: () => void;
}

export function AuthForm({ error, onLogin, onRegister, onClearError }: AuthFormProps) {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isRegister) {
      onRegister(email, password);
    } else {
      onLogin(email, password);
    }
  };

  const toggleMode = () => {
    setIsRegister(!isRegister);
    onClearError();
  };

  return (
    <div className="w-[380px] rounded-2xl border border-neutral-800 bg-neutral-900 p-10 text-center">
      <h1 className="mb-6 text-2xl font-semibold text-white">
        {isRegister ? "Create Account" : "Sign In"}
      </h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="rounded-lg border border-neutral-700 bg-neutral-800 px-4 py-3 text-sm text-white placeholder-neutral-500 outline-none focus:border-neutral-500"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
          className="rounded-lg border border-neutral-700 bg-neutral-800 px-4 py-3 text-sm text-white placeholder-neutral-500 outline-none focus:border-neutral-500"
        />

        {error && (
          <p className="m-0 text-sm text-red-400">{error}</p>
        )}

        <button
          type="submit"
          className="cursor-pointer rounded-lg bg-white py-3 text-[15px] font-semibold text-black transition-colors hover:bg-neutral-200"
        >
          {isRegister ? "Register" : "Sign In"}
        </button>
      </form>

      <div className="my-5 flex items-center gap-3">
        <span className="h-px flex-1 bg-neutral-700" />
        <span className="text-[13px] text-neutral-500">or</span>
        <span className="h-px flex-1 bg-neutral-700" />
      </div>

      <a
        href={AuthService.getGoogleAuthUrl()}
        className="block rounded-lg bg-blue-600 py-3 text-[15px] font-medium text-white no-underline transition-colors hover:bg-blue-700"
      >
        Sign in with Google
      </a>

      <p className="mt-5 text-sm text-neutral-400">
        {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
        <button
          onClick={toggleMode}
          className="cursor-pointer border-none bg-transparent p-0 text-sm text-blue-500 hover:underline"
        >
          {isRegister ? "Sign in" : "Register"}
        </button>
      </p>
    </div>
  );
}
