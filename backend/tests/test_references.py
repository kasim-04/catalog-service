import pytest


def test_genres_list_returns_all_sorted(client, seeded):
    r = client.get("/api/genres", params={"page": 1, "size": 10})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert [g["name"] for g in data["items"]] == ["Action", "Drama"]


def test_genres_search_returns_drama_only(client, seeded):
    r = client.get("/api/genres", params={"search": "dra"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Drama"


def test_countries_list_returns_total(client, seeded):
    r = client.get("/api/countries")
    assert r.status_code == 200
    assert r.json()["total"] == 2


@pytest.mark.parametrize(
    "search, expected_total, expected_first_name",
    [
        ("u", 2, "UK"),
        ("uk", 1, "UK"),
    ],
)
def test_countries_search(client, seeded, search, expected_total, expected_first_name):
    r = client.get("/api/countries", params={"search": search})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == expected_total
    assert data["items"][0]["name"] == expected_first_name


def test_persons_search_returns_nolan(client, seeded):
    r = client.get("/api/persons", params={"search": "nolan"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["full_name"] == "Christopher Nolan"
