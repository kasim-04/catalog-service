import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header";
import { getMovieById } from "../api/movies";
import type { MovieDetails } from "../api/types";

export default function MoviePage() {
  const { id } = useParams();
  const movieId = Number(id);

  const [movie, setMovie] = useState<MovieDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!Number.isFinite(movieId)) {
      setError("Invalid movie id");
      return;
    }

    setLoading(true);
    setError(null);

    getMovieById(movieId)
      .then((m) => setMovie(m))
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [movieId]);

  return (
    <div style={{ padding: 16, fontFamily: "system-ui", maxWidth: 1000, margin: "0 auto" }}>
      <Header />

      {error && <pre style={{ color: "crimson", whiteSpace: "pre-wrap" }}>{error}</pre>}
      {loading && <p>Loading...</p>}

      {movie && (
        <div style={{ border: "1px solid #e5e5e5", borderRadius: 12, padding: 16 }}>
          <h2 style={{ marginTop: 0 }}>{movie.title}</h2>
          <p style={{ color: "#666" }}>
            {movie.release_year ?? "—"} · rating {movie.rating ?? "—"}
          </p>

          {movie.description && <p>{movie.description}</p>}

          <hr style={{ border: 0, borderTop: "1px solid #eee", margin: "16px 0" }} />

          <div style={{ display: "grid", gap: 10 }}>
            <div>
              <b>Genres:</b> {movie.genres.length ? movie.genres.map((g) => g.name).join(", ") : "—"}
            </div>
            <div>
              <b>Countries:</b>{" "}
              {movie.countries.length ? movie.countries.map((c) => c.name).join(", ") : "—"}
            </div>
            <div>
              <b>Persons:</b>{" "}
              {movie.persons.length ? movie.persons.map((p) => p.full_name).join(", ") : "—"}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
