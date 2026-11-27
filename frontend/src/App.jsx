
import { useEffect, useState } from "react";

import DashboardHeader from "./components/dashboard/DashboardHeader";
import StatCard from "./components/dashboard/StatCard";
import SessionSelector from "./components/dashboard/SessionSelector";

import DriverTable from "./components/drivers/DriverTable";
import SectorChart from "./components/charts/SectorChart";

import {
  getSessions,
  getDriverPerformance,
} from "./services/driverService";

function App() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState("");
  const [drivers, setDrivers] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Load the available 2025 sessions when the page opens.
  useEffect(() => {
    async function loadSessions() {
      try {
        const data = await getSessions(2025);
        setSessions(data.sessions || []);
      } catch {
        setError("Unable to load sessions from the backend.");
      }
    }

    loadSessions();
  }, []);

  // Load performance whenever the selected race changes.
  useEffect(() => {
    if (!selectedSession) {
      setDrivers([]);
      return;
    }

    async function loadPerformance() {
      setLoading(true);
      setError("");

      try {
        const data = await getDriverPerformance(selectedSession);
        setDrivers(data.drivers || []);
      } catch {
        setDrivers([]);
        setError("Unable to load driver performance.");
      } finally {
        setLoading(false);
      }
    }

    loadPerformance();
  }, [selectedSession]);

  const totalLaps = drivers.reduce(
    (total, driver) => total + driver.lap_count,
    0
  );

  return (
    <main className="min-h-screen bg-[#101116] px-4 py-8 text-white sm:px-8">
      <div className="mx-auto max-w-7xl space-y-8">

        <DashboardHeader />

        <div className="max-w-md">
          <SessionSelector
            sessions={sessions}
            selectedSession={selectedSession}
            onChange={setSelectedSession}
          />
        </div>

        {error && (
          <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-300">
            {error}
          </div>
        )}

        {!selectedSession && (
          <div className="rounded-xl border border-dashed border-white/20 p-10 text-center">
            <h2 className="text-lg font-semibold">
              Select a race session
            </h2>
            <p className="mt-2 text-sm text-gray-400">
              Choose a race above to explore driver performance.
            </p>
          </div>
        )}

        {selectedSession && (
          <>
            <section className="grid gap-4 sm:grid-cols-2">
              <StatCard
                title="Drivers"
                value={drivers.length}
                description="Drivers with recorded lap data"
              />

              <StatCard
                title="Laps recorded"
                value={totalLaps}
                description="Valid recorded laps counted in the API summary"
              />
            </section>

            {loading ? (
              <p className="py-12 text-center text-gray-400">
                Loading driver performance...
              </p>
            ) : (
              <>
                <DriverTable drivers={drivers} />
                <SectorChart drivers={drivers} />
              </>
            )}
          </>
        )}

      </div>
    </main>
  );
}

export default App;
