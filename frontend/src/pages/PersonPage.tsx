import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Header from "../components/Header";
import { getMovies } from "../api/movies";
import { getPersons } from "../api/references";
import type { MovieShort, Person } from "../api/types";

async function fetchAllMoviesByPerson(personId: number): Promise<MovieShort[]> {
  const pageSize = 100; // ограничение бэка
  let page = 1;
  const all: MovieShort[] = [];

  while (true) {
    const resp = await getMovies({
      person_id: [personId],
      page,
      size: pageSize,
      sort: "-rating",
    });

    all.push(...resp.items);

    // если пришло меньше pageSize — это последняя страница
    if (resp.items.length < pageSize) break;

    page += 1;

    // safety guard, чтобы не уйти в бесконечность (на всякий случай)
    if (page > 50) break;
  }

  return all;
}

async function findPersonNameById(personId: number): Promise<string | null> {
  const pageSize = 100;
  let page = 1;

  while (true) {
    const resp = await getPersons({ page, size: pageSize });

    const found: Person | undefined = resp.items.find((x) => x.id === personId);
    if (found) return found.full_name;

    // если это последняя страница — прекращаем
    if (resp.items.length < pageSize) break;

    page += 1;

    // safety guard
    if (page > 50) break;
  }

  return null;
}

export default function PersonPage() {
  const { id } = useParams();
  const personId = Number(id);

  const [personName, setPersonName] = useState<string>("(неизвестно)");
  const [movies, setMovies] = useState<MovieShort[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!Number.isFinite(personId)) {
      setError("Invalid person id");
      return;
    }

    setLoading(true);
    setError(null);

    Promise.all([findPersonNameById(personId), fetchAllMoviesByPerson(personId)])
      .then(([name, ms]) => {
        setPersonName(name ?? `Person #${personId}`);
        setMovies(ms);
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [personId]);

  const title = useMemo(() => `Фильмы с участием ${personName}`, [personName]);

  return (
    <div style={{ padding: 16, fontFamily: "system-ui", maxWidth: 1000, margin: "0 auto" }}>
      <Header />

      <h2 style={{ marginTop: 0 }}>{title}</h2>

      {error && <pre style={{ color: "crimson", whiteSpace: "pre-wrap" }}>{error}</pre>}
      {loading && <p>Loading...</p>}

      {!loading &&
        (movies.length === 0 ? (
          <p style={{ color: "#666" }}>Фильмов не найдено</p>
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
        ))}
    </div>
  );
}
