import importlib
from typing import Callable, Union
import pytest


@pytest.fixture
def mock_dependencies(monkeypatch: pytest.MonkeyPatch) -> Callable:
    def _mock(exchange_rate: Union[int, float]) -> None:
        monkeypatch.setattr(
            "app.main.get_exchange_rate_prediction",
            lambda current_rate: exchange_rate)
    return _mock


@pytest.mark.parametrize(
    "current_rate, predicted_rate, expected",
    [
        (100, 106, "Buy more cryptocurrency"),
        (100, 105, "Buy more cryptocurrency"),
        (100, 95, "Do nothing"),
        (100, 94, "Sell all your cryptocurrency"),
        (100, 102, "Do nothing"),
        (100, 98, "Do nothing"),
    ],
)
def test_cryptocurrency_action(
    mock_dependencies: Callable,
    current_rate: Union[int, float],
    predicted_rate: Union[int, float],
    expected: str
) -> None:
    from app import main
    importlib.reload(main)
    mock_dependencies(predicted_rate)
    from app.main import cryptocurrency_action
    assert cryptocurrency_action(current_rate) == expected
