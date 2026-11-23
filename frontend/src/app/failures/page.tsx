import type { Metadata } from "next";
import { PagePlaceholder } from "@/components/PagePlaceholder";

export const metadata: Metadata = { title: "Failures · Failure Forensics" };

export default function FailuresPage() {
  return <PagePlaceholder href="/failures" />;
}
