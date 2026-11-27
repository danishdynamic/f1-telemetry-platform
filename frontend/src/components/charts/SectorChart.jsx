
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

function SectorChart({ drivers }) {
  const chartData = [...drivers]
    .filter(
      (driver) =>
        driver.best_sector_1 != null &&
        driver.best_sector_2 != null &&
        driver.best_sector_3 != null
    )
    .sort((a, b) => a.best_sector_1 - b.best_sector_1)
    .slice(0, 10)
    .map((driver) => ({
      driver: driver.acronym,
      sector1: Number(driver.best_sector_1.toFixed(3)),
      sector2: Number(driver.best_sector_2.toFixed(3)),
      sector3: Number(driver.best_sector_3.toFixed(3)),
    }));

  return (
    <section className="rounded-xl border border-white/10 bg-[#1a1b22] p-5">
      <h2 className="text-lg font-bold text-white">
        Best sector times
      </h2>

      <p className="mb-5 mt-1 text-sm text-gray-400">
        Fastest recorded individual sector per driver
      </p>

      <div className="h-80 w-full">
        {chartData.length === 0 ? (
          <p className="pt-8 text-sm text-gray-400">
            Sector data is unavailable.
          </p>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid stroke="#30313a" strokeDasharray="3 3" />

              <XAxis
                dataKey="driver"
                stroke="#9ca3af"
              />

              <YAxis stroke="#9ca3af" />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#1a1b22",
                  border: "1px solid #444",
                  borderRadius: "8px",
                }}
              />

              <Bar dataKey="sector1" name="Sector 1" fill="#ef4444" />
              <Bar dataKey="sector2" name="Sector 2" fill="#3b82f6" />
              <Bar dataKey="sector3" name="Sector 3" fill="#22c55e" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </section>
  );
}

export default SectorChart;
