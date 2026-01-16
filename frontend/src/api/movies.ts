import { apiGet } from "./client";
import type { MovieDetails, MovieShort, PageResponse } from "./types";

function qs(params: Record<string, any>) {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === "") continue;

    // массивы параметров: genre_id=1&genre_id=2
    if (Array.isArray(v)) {
      v.forEach((item) => q.append(k, String(item)));
    } else {
      q.set(k, String(v));
    }
  }
  const s = q.toString();
  return s ? `?${s}` : "";
}

export function getMovies(params: {
  q?: string;
  genre_id?: number[];
  country_id?: number[];
  person_id?: number[];
  year_from?: number;
  year_to?: number;
  rating_from?: number;
  rating_to?: number;
  sort?: string;
  page?: number;
  size?: number;
}) {
  return apiGet<PageResponse<MovieShort>>(`/api/movies${qs(params)}`);
}

export function getMovieById(id: number) {
  return apiGet<MovieDetails>(`/api/movies/${id}`);
}
