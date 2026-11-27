function DashboardHeader() {
  return (
    <header className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-xs font-bold tracking-[0.25em] text-red-500">
          F1 TELEMETRY PLATFORM
        </p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-white">
          Driver Performance
        </h1>
        <p className="mt-1 text-sm text-gray-400">
          Compare driver pace and sector performance.
        </p>
      </div>

      <div className="rounded-lg border border-white/10 bg-white/5 px-4 py-2">
        <span className="text-xs text-gray-400">DATA SOURCE</span>
        <p className="text-sm font-semibold text-white">OpenF1</p>
      </div>
    </header>
  );
}

export default DashboardHeader;