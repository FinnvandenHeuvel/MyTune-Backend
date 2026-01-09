from core.application.services import auth_service as auth_services



def test_can_register_returns_true():
    assert auth_services.can_register(email="x@example.com") is True
