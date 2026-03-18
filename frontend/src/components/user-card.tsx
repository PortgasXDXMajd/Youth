import { User } from "@/types";

interface UserCardProps {
  user: User;
  onSignOut: () => void;
}

export function UserCard({ user, onSignOut }: UserCardProps) {
  return (
    <div className="w-[400px] rounded-3xl border border-gray-200 bg-white p-10 text-center shadow-sm">
      <h2 className="mb-6 text-xl font-medium text-black">
        User Information
      </h2>

      <div className="flex items-center justify-between border-b border-gray-100 py-3">
        <span className="text-sm text-gray-400">Email</span>
        <span className="text-sm text-black">{user.email}</span>
      </div>

      <div className="flex items-center justify-between border-b border-gray-100 py-3">
        <span className="text-sm text-gray-400">Date of Registration</span>
        <span className="text-sm text-black">
          {new Date(user.created_at).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </span>
      </div>

      <div className="flex items-center justify-between border-b border-gray-100 py-3">
        <span className="text-sm text-gray-400">Auth Provider</span>
        <span className="text-sm text-black">
          {user.provider === "google" ? "Google" : "Password"}
        </span>
      </div>

      <button
        onClick={onSignOut}
        className="mt-6 cursor-pointer rounded-full border border-gray-300 bg-white px-8 py-2.5 text-sm font-medium text-black transition-colors hover:bg-gray-50"
      >
        Sign out
      </button>
    </div>
  );
}
