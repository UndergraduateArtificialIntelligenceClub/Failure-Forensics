import { getNavItem } from "@/lib/navigation";

/** Stub page for a nav entry whose screen is built in a later sprint. */
export function PagePlaceholder({ href }: { href: string }) {
  const item = getNavItem(href);

  return (
    <div>
      <h1 className="text-2xl font-semibold">{item.label}</h1>
      <p className="text-muted mt-2">{item.description}</p>
      <p className="border-border text-muted mt-6 rounded-md border border-dashed p-4 text-sm">
        This screen is not built yet. It is planned in{" "}
        <a
          className="text-primary underline"
          href={`https://pranav01.atlassian.net/browse/${item.jira}`}
        >
          {item.jira}
        </a>
        .
      </p>
    </div>
  );
}
