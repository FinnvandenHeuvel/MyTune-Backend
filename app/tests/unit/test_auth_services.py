from core.application.services import auth_service


def test_can_register_returns_true():
    assert auth_service.can_register(email="x@example.com") is True
