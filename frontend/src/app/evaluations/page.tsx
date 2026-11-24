import type { Metadata } from "next";
import { PagePlaceholder } from "@/components/PagePlaceholder";

export const metadata: Metadata = { title: "Evaluations · Failure Forensics" };

export default function EvaluationsPage() {
  return <PagePlaceholder href="/evaluations" />;
}
