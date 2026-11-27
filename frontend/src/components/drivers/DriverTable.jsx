import DriverRow from "./DriverRow";

function DriverTable({ drivers }) {
  const validDrivers = drivers.filter(
    (driver) => driver.best_lap != null
  );

  const fastestLap = validDrivers.length
    ? Math.min(...validDrivers.map((driver) => driver.best_lap))
    : null;

  return (
    <section className="overflow-hidden rounded-xl border border-white/10 bg-[#1a1b22]">
      <div className="border-b border-white/10 p-5">
        <h2 className="text-lg font-bold text-white">
          Driver rankings
        </h2>
        <p className="mt-1 text-sm text-gray-400">
          Ranked by fastest recorded lap
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[700px] text-left">
          <thead className="bg-white/5 text-xs uppercase tracking-wider text-gray-400">
            <tr>
              <th className="px-4 py-3">Pos</th>
              <th className="px-4 py-3">Driver</th>
              <th className="px-4 py-3">Best lap</th>
              <th className="px-4 py-3">Average lap</th>
              <th className="px-4 py-3">Laps</th>
              <th className="px-4 py-3">Gap</th>
            </tr>
          </thead>

          <tbody>
            {validDrivers.map((driver, index) => (
              <DriverRow
                key={driver.driver_number}
                driver={driver}
                position={index + 1}
                fastestLap={fastestLap}
              />
            ))}
          </tbody>
        </table>
      </div>

      {validDrivers.length === 0 && (
        <p className="p-6 text-sm text-gray-400">
          No driver lap data is available for this session.
        </p>
      )}
    </section>
  );
}

export default DriverTable;