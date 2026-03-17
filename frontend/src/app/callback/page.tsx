"use client";

import { useEffect, useState } from "react";
import { AuthService } from "@/services/auth-service";

export default function Callback() {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");

    if (!code) {
      setError("No authorization code received");
      return;
    }

    const redirectUri = `${window.location.origin}/callback`;

    AuthService.googleAuth(code, redirectUri)
      .then((token) => {
        localStorage.setItem("token", token);
        window.location.href = "/";
      })
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4">
        <p className="text-red-400">Error: {error}</p>
        <a href="/" className="text-blue-500 hover:underline">
          Back to login
        </a>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <p className="text-neutral-400">Authenticating...</p>
    </div>
  );
}
