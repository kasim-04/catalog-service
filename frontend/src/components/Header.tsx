import { Link, useLocation } from "react-router-dom";

type Props = {
  title?: string;
};

export default function Header({ title = "🎬 Cinema Catalog" }: Props) {
  const { pathname } = useLocation();

  const linkStyle = (active: boolean): React.CSSProperties => ({
    textDecoration: "none",
    padding: "6px 10px",
    borderRadius: 10,
    border: "1px solid #e5e5e5",
    background: active ? "#f6f6f6" : "white",
    color: "inherit",
  });

  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 12,
        marginBottom: 16,
      }}
    >
      <h1 style={{ margin: 0 }}>{title}</h1>

      <nav style={{ display: "flex", gap: 10, alignItems: "center" }}>
        <Link to="/" style={linkStyle(pathname === "/")}>
          Каталог
        </Link>
        <Link to="/search" style={linkStyle(pathname.startsWith("/search"))}>
          Поиск
        </Link>
      </nav>
    </header>
  );
}
