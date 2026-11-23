import type { Metadata } from "next";
import { Suspense } from "react";
import { TraceTableSkeleton } from "@/components/traces/TraceTable";
import { TracesView } from "@/components/traces/TracesView";

export const metadata: Metadata = { title: "Traces · Failure Forensics" };

export default function TracesPage() {
  // TracesView reads the filters from the URL (useSearchParams), so it renders
  // in the browser; the skeleton is what gets prerendered.
  return (
    <Suspense fallback={<TraceTableSkeleton />}>
      <TracesView />
    </Suspense>
  );
}
