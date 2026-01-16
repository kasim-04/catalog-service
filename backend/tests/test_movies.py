import pytest


def test_movies_list_sorted_by_title(client, seeded):
    r = client.get("/api/movies", params={"page": 1, "size": 10, "sort": "title"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert [m["title"] for m in data["items"]] == ["Inception", "Memento"]


def test_movies_search_by_q(client, seeded):
    r = client.get("/api/movies", params={"q": "memen"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Memento"


def test_movies_filter_by_genre_returns_expected_total(client, seeded):
    g_drama_id = seeded["genres"]["drama"].id
    r = client.get("/api/movies", params={"genre_id": [g_drama_id]})
    assert r.status_code == 200
    assert r.json()["total"] == 2


def test_movies_filter_by_country_returns_inception_only(client, seeded):
    c_uk_id = seeded["countries"]["uk"].id
    r = client.get("/api/movies", params={"country_id": [c_uk_id]})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Inception"


def test_movies_filter_by_person_returns_inception_only(client, seeded):
    p_dicaprio_id = seeded["persons"]["dicaprio"].id
    r = client.get("/api/movies", params={"person_id": [p_dicaprio_id]})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Inception"


def test_movies_sort_by_rating_desc(client, seeded):
    r = client.get("/api/movies", params={"sort": "-rating"})
    assert r.status_code == 200
    data = r.json()
    assert [m["title"] for m in data["items"]] == ["Inception", "Memento"]


def test_movie_details_returns_full_payload(client, seeded):
    inception_id = seeded["movies"]["inception"].id
    r = client.get(f"/api/movies/{inception_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == inception_id
    assert len(data["genres"]) == 2
    assert len(data["countries"]) == 2
    assert len(data["persons"]) == 2


def test_movie_details_404(client, seeded):
    r = client.get("/api/movies/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Movie not found"


@pytest.mark.parametrize(
    "params, expected_titles",
    [
        ({"year_from": 2005}, ["Inception"]),
        ({"year_to": 2005}, ["Memento"]),
        ({"rating_from": 8.6}, ["Inception"]),
        ({"rating_to": 8.6}, ["Memento"]),
    ],
)
def test_movies_numeric_filters(client, seeded, params, expected_titles):
    r = client.get("/api/movies", params=params)
    assert r.status_code == 200
    data = r.json()
    assert [m["title"] for m in data["items"]] == expected_titles
    assert data["total"] == len(expected_titles)
