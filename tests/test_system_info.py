from unittest.mock import mock_open, patch

from scripts.collect_system_info import get_memory_info


def test_memory_calculation():
    # Simulated /proc/meminfo content
    fake_memory = """
    MemTotal:       4194304 kB
    MemAvailable:   1048576 kB
    """

    with patch("builtins.open", mock_open(read_data=fake_memory)):
        result = get_memory_info()

    assert result["total_gib"] == 4.0
    assert result["available_gib"] == 1.0
    assert result["used_percentage"] == "75.0%"