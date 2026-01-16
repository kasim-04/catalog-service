from sqlalchemy.orm import Session

from app.models.country import Country
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.person import Person


def seed_reference_data(db: Session):
    g_action = Genre(name="Action")
    g_drama = Genre(name="Drama")

    c_usa = Country(name="USA")
    c_uk = Country(name="UK")

    p_nolan = Person(full_name="Christopher Nolan")
    p_dicaprio = Person(full_name="Leonardo DiCaprio")

    m_inception = Movie(
        title="Inception",
        description="Dreams within dreams.",
        release_year=2010,
        rating=8.8,
        genres=[g_action, g_drama],
        countries=[c_usa, c_uk],
        persons=[p_nolan, p_dicaprio],
    )

    m_memento = Movie(
        title="Memento",
        description="Memory is fragile.",
        release_year=2000,
        rating=8.4,
        genres=[g_drama],
        countries=[c_usa],
        persons=[p_nolan],
    )

    db.add_all([m_inception, m_memento])
    db.commit()

    for obj in [g_action, g_drama, c_usa, c_uk, p_nolan, p_dicaprio, m_inception, m_memento]:
        db.refresh(obj)

    return {
        "genres": {"action": g_action, "drama": g_drama},
        "countries": {"usa": c_usa, "uk": c_uk},
        "persons": {"nolan": p_nolan, "dicaprio": p_dicaprio},
        "movies": {"inception": m_inception, "memento": m_memento},
    }
