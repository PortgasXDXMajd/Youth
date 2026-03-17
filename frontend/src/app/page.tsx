"use client";

import { useAuth } from "@/hooks/use-auth";
import { AuthForm } from "@/components/auth-form";
import { UserCard } from "@/components/user-card";

export default function Home() {
  const { user, loading, error, handleLogin, handleRegister, signOut, clearError } =
    useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-neutral-400">Loading...</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      {user ? (
        <UserCard user={user} onSignOut={signOut} />
      ) : (
        <AuthForm
          error={error}
          onLogin={handleLogin}
          onRegister={handleRegister}
          onClearError={clearError}
        />
      )}
    </div>
  );
}
