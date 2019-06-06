import pytest
from Task10.app.application import LitecartApp

@pytest.fixture
def litecart(request):
    app = LitecartApp()
    request.addfinalizer(app.quit)
    return app