import pytest
from types import SimpleNamespace

# IMPORTANT: import the module, not just the functions,
# so monkeypatch can patch module-level selectors/repositories.
from core.application.services import reviews_service as reviews_services


def test_get_reviews_calls_selectors_list_reviews_with_filters(monkeypatch):
    expected = [{"id": 1}]

    def fake_list_reviews(*, artist_id=None, album_id=None):
        assert artist_id == "123"
        assert album_id == "A1"
        return expected

    monkeypatch.setattr(reviews_services.selectors, "list_reviews", fake_list_reviews)

    out = reviews_services.get_reviews(artist_id="123", album_id="A1")
    assert out == expected


def test_get_reviews_calls_selectors_list_reviews_without_filters(monkeypatch):
    expected = [{"id": 1}, {"id": 2}]

    def fake_list_reviews(*, artist_id=None, album_id=None):
        assert artist_id is None
        assert album_id is None
        return expected

    monkeypatch.setattr(reviews_services.selectors, "list_reviews", fake_list_reviews)

    out = reviews_services.get_reviews()
    assert out == expected


def test_create_new_review_calls_repositories_create_review(monkeypatch):
    user = SimpleNamespace(username="alice")
    validated_data = {"title": "t", "artist": "a", "content": "c", "rating": 5}
    expected = {"id": 99}

    def fake_create_review(*, user, data):
        assert user.username == "alice"
        assert data == validated_data
        return expected

    monkeypatch.setattr(reviews_services.repositories, "create_review", fake_create_review)

    out = reviews_services.create_new_review(user=user, validated_data=validated_data)
    assert out == expected


def test_delete_review_as_admin_denies_non_admin(monkeypatch):
    user = SimpleNamespace(is_staff=False, is_superuser=False)

    # Make sure selectors/repositories are NOT called
    monkeypatch.setattr(reviews_services.selectors, "get_review_by_pk", lambda pk: pytest.fail("selector called"))
    monkeypatch.setattr(reviews_services.repositories, "delete_review", lambda review: pytest.fail("repo called"))

    ok, err = reviews_services.delete_review_as_admin(user=user, pk=1)
    assert ok is None
    assert err == "Not allowed"


def test_delete_review_as_admin_returns_not_found(monkeypatch):
    user = SimpleNamespace(is_staff=True, is_superuser=False)

    def fake_get_review_by_pk(*, pk):
        assert pk == 999
        return None

    monkeypatch.setattr(reviews_services.selectors, "get_review_by_pk", fake_get_review_by_pk)
    monkeypatch.setattr(reviews_services.repositories, "delete_review", lambda review: pytest.fail("repo called"))

    ok, err = reviews_services.delete_review_as_admin(user=user, pk=999)
    assert ok is None
    assert err == "Not found"


def test_delete_review_as_admin_deletes_when_admin_and_exists(monkeypatch):
    user = SimpleNamespace(is_staff=False, is_superuser=True)
    fake_review = object()
    calls = {"deleted": False}

    def fake_get_review_by_pk(*, pk):
        assert pk == 5
        return fake_review

    def fake_delete_review(*, review):
        assert review is fake_review
        calls["deleted"] = True

    monkeypatch.setattr(reviews_services.selectors, "get_review_by_pk", fake_get_review_by_pk)
    monkeypatch.setattr(reviews_services.repositories, "delete_review", fake_delete_review)

    ok, err = reviews_services.delete_review_as_admin(user=user, pk=5)
    assert ok is True
    assert err is None
    assert calls["deleted"] is True
