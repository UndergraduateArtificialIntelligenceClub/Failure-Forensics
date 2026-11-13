export default function Home() {
  return (
    <div>
      <h1 className="text-2xl font-semibold">Overview</h1>
      <p className="text-muted mt-2">
        The console scaffold is ready. Screens are added in later sprints.
      </p>
      <div className="mt-6 flex gap-3">
        <span className="bg-success rounded-full px-3 py-1 text-sm text-white">
          Healthy
        </span>
        <span className="bg-warning rounded-full px-3 py-1 text-sm text-white">
          Degraded
        </span>
        <span className="bg-danger rounded-full px-3 py-1 text-sm text-white">
          Failed
        </span>
      </div>
    </div>
  );
}
