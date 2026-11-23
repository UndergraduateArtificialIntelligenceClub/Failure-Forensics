import type { Metadata } from "next";
import { PagePlaceholder } from "@/components/PagePlaceholder";

export const metadata: Metadata = { title: "Settings · Failure Forensics" };

export default function SettingsPage() {
  return <PagePlaceholder href="/settings" />;
}
