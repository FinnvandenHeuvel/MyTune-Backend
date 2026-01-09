from types import SimpleNamespace

from core.application.services import profile_service as profile_services


def test_get_my_reviews_calls_selectors_list_my_reviews(monkeypatch):
    user = SimpleNamespace(username="alice")
    expected = [{"id": 1}, {"id": 2}]

    def fake_list_my_reviews(*, user):
        assert user.username == "alice"
        return expected

    monkeypatch.setattr(profile_services.selectors, "list_my_reviews", fake_list_my_reviews)

    out = profile_services.get_my_reviews(user=user)
    assert out == expected
