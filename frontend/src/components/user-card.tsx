import { User } from "@/types";

interface UserCardProps {
  user: User;
  onSignOut: () => void;
}

export function UserCard({ user, onSignOut }: UserCardProps) {
  return (
    <div className="w-[380px] rounded-2xl border border-neutral-800 bg-neutral-900 p-10 text-center">
      <h2 className="mb-6 text-xl font-semibold text-white">
        User Information
      </h2>

      <div className="flex items-center justify-between border-b border-neutral-800 py-3">
        <span className="text-sm text-neutral-400">Email</span>
        <span className="text-sm text-white">{user.email}</span>
      </div>

      <div className="flex items-center justify-between border-b border-neutral-800 py-3">
        <span className="text-sm text-neutral-400">Date of Registration</span>
        <span className="text-sm text-white">
          {new Date(user.created_at).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </span>
      </div>

      <div className="flex items-center justify-between border-b border-neutral-800 py-3">
        <span className="text-sm text-neutral-400">Auth Provider</span>
        <span className="text-sm text-white">
          {user.provider === "google" ? "Google" : "Password"}
        </span>
      </div>

      <button
        onClick={onSignOut}
        className="mt-6 cursor-pointer rounded-lg border border-red-500 bg-transparent px-8 py-2.5 text-sm text-red-500 transition-colors hover:bg-red-500/10"
      >
        Sign out
      </button>
    </div>
  );
}
