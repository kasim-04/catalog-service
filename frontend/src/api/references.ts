import { apiGet } from "./client";
import type { Country, Genre, PageResponse, Person } from "./types";

function qs(params: Record<string, string | number | undefined>) {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === "") continue;
    q.set(k, String(v));
  }
  const s = q.toString();
  return s ? `?${s}` : "";
}

export function getGenres(params?: { search?: string; page?: number; size?: number }) {
  return apiGet<PageResponse<Genre>>(`/api/genres${qs(params ?? {})}`);
}

export function getCountries(params?: { search?: string; page?: number; size?: number }) {
  return apiGet<PageResponse<Country>>(`/api/countries${qs(params ?? {})}`);
}

export function getPersons(params?: { search?: string; page?: number; size?: number }) {
  return apiGet<PageResponse<Person>>(`/api/persons${qs(params ?? {})}`);
}
