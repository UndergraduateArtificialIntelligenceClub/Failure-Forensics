import type { Metadata } from "next";
import { PagePlaceholder } from "@/components/PagePlaceholder";

export const metadata: Metadata = { title: "Experiments · Failure Forensics" };

export default function ExperimentsPage() {
  return <PagePlaceholder href="/experiments" />;
}
