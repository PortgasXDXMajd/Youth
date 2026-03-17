"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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

    fetch(`${API_URL}/api/v1/auth/google`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, redirect_uri: redirectUri }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Authentication failed");
        return res.json();
      })
      .then((body) => {
        localStorage.setItem("token", body.data.access_token);
        window.location.href = "/";
      })
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div style={styles.container}>
        <p style={{ color: "#f44" }}>Error: {error}</p>
        <a href="/" style={{ color: "#4285f4" }}>
          Back to login
        </a>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <p style={{ color: "#888" }}>Authenticating...</p>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#000",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: 16,
  },
};
