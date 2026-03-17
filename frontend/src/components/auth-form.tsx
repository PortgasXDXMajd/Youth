"use client";

import { useState } from "react";
import { AuthService } from "@/services/auth-service";

interface AuthFormProps {
  error: string;
  onLogin: (email: string, password: string) => void;
  onRegister: (email: string, password: string) => void;
  onClearError: () => void;
}

const HEALTH_TAGS = [
  "METABOLIC",
  "GENOMIC",
  "LUNGS",
  "CARDIOVASCULAR",
  "MENTAL",
  "LIVER",
  "BRAIN",
  "PREVENTION",
  "GENETIC",
  "AGING",
];

export function AuthForm({ error, onLogin, onRegister, onClearError }: AuthFormProps) {
  const [step, setStep] = useState<"email" | "password">("email");
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleEmailContinue = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setStep("password");
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isRegister) {
      onRegister(email, password);
    } else {
      onLogin(email, password);
    }
  };

  const handleBack = () => {
    setStep("email");
    setPassword("");
    onClearError();
  };

  const toggleMode = () => {
    setIsRegister(!isRegister);
    onClearError();
  };

  return (
    <div className="flex min-h-screen w-full flex-col">
      {/* Hero section with gradient */}
      <div className="relative flex flex-col items-center overflow-hidden bg-gradient-to-b from-[#D4634B] via-[#D48A6B] to-[#E8C4A8] px-6 pb-24 pt-12">
        {/* Logo */}
        <h1 className="z-10 font-serif text-4xl font-bold tracking-wide text-white">
          YOU(th)
        </h1>

        {/* Floating health tags */}
        <div className="relative mt-8 flex h-48 w-full max-w-md items-center justify-center">
          {/* Avatar placeholder frame */}
          <div className="absolute z-10 h-56 w-44 rounded-3xl border-2 border-white/30 bg-white/10 backdrop-blur-sm" />

          {/* Tags row 1 */}
          <div className="absolute top-4 flex w-full justify-between px-2">
            <span className="text-xs font-semibold tracking-widest text-white/70">METABOLIC</span>
            <span className="text-xs font-semibold tracking-widest text-white/70">GENOMIC</span>
            <span className="text-xs font-semibold tracking-widest text-white/70">LUNGS</span>
          </div>
          {/* Tags row 2 */}
          <div className="absolute top-16 flex w-full justify-between px-2">
            <span className="text-xs font-semibold tracking-widest text-white/70">CARDIOVASCULAR</span>
            <span className="text-xs font-semibold tracking-widest text-white/70">MENTAL</span>
            <span className="text-xs font-semibold tracking-widest text-white/70">LIVER</span>
          </div>
          {/* Tags row 3 */}
          <div className="absolute top-28 flex w-full justify-between px-2">
            <span className="text-xs font-semibold tracking-widest text-white/70">BRAIN</span>
            <span className="text-xs font-semibold tracking-widest text-white/70">PREVENTION</span>
            <span className="text-xs font-semibold tracking-widest text-white/70">GENETIC</span>
            <span className="text-xs font-semibold tracking-widest text-white/70">AGING</span>
          </div>
        </div>

        {/* Fade to white */}
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white to-transparent" />
      </div>

      {/* Form section */}
      <div className="flex flex-1 flex-col items-center px-6 pb-8">
        <h2 className="mb-8 font-serif text-2xl font-medium text-black">
          Login or register
        </h2>

        <div className="w-full max-w-sm">
          {step === "email" ? (
            <>
              <form onSubmit={handleEmailContinue} className="flex flex-col gap-4">
                <input
                  type="email"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full rounded-full border border-gray-300 bg-white px-5 py-3.5 text-sm text-black placeholder-gray-400 outline-none focus:border-gray-500"
                />
                <button
                  type="submit"
                  className="w-full cursor-pointer rounded-full bg-black py-3.5 text-sm font-semibold uppercase tracking-widest text-white transition-colors hover:bg-gray-800"
                >
                  Continue with Email
                </button>
              </form>

              {/* Divider */}
              <div className="my-6 flex items-center gap-3">
                <span className="h-px flex-1 bg-gray-200" />
                <span className="text-xs uppercase tracking-wider text-gray-400">or</span>
                <span className="h-px flex-1 bg-gray-200" />
              </div>

              {/* Google button */}
              <a
                href={AuthService.getGoogleAuthUrl()}
                className="flex w-full items-center justify-center gap-3 rounded-full border border-gray-300 bg-white py-3.5 text-sm font-semibold uppercase tracking-widest text-black no-underline transition-colors hover:bg-gray-50"
              >
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                  <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844a4.14 4.14 0 0 1-1.796 2.716v2.259h2.908c1.702-1.567 2.684-3.875 2.684-6.615Z" fill="#4285F4"/>
                  <path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.26c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18Z" fill="#34A853"/>
                  <path d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.997 8.997 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332Z" fill="#FBBC05"/>
                  <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58Z" fill="#EA4335"/>
                </svg>
                Continue with Google
              </a>
            </>
          ) : (
            <>
              <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <div className="flex items-center gap-2 rounded-full border border-gray-300 bg-gray-50 px-5 py-3.5">
                  <span className="text-sm text-gray-600">{email}</span>
                  <button
                    type="button"
                    onClick={handleBack}
                    className="ml-auto cursor-pointer border-none bg-transparent p-0 text-xs text-gray-400 hover:text-gray-600"
                  >
                    Change
                  </button>
                </div>

                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={6}
                  autoFocus
                  className="w-full rounded-full border border-gray-300 bg-white px-5 py-3.5 text-sm text-black placeholder-gray-400 outline-none focus:border-gray-500"
                />

                {error && (
                  <p className="m-0 text-center text-sm text-red-500">{error}</p>
                )}

                <button
                  type="submit"
                  className="w-full cursor-pointer rounded-full bg-black py-3.5 text-sm font-semibold uppercase tracking-widest text-white transition-colors hover:bg-gray-800"
                >
                  {isRegister ? "Register" : "Sign In"}
                </button>
              </form>

              <p className="mt-4 text-center text-sm text-gray-500">
                {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
                <button
                  onClick={toggleMode}
                  className="cursor-pointer border-none bg-transparent p-0 text-sm font-medium text-black underline"
                >
                  {isRegister ? "Sign in" : "Register"}
                </button>
              </p>
            </>
          )}
        </div>

        {/* Footer */}
        <p className="mt-auto pt-8 text-center text-xs text-gray-400">
          Any issues or questions? Contact{" "}
          <a href="mailto:support@youth-prevention.com" className="text-gray-500 underline">
            support@youth-prevention.com
          </a>
        </p>
      </div>
    </div>
  );
}
