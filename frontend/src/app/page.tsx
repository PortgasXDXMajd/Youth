"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "";

interface User {
  email: string;
  created_at: string;
  provider: string;
}

function getGoogleAuthUrl() {
  const redirectUri = `${window.location.origin}/callback`;
  const params = new URLSearchParams({
    client_id: GOOGLE_CLIENT_ID,
    redirect_uri: redirectUri,
    response_type: "code",
    scope: "openid email profile",
    access_type: "offline",
    prompt: "consent",
  });
  return `https://accounts.google.com/o/oauth2/v2/auth?${params}`;
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }

    fetch(`${API_URL}/users/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Unauthorized");
        return res.json();
      })
      .then(setUser)
      .catch(() => localStorage.removeItem("token"))
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const endpoint = isRegister ? "/users" : "/auth/login";

    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Request failed");
      }

      const data = await res.json();
      localStorage.setItem("token", data.token);
      setUser(data.user);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <p style={{ color: "#888" }}>Loading...</p>
      </div>
    );
  }

  // ── Logged in: show user info ──────────────────────────────────
  if (user) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h2 style={{ color: "#fff", margin: "0 0 24px" }}>User Information</h2>

          <div style={styles.row}>
            <span style={styles.label}>Email</span>
            <span style={styles.value}>{user.email}</span>
          </div>

          <div style={styles.row}>
            <span style={styles.label}>Date of Registration</span>
            <span style={styles.value}>
              {new Date(user.created_at).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </span>
          </div>

          <div style={styles.row}>
            <span style={styles.label}>Auth Provider</span>
            <span style={styles.value}>
              {user.provider === "google" ? "Google" : "Password"}
            </span>
          </div>

          <button
            onClick={() => {
              localStorage.removeItem("token");
              setUser(null);
            }}
            style={styles.logout}
          >
            Sign out
          </button>
        </div>
      </div>
    );
  }

  // ── Not logged in: login / register form ───────────────────────
  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={{ color: "#fff", margin: "0 0 24px" }}>
          {isRegister ? "Create Account" : "Sign In"}
        </h1>

        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={styles.input}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
            style={styles.input}
          />

          {error && <p style={{ color: "#f44", margin: 0, fontSize: 14 }}>{error}</p>}

          <button type="submit" style={styles.submitBtn}>
            {isRegister ? "Register" : "Sign In"}
          </button>
        </form>

        <div style={styles.divider}>
          <span style={styles.dividerLine} />
          <span style={{ color: "#666", fontSize: 13 }}>or</span>
          <span style={styles.dividerLine} />
        </div>

        <a href={getGoogleAuthUrl()} style={styles.googleBtn}>
          Sign in with Google
        </a>

        <p style={{ color: "#888", marginTop: 20, fontSize: 14 }}>
          {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
          <button
            onClick={() => {
              setIsRegister(!isRegister);
              setError("");
            }}
            style={styles.toggleLink}
          >
            {isRegister ? "Sign in" : "Register"}
          </button>
        </p>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#000",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  card: {
    textAlign: "center",
    padding: 40,
    borderRadius: 16,
    backgroundColor: "#111",
    border: "1px solid #222",
    width: 380,
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },
  input: {
    padding: "12px 16px",
    borderRadius: 8,
    border: "1px solid #333",
    backgroundColor: "#1a1a1a",
    color: "#fff",
    fontSize: 14,
    outline: "none",
  },
  submitBtn: {
    padding: "12px 0",
    backgroundColor: "#fff",
    color: "#000",
    border: "none",
    borderRadius: 8,
    fontSize: 15,
    fontWeight: 600,
    cursor: "pointer",
  },
  divider: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    margin: "20px 0",
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: "#333",
  },
  googleBtn: {
    display: "block",
    padding: "12px 0",
    backgroundColor: "#4285f4",
    color: "#fff",
    borderRadius: 8,
    textDecoration: "none",
    fontSize: 15,
    fontWeight: 500,
  },
  toggleLink: {
    background: "none",
    border: "none",
    color: "#4285f4",
    cursor: "pointer",
    fontSize: 14,
    padding: 0,
  },
  row: {
    display: "flex",
    justifyContent: "space-between",
    padding: "12px 0",
    borderBottom: "1px solid #222",
  },
  label: {
    color: "#888",
    fontSize: 14,
  },
  value: {
    color: "#fff",
    fontSize: 14,
  },
  logout: {
    marginTop: 24,
    padding: "10px 32px",
    backgroundColor: "transparent",
    color: "#f44",
    border: "1px solid #f44",
    borderRadius: 8,
    cursor: "pointer",
    fontSize: 14,
  },
};
