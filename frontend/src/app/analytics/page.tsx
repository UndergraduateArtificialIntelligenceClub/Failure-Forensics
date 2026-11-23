import type { Metadata } from "next";
import { PagePlaceholder } from "@/components/PagePlaceholder";

export const metadata: Metadata = { title: "Analytics · Failure Forensics" };

export default function AnalyticsPage() {
  return <PagePlaceholder href="/analytics" />;
}
