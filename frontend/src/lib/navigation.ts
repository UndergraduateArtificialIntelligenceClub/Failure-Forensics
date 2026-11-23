/**
 * Main console navigation (KAN-46).
 *
 * Order and labels follow the KAN-31 wireframes (docs/design/wireframes.md).
 * "Live traces" is a stretch goal and is left out; trace detail has no menu
 * item because it opens from a row on the Traces page.
 */
export type NavItem = {
  label: string;
  href: string;
  /** One-line purpose, shown on the stub page until the screen is built. */
  description: string;
  /** Jira story that builds the real screen. */
  jira: string;
};

export const navItems: readonly NavItem[] = [
  {
    label: "Overview",
    href: "/",
    description: "Health of your AI pipelines at a glance.",
    jira: "KAN-129",
  },
  {
    label: "Traces",
    href: "/traces",
    description:
      "Search and filter traces by status, health, version and date.",
    jira: "KAN-47",
  },
  {
    label: "Failures",
    href: "/failures",
    description: "Diagnoses with root cause, category and confidence.",
    jira: "KAN-83",
  },
  {
    label: "Compare",
    href: "/compare",
    description:
      "A healthy trace next to a failed one, with the first divergence.",
    jira: "KAN-110",
  },
  {
    label: "Evaluations",
    href: "/evaluations",
    description: "Regression runs against your datasets.",
    jira: "KAN-118",
  },
  {
    label: "Experiments",
    href: "/experiments",
    description: "Compare pipeline versions side by side.",
    jira: "KAN-128",
  },
  {
    label: "Datasets",
    href: "/datasets",
    description: "Golden, failure and injected-fault cases.",
    jira: "KAN-118",
  },
  {
    label: "Analytics",
    href: "/analytics",
    description: "Failures over time, cost and latency.",
    jira: "KAN-129",
  },
  {
    label: "Settings",
    href: "/settings",
    description: "Projects, API keys and capture policy.",
    jira: "KAN-69",
  },
];

/** True when `pathname` is the nav item's page or a page below it. */
export function isActive(href: string, pathname: string): boolean {
  if (href === "/") return pathname === "/";
  return pathname === href || pathname.startsWith(`${href}/`);
}

export function getNavItem(href: string): NavItem {
  const item = navItems.find((entry) => entry.href === href);
  if (!item) throw new Error(`No nav item for ${href}`);
  return item;
}
