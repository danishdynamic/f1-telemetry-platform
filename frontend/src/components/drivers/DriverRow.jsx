function formatLapTime(seconds) {
  if (seconds == null) return "N/A";

  const minutes = Math.floor(seconds / 60);
  const remaining = (seconds % 60).toFixed(3);

  return `${minutes}:${remaining.padStart(6, "0")}`;
}

function DriverRow({ driver, position, fastestLap }) {
  const teamColour = driver.team_colour
    ? `#${driver.team_colour.replace("#", "")}`
    : "#6b7280";

  return (
    <tr className="border-b border-white/5 transition hover:bg-white/5">
      <td className="px-4 py-4 text-gray-400">{position}</td>

      <td className="px-4 py-4">
        <div className="flex items-center gap-3">
          <div
            className="h-9 w-1 rounded-full"
            style={{ backgroundColor: teamColour }}
          />

          <div>
            <p className="font-semibold text-white">
              {driver.name || driver.acronym}
            </p>
            <p className="text-xs text-gray-500">
              {driver.team}
            </p>
          </div>
        </div>
      </td>

      <td className="px-4 py-4 font-mono text-sm text-white">
        {formatLapTime(driver.best_lap)}
      </td>

      <td className="px-4 py-4 font-mono text-sm text-gray-300">
        {formatLapTime(driver.average_lap)}
      </td>

      <td className="px-4 py-4 text-sm text-gray-300">
        {driver.lap_count}
      </td>

      <td className="px-4 py-4 font-mono text-sm text-red-400">
        {driver.best_lap != null && fastestLap != null
          ? `+${(driver.best_lap - fastestLap).toFixed(3)}s`
          : "N/A"}
      </td>
    </tr>
  );
}

export default DriverRow;