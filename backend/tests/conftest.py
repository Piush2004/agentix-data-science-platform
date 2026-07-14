import pytest
from core.api.main import app
from core.auth import get_current_user
from core.models.models import User

def mock_get_current_user():
    return User(id="test-user-id", email="test@example.com", role="admin", is_active=True)

@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides = {}
