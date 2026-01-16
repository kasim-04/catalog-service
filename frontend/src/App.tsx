import { Routes, Route, Navigate } from "react-router-dom";
import CatalogPage from "./pages/CatalogPage";
import SearchPage from "./pages/SearchPage";
import MoviePage from "./pages/MoviePage";
import PersonPage from "./pages/PersonPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<CatalogPage />} />
      <Route path="/search" element={<SearchPage />} />
      <Route path="/movies/:id" element={<MoviePage />} />
      <Route path="/persons/:id" element={<PersonPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
