import { Suspense, type ReactNode } from "react";
import { SessionProvider } from "@/lib/session";
import { SessionBadge } from "./SessionBadge";
import { SideNav, SideNavFallback } from "./SideNav";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <SessionProvider>
      <div className="bg-background text-foreground flex min-h-screen flex-col">
        <header className="border-border bg-surface flex h-14 items-center justify-between border-b px-4">
          <span className="text-lg font-semibold">Failure Forensics</span>
          <SessionBadge />
        </header>
        <div className="flex flex-1">
          <nav
            aria-label="Main"
            className="border-border bg-surface w-56 shrink-0 border-r p-3"
          >
            {/* usePathname can suspend on routes with dynamic params
                (e.g. trace detail) when cacheComponents is on. */}
            <Suspense fallback={<SideNavFallback />}>
              <SideNav />
            </Suspense>
          </nav>
          <main className="flex-1 p-6">{children}</main>
        </div>
      </div>
    </SessionProvider>
  );
}
