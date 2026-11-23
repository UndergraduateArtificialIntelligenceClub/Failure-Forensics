import type { Metadata } from "next";
import { PagePlaceholder } from "@/components/PagePlaceholder";

export const metadata: Metadata = { title: "Traces · Failure Forensics" };

export default function TracesPage() {
  return <PagePlaceholder href="/traces" />;
}
