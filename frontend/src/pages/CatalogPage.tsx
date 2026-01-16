import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import Header from "../components/Header";
import { getMovies } from "../api/movies";
import { getCountries, getGenres } from "../api/references";
import type { Country, Genre, MovieShort } from "../api/types";

export default function CatalogPage() {
  // справочники
  const [genres, setGenres] = useState<Genre[]>([]);
  const [countries, setCountries] = useState<Country[]>([]);

  // фильтры
  const [selectedGenreIds, setSelectedGenreIds] = useState<number[]>([]);
  const [selectedCountryIds, setSelectedCountryIds] = useState<number[]>([]);
  const [yearFrom, setYearFrom] = useState<number | undefined>(undefined);
  const [yearTo, setYearTo] = useState<number | undefined>(undefined);
  const [ratingFrom, setRatingFrom] = useState<number | undefined>(undefined);
  const [ratingTo, setRatingTo] = useState<number | undefined>(undefined);
  const [sort, setSort] = useState<string>("-rating");

  // UI
  const [filtersOpen, setFiltersOpen] = useState(false);

  // список
  const [movies, setMovies] = useState<MovieShort[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const size = 10;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // сколько активных фильтров выбрано (для бейджа)
  const activeFiltersCount = useMemo(() => {
    let n = 0;
    n += selectedGenreIds.length;
    n += selectedCountryIds.length;
    if (yearFrom !== undefined) n += 1;
    if (yearTo !== undefined) n += 1;
    if (ratingFrom !== undefined) n += 1;
    if (ratingTo !== undefined) n += 1;
    // sort не считаем как “фильтр”, чтобы не было странно
    return n;
  }, [selectedGenreIds, selectedCountryIds, yearFrom, yearTo, ratingFrom, ratingTo]);

  // загрузка справочников
  useEffect(() => {
    Promise.all([getGenres({ page: 1, size: 100 }), getCountries({ page: 1, size: 100 })])
      .then(([g, c]) => {
        setGenres(g.items);
        setCountries(c.items);
      })
      .catch((e) => setError(String(e)));
  }, []);

  async function loadMovies(targetPage: number) {
    setLoading(true);
    setError(null);
    try {
      const data = await getMovies({
        page: targetPage,
        size,
        sort,
        genre_id: selectedGenreIds,
        country_id: selectedCountryIds,
        year_from: yearFrom,
        year_to: yearTo,
        rating_from: ratingFrom,
        rating_to: ratingTo,
      });
      setMovies(data.items);
      setTotal(data.total);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  // первичная загрузка
  useEffect(() => {
    loadMovies(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // при смене страницы — грузим текущие фильтры
  useEffect(() => {
    loadMovies(page);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page]);

  // Смена сортировки — сразу применяем (удобно, сортировка не требует Apply)
  useEffect(() => {
    setPage(1);
    loadMovies(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sort]);

  const totalPages = useMemo(() => Math.max(1, Math.ceil(total / size)), [total, size]);

  function toggleId(list: number[], id: number) {
    return list.includes(id) ? list.filter((x) => x !== id) : [...list, id];
  }

  function applyFilters() {
    setPage(1);
    loadMovies(1);
  }

  function resetFilters() {
    setSelectedGenreIds([]);
    setSelectedCountryIds([]);
    setYearFrom(undefined);
    setYearTo(undefined);
    setRatingFrom(undefined);
    setRatingTo(undefined);
    setSort("-rating");
    setPage(1);
    loadMovies(1);
  }

  return (
    <div style={{ padding: 16, fontFamily: "system-ui", maxWidth: 1000, margin: "0 auto" }}>
      <Header />

      {/* Filters (collapsible) */}
      <section
        style={{
          border: "1px solid #e5e5e5",
          borderRadius: 14,
          padding: 14,
          marginBottom: 16,
        }}
      >
        <button
          type="button"
          onClick={() => setFiltersOpen((v) => !v)}
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "10px 12px",
            borderRadius: 12,
            border: "1px solid #eee",
            background: "#fff",
            cursor: "pointer",
            fontWeight: 700,
          }}
        >
          <span>
            Фильтры{activeFiltersCount ? ` (${activeFiltersCount})` : ""}
          </span>
          <span style={{ color: "#666" }}>{filtersOpen ? "▲" : "▼"}</span>
        </button>

        {filtersOpen && (
          <div style={{ marginTop: 12 }}>
            {/* чекбоксы */}
            <div style={{ display: "grid", gap: 12, gridTemplateColumns: "1fr 1fr" }}>
              <fieldset style={{ border: "1px solid #eee", borderRadius: 12, padding: 12 }}>
                <legend style={{ padding: "0 6px", color: "#444" }}>Жанры</legend>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fill, minmax(170px, 1fr))",
                    gap: 8,
                    marginTop: 6,
                  }}
                >
                  {genres.map((g) => (
                    <label key={g.id} style={{ display: "flex", gap: 8, alignItems: "center" }}>
                      <input
                        type="checkbox"
                        checked={selectedGenreIds.includes(g.id)}
                        onChange={() => setSelectedGenreIds((prev) => toggleId(prev, g.id))}
                      />
                      {g.name}
                    </label>
                  ))}
                </div>
              </fieldset>

              <fieldset style={{ border: "1px solid #eee", borderRadius: 12, padding: 12 }}>
                <legend style={{ padding: "0 6px", color: "#444" }}>Страны</legend>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fill, minmax(170px, 1fr))",
                    gap: 8,
                    marginTop: 6,
                  }}
                >
                  {countries.map((c) => (
                    <label key={c.id} style={{ display: "flex", gap: 8, alignItems: "center" }}>
                      <input
                        type="checkbox"
                        checked={selectedCountryIds.includes(c.id)}
                        onChange={() => setSelectedCountryIds((prev) => toggleId(prev, c.id))}
                      />
                      {c.name}
                    </label>
                  ))}
                </div>
              </fieldset>
            </div>

            {/* числовые фильтры */}
            <div
              style={{
                display: "grid",
                gap: 12,
                gridTemplateColumns: "1fr 1fr 1fr 1fr",
                marginTop: 12,
              }}
            >
              <label style={{ display: "grid", gap: 6 }}>
                Год от
                <input
                  type="number"
                  value={yearFrom ?? ""}
                  onChange={(e) => setYearFrom(e.target.value ? Number(e.target.value) : undefined)}
                />
              </label>

              <label style={{ display: "grid", gap: 6 }}>
                Год до
                <input
                  type="number"
                  value={yearTo ?? ""}
                  onChange={(e) => setYearTo(e.target.value ? Number(e.target.value) : undefined)}
                />
              </label>

              <label style={{ display: "grid", gap: 6 }}>
                Рейтинг от
                <input
                  type="number"
                  step="0.1"
                  value={ratingFrom ?? ""}
                  onChange={(e) => setRatingFrom(e.target.value ? Number(e.target.value) : undefined)}
                />
              </label>

              <label style={{ display: "grid", gap: 6 }}>
                Рейтинг до
                <input
                  type="number"
                  step="0.1"
                  value={ratingTo ?? ""}
                  onChange={(e) => setRatingTo(e.target.value ? Number(e.target.value) : undefined)}
                />
              </label>
            </div>

            <div style={{ display: "flex", gap: 10, alignItems: "center", marginTop: 12, flexWrap: "wrap" }}>
              <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
                Сортировка
                <select value={sort} onChange={(e) => setSort(e.target.value)}>
                  <option value="-rating">Рейтинг (убыв.)</option>
                  <option value="rating">Рейтинг (возр.)</option>
                  <option value="-year">Год (новые)</option>
                  <option value="year">Год (старые)</option>
                  <option value="title">Название A→Z</option>
                  <option value="-title">Название Z→A</option>
                </select>
              </label>

              <div style={{ marginLeft: "auto", display: "flex", gap: 10 }}>
                <button onClick={resetFilters} style={{ padding: "8px 12px", borderRadius: 10 }}>
                  Reset
                </button>
                <button onClick={applyFilters} style={{ padding: "8px 12px", borderRadius: 10 }}>
                  Apply filters
                </button>
              </div>
            </div>
          </div>
        )}
      </section>

      {/* Movies */}
      <section>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 10 }}>
          <h2 style={{ margin: 0 }}>Фильмы</h2>
          <div style={{ color: "#555" }}>
            Found: <b>{total}</b>
          </div>
        </div>

        {error && <pre style={{ color: "crimson", whiteSpace: "pre-wrap" }}>{error}</pre>}
        {loading ? (
          <p>Loading...</p>
        ) : movies.length === 0 ? (
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
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div>
                  <div style={{ fontSize: 18, fontWeight: 700 }}>{m.title}</div>
                  <div style={{ color: "#666", marginTop: 4 }}>
                    {m.release_year ?? "—"} · rating {m.rating ?? "—"}
                  </div>
                </div>
                <div style={{ color: "#999" }}>Open →</div>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Pagination */}
      <div style={{ display: "flex", gap: 10, marginTop: 16, alignItems: "center" }}>
        <button
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page <= 1}
          style={{ padding: "8px 12px", borderRadius: 10 }}
        >
          Prev
        </button>

        <span style={{ color: "#555" }}>
          Page <b>{page}</b> / {totalPages}
        </span>

        <button
          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          disabled={page >= totalPages}
          style={{ padding: "8px 12px", borderRadius: 10 }}
        >
          Next
        </button>
      </div>
    </div>
  );
}
