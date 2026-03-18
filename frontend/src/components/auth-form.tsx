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
      <div className="relative flex flex-col items-center overflow-hidden px-6 pb-24" style={{ background: 'linear-gradient(3.59deg, #F4F3F3 11.21%, #E2C2A3 36.56%, #CEA68A 69.71%, #BB835C 100.11%)' }}>
        {/* Logo */}
        <img
          src="/logo.png"
          alt="Youth logo"
          className="z-20"
          style={{ width: '189px', height: '31.28px', marginTop: '24px' }}
        />

        {/* Keywords background + profile */}
        <div className="relative" style={{ width: '100%', maxWidth: '500px', height: '280px', marginTop: '8px' }}>
          {/* Keywords SVG background */}
          <img
            src="/keywords-bg.svg"
            alt="Health keywords"
            className="absolute inset-0 h-full w-full object-contain"
          />

          {/* Blurred phone frame */}
          <div
            className="absolute"
            style={{
              width: '177px',
              height: '293px',
              left: 'calc(50% - 177px/2)',
              top: '20px',
              background: 'linear-gradient(180deg, rgba(255, 255, 255, 0.24) 0%, rgba(255, 255, 255, 0) 39%)',
              borderRadius: '20.8667px',
              border: '1.5px solid rgba(255, 255, 255, 0.3)',
              backdropFilter: 'blur(10px)',
              WebkitBackdropFilter: 'blur(10px)',
              zIndex: 5,
            }}
          />

          {/* Avatar */}
          <div
            className="absolute overflow-hidden"
            style={{
              width: '177px',
              height: '293px',
              left: 'calc(50% - 177px/2)',
              top: '20px',
              borderRadius: '20.8667px',
              zIndex: 10,
            }}
          >
            <img
              src="/profile.png"
              alt="Profile"
              className="h-full w-full object-cover"
            />
          </div>
        </div>

        {/* Fade to white */}
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white to-transparent" />
      </div>

      {/* Form section */}
      <div className="flex flex-1 flex-col items-center px-6 pb-8">
        <h2 className="mb-8 text-2xl font-medium leading-[30px] tracking-[-0.4px] text-[#1B1B1B]">
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
                  className="w-full rounded-[10px] border border-[#DEDEDE] bg-white px-3 py-[15px] text-sm text-black placeholder-gray-400 outline-none focus:border-gray-500"
                />
                <button
                  type="submit"
                  className="w-full cursor-pointer rounded-xl border border-[#1B1B1B] bg-[#1B1B1B] px-6 py-[18px] font-mono text-sm font-medium uppercase tracking-widest text-white transition-colors hover:bg-gray-800"
                >
                  Continue with Email
                </button>
              </form>

              {/* Divider */}
              <div className="my-5 flex items-center" style={{ gap: '14px', height: '21px', padding: '0px' }}>
                <span className="h-px flex-1 bg-gray-200" />
                <span className="text-xs uppercase tracking-wider text-gray-400">or</span>
                <span className="h-px flex-1 bg-gray-200" />
              </div>

              {/* Google button */}
              <a
                href={AuthService.getGoogleAuthUrl()}
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-[#1B1B1B] bg-white px-6 py-[18px] font-mono text-sm font-medium uppercase tracking-widest text-black no-underline transition-colors hover:bg-gray-50"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1Z" fill="#1B1B1B"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23Z" fill="#1B1B1B"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A10.96 10.96 0 0 0 1 12c0 1.77.42 3.45 1.18 4.93l3.66-2.84Z" fill="#1B1B1B"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53Z" fill="#1B1B1B"/>
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
                  className="w-full rounded-[10px] border border-[#DEDEDE] bg-white px-3 py-[15px] text-sm text-black placeholder-gray-400 outline-none focus:border-gray-500"
                />

                {error && (
                  <p className="m-0 text-center text-sm text-red-500">{error}</p>
                )}

                <button
                  type="submit"
                  className="w-full cursor-pointer rounded-xl border border-[#1B1B1B] bg-[#1B1B1B] px-6 py-[18px] font-mono text-sm font-medium uppercase tracking-widest text-white transition-colors hover:bg-gray-800"
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
        <p className="mt-auto pt-8 text-center text-xs leading-4 text-[#8F8F8F]">
          Any issues or questions? Contact{" "}
          <a href="mailto:support@youth-prevention.com" className="text-[#1B1B1B] underline">
            support@youth-prevention.com
          </a>
        </p>
      </div>
    </div>
  );
}
