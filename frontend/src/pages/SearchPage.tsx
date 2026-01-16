import { useState } from "react";
import { Link } from "react-router-dom";
import Header from "../components/Header";
import { getMovies } from "../api/movies";
import { getPersons } from "../api/references";
import type { MovieShort, Person } from "../api/types";

export default function SearchPage() {
  const [q, setQ] = useState("");
  const [movies, setMovies] = useState<MovieShort[]>([]);
  const [persons, setPersons] = useState<Person[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function doSearch() {
    const query = q.trim();
    if (!query) {
      setMovies([]);
      setPersons([]);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const [m, p] = await Promise.all([
        getMovies({ q: query, page: 1, size: 20, sort: "-rating" }),
        getPersons({ search: query, page: 1, size: 50 }),
      ]);
      setMovies(m.items);
      setPersons(p.items);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 16, fontFamily: "system-ui", maxWidth: 1000, margin: "0 auto" }}>
      <Header />

      <h2 style={{ marginTop: 0 }}>Поиск</h2>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          doSearch();
        }}
        style={{ display: "flex", gap: 8, marginBottom: 16 }}
      >
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Введите запрос (фильм или персона)..."
          style={{ flex: 1, padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
        />
        <button type="submit" style={{ padding: "10px 14px", borderRadius: 10 }}>
          Искать
        </button>
      </form>

      {error && <pre style={{ color: "crimson", whiteSpace: "pre-wrap" }}>{error}</pre>}
      {loading && <p>Loading...</p>}

      {!loading && (
        <div style={{ display: "grid", gap: 18 }}>
          <section>
            <h3 style={{ marginBottom: 10 }}>Фильмы</h3>
            {movies.length === 0 ? (
              <p style={{ color: "#666" }}>Ничего не найдено</p>
            ) : (
              <div style={{ display: "grid", gap: 10 }}>
                {movies.map((m) => (
                  <Link
                    key={m.id}
                    to={`/movies/${m.id}`}
                    style={{
                      textDecoration: "none",
                      color: "inherit",
                      border: "1px solid #e5e5e5",
                      borderRadius: 12,
                      padding: 12,
                    }}
                  >
                    <div style={{ fontSize: 18, fontWeight: 700 }}>{m.title}</div>
                    <div style={{ color: "#666", marginTop: 4 }}>
                      {m.release_year ?? "—"} · rating {m.rating ?? "—"}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </section>

          <section>
            <h3 style={{ marginBottom: 10 }}>Персоны</h3>
            {persons.length === 0 ? (
              <p style={{ color: "#666" }}>Ничего не найдено</p>
            ) : (
              <ul style={{ margin: 0, paddingLeft: 18 }}>
                {persons.map((p) => (
                  <li key={p.id}>
                    <Link to={`/persons/${p.id}`}>{p.full_name}</Link>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      )}
    </div>
  );
}
