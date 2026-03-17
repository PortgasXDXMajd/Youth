"use client";

import { useEffect, useState } from "react";
import { AuthService } from "@/services/auth-service";
import { UserService } from "@/services/user-service";
import { User } from "@/types";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }

    UserService.me()
      .then(setUser)
      .catch(() => localStorage.removeItem("token"))
      .finally(() => setLoading(false));
  }, []);

  const handleLogin = async (email: string, password: string) => {
    setError("");
    try {
      const token = await AuthService.login(email, password);
      localStorage.setItem("token", token);
      const userData = await UserService.me();
      setUser(userData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    }
  };

  const handleRegister = async (email: string, password: string) => {
    setError("");
    try {
      await AuthService.register(email, password);
      const token = await AuthService.login(email, password);
      localStorage.setItem("token", token);
      const userData = await UserService.me();
      setUser(userData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    }
  };

  const signOut = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  const clearError = () => setError("");

  return { user, loading, error, handleLogin, handleRegister, signOut, clearError };
}
