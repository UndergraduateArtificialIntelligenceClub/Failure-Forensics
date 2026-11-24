"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { isActive, navItems } from "@/lib/navigation";

export function SideNav() {
  const pathname = usePathname() ?? "/";

  return (
    <ul className="space-y-1">
      {navItems.map((item) => {
        const active = isActive(item.href, pathname);
        return (
          <li key={item.href}>
            <Link
              href={item.href}
              aria-current={active ? "page" : undefined}
              className={`block rounded-md px-3 py-2 text-sm ${
                active
                  ? "bg-primary/15 text-primary font-medium"
                  : "hover:bg-border"
              }`}
            >
              {item.label}
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

/** Rendered while the current path is unknown (prerender with dynamic params). */
export function SideNavFallback() {
  return (
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
  );
}
