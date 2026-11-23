"use client";

import { useSession } from "@/lib/session";

export function SessionBadge() {
  const { user, project, isStub } = useSession();

  return (
    <div className="flex items-center gap-3 text-sm">
      <span>
        <span className="text-muted">Project:</span>{" "}
        <span className="font-medium">{project.name}</span>
      </span>
      <span className="text-muted" aria-hidden="true">
        ·
      </span>
      <span>{user.name}</span>
      {isStub && (
        <span
          className="border-border text-muted rounded-full border px-2 py-0.5 text-xs"
          title="No login yet. Everyone uses the same local session."
        >
          Dev session
        </span>
      )}
    </div>
  );
}
