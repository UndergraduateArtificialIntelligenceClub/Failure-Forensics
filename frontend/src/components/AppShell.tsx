import Link from "next/link";
import type { ReactNode } from "react";

const navItems = [
  { label: "Overview", href: "/" },
  { label: "Traces", href: "/traces" },
  { label: "Failures", href: "/failures" },
  { label: "Evaluations", href: "/evaluations" },
  { label: "Experiments", href: "/experiments" },
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="bg-background text-foreground flex min-h-screen flex-col">
      <header className="border-border bg-surface flex h-14 items-center border-b px-4">
        <span className="text-lg font-semibold">Failure Forensics</span>
      </header>
      <div className="flex flex-1">
        <nav
          aria-label="Main"
          className="border-border bg-surface w-56 border-r p-3"
        >
          <ul className="space-y-1">
            {navItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className="hover:bg-border block rounded-md px-3 py-2 text-sm"
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
