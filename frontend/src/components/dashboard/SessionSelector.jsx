function SessionSelector({ sessions, selectedSession, onChange }) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-sm font-medium text-gray-300">
        Select race session
      </label>

      <select
        value={selectedSession}
        onChange={(event) => onChange(Number(event.target.value))}
        className="rounded-lg border border-white/10 bg-[#1a1b22] px-4 py-3 text-sm text-white outline-none focus:border-red-500"
      >
        <option value="">Choose a session</option>

        {sessions
          .filter((session) => session.session_type === "Race")
          .map((session) => (
            <option
              key={session.session_key}
              value={session.session_key}
            >
              {session.country_name} — {session.session_name}
            </option>
          ))}
      </select>
    </div>
  );
}

export default SessionSelector;