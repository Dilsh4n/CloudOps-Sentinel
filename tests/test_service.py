from subprocess import CompletedProcess

from scripts import diagnose_service


def test_service_info_parsing(monkeypatch):
    fake_output = """
    LoadState=loaded
    ActiveState=active
    SubState=running
    MainPID=652
    """

    def fake_run_command(command):
        return CompletedProcess(
            args=command,
            returncode=0,
            stdout=fake_output,
            stderr=""
        )

    monkeypatch.setattr(
        diagnose_service,
        "run_command",
        fake_run_command
    )

    result = diagnose_service.get_service_info(
        "example.service"
    )

    assert result["LoadState"] == "loaded"
    assert result["ActiveState"] == "active"
    assert result["SubState"] == "running"
    assert result["MainPID"] == "652"