function StatCard({ title, value, description }) {
  return (
    <article className="rounded-xl border border-white/10 bg-[#1a1b22] p-5">
      <p className="text-sm text-gray-400">{title}</p>

      <h2 className="mt-3 text-3xl font-bold text-white">
        {value}
      </h2>

      <p className="mt-2 text-xs text-gray-500">
        {description}
      </p>
    </article>
  );
}

export default StatCard;