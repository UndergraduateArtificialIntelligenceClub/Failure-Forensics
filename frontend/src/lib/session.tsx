"use client";

import { createContext, useContext, type ReactNode } from "react";

/**
 * Session stub (KAN-46).
 *
 * There is no login yet. Every visitor gets the same local developer session
 * so pages can read "who am I" and "which project" through one hook. When real
 * auth lands, replace `devSession` with data from the backend and keep the
 * `useSession()` shape so pages do not change.
 */
export type Session = {
  user: { id: string; name: string; email: string };
  project: { id: string; name: string };
  /** True while the stub is in use, so the UI can label it. */
  isStub: boolean;
};

export const devSession: Session = {
  user: { id: "dev-user", name: "Local developer", email: "dev@localhost" },
  project: {
    id: process.env.NEXT_PUBLIC_DEV_PROJECT_ID ?? "demo",
    name: process.env.NEXT_PUBLIC_DEV_PROJECT_NAME ?? "Demo project",
  },
  isStub: true,
};

const SessionContext = createContext<Session | null>(null);

export function SessionProvider({
  children,
  session = devSession,
}: {
  children: ReactNode;
  session?: Session;
}) {
  return (
    <SessionContext.Provider value={session}>
      {children}
    </SessionContext.Provider>
  );
}

export function useSession(): Session {
  const session = useContext(SessionContext);
  if (!session) {
    throw new Error("useSession must be used inside <SessionProvider>");
  }
  return session;
}
