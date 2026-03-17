"use client";

import { useAuth } from "@/hooks/use-auth";
import { AuthForm } from "@/components/auth-form";
import { UserCard } from "@/components/user-card";

export default function Home() {
  const { user, loading, error, handleLogin, handleRegister, signOut, clearError } =
    useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-white">
        <p className="text-gray-400">Loading...</p>
      </div>
    );
  }

  if (user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-white">
        <UserCard user={user} onSignOut={signOut} />
      </div>
    );
  }

  return <AuthForm error={error} onLogin={handleLogin} onRegister={handleRegister} onClearError={clearError} />;
}
