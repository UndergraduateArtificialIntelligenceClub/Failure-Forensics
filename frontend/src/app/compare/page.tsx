import type { Metadata } from "next";
import { PagePlaceholder } from "@/components/PagePlaceholder";

export const metadata: Metadata = { title: "Compare · Failure Forensics" };

export default function ComparePage() {
  return <PagePlaceholder href="/compare" />;
}
