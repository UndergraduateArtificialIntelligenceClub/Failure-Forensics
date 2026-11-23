import type { Metadata } from "next";
import { PagePlaceholder } from "@/components/PagePlaceholder";

export const metadata: Metadata = { title: "Datasets · Failure Forensics" };

export default function DatasetsPage() {
  return <PagePlaceholder href="/datasets" />;
}
