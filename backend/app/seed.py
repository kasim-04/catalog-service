from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.genre import Genre
from app.models.country import Country
from app.models.person import Person
from app.models.movie import Movie


def get_or_create(db: Session, model, **kwargs):
    obj = db.query(model).filter_by(**kwargs).first()
    if obj:
        return obj
    obj = model(**kwargs)
    db.add(obj)
    db.flush()
    return obj


def seed():
    db = SessionLocal()
    try:
        # если уже есть фильмы — не сидим повторно
        if db.query(Movie).count() > 0:
            print("Seed: movies already exist, skip")
            return

        # Reference data
        genres = [
            "Action",
            "Comedy",
            "Drama",
            "Thriller",
            "Sci-Fi",
            "Fantasy",
            "Animation",
            "Adventure",
            "Mystery",
            "Crime",
        ]
        countries = ["USA", "UK", "France", "Japan", "Germany", "Canada", "South Korea", "Spain"]
        persons = [
            "Christopher Nolan",
            "Leonardo DiCaprio",
            "Keanu Reeves",
            "Hayao Miyazaki",
            "Greta Gerwig",
            "Denis Villeneuve",
            "Bong Joon-ho",
            "Natalie Portman",
            "Brad Pitt",
            "Tilda Swinton",
        ]

        genre_objs = [get_or_create(db, Genre, name=g) for g in genres]
        country_objs = [get_or_create(db, Country, name=c) for c in countries]
        person_objs = [get_or_create(db, Person, full_name=p) for p in persons]

        # Movies (50 items, deterministic)
        import random

        random.seed(42)

        curated = [
            {
                "title": "Inception",
                "description": "A thief steals secrets through dream-sharing technology.",
                "year": 2010,
                "rating": 8.8,
                "genres": ["Sci-Fi", "Thriller"],
                "countries": ["USA", "UK"],
                "persons": ["Christopher Nolan", "Leonardo DiCaprio"],
            },
            {
                "title": "The Matrix",
                "description": "A hacker discovers the world is a simulation.",
                "year": 1999,
                "rating": 8.7,
                "genres": ["Action", "Sci-Fi"],
                "countries": ["USA"],
                "persons": ["Keanu Reeves"],
            },
            {
                "title": "Spirited Away",
                "description": "A girl navigates a mysterious spirit world.",
                "year": 2001,
                "rating": 8.6,
                "genres": ["Animation", "Fantasy", "Adventure"],
                "countries": ["Japan"],
                "persons": ["Hayao Miyazaki"],
            },
        ]

        title_bases = [
            "Midnight Protocol",
            "Neon Harbor",
            "Glass Horizon",
            "Silent Meridian",
            "Crimson Circuit",
            "Paper Sky",
            "Echoes of Tomorrow",
            "Velvet Storm",
            "Shadow Atlas",
            "Last Train North",
            "The Fourth Door",
            "Moonlit Archive",
            "Winter Signal",
            "City of Ash",
            "Astra Run",
            "Hidden Orchard",
            "Terminal Bloom",
            "Kite & Stone",
            "Wild Card",
            "The Long Detour",
        ]

        movies: list[Movie] = []

        # Add curated first
        for item in curated:
            m = Movie(
                title=item["title"],
                description=item["description"],
                release_year=item["year"],
                rating=item["rating"],
            )
            m.genres = [get_or_create(db, Genre, name=g) for g in item["genres"]]
            m.countries = [get_or_create(db, Country, name=c) for c in item["countries"]]
            m.persons = [get_or_create(db, Person, full_name=p) for p in item["persons"]]
            movies.append(m)

        # Generate the rest
        target_total = 50
        while len(movies) < target_total:
            base = random.choice(title_bases)
            suffix = f" #{len(movies)+1:02d}"
            title = base + suffix
            year = random.randint(1985, 2025)
            rating = round(random.uniform(5.5, 9.1), 1)

            g_count = random.randint(1, 3)
            c_count = random.randint(1, 2)
            p_count = random.randint(1, 3)

            m = Movie(
                title=title,
                description=f"{base}: a story of choices, consequences, and unexpected turns.",
                release_year=year,
                rating=rating,
            )
            m.genres = [get_or_create(db, Genre, name=g) for g in random.sample(genres, k=g_count)]
            m.countries = [get_or_create(db, Country, name=c) for c in random.sample(countries, k=c_count)]
            m.persons = [get_or_create(db, Person, full_name=p) for p in random.sample(persons, k=p_count)]
            movies.append(m)

        db.add_all(movies)
        db.commit()
        print("Seed: done")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
