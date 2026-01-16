export type PageResponse<T> = {
  items: T[];
  page: number;
  size: number;
  total: number;
};

export type Genre = { id: number; name: string };
export type Country = { id: number; name: string };
export type Person = { id: number; full_name: string };

export type MovieShort = {
  id: number;
  title: string;
  release_year?: number | null;
  rating?: number | null;
};

export type MovieDetails = MovieShort & {
  description?: string | null;
  genres: Genre[];
  countries: Country[];
  persons: Person[];
};
