import argparse
import sys
import subprocess


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        return result
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return None


def get_service_info(service):
    result = run_command(
        ["systemctl", "show", service,"--property=LoadState,ActiveState,SubState,MainPID"]
    )

    if result is None:
        return None

    if result.returncode != 0:
        print("[ERROR] could not inspect the service", file=sys.stderr)
        return None

    service_info = {}

    for line in result.stdout.splitlines():
        if "=" in line:
            key,value = line.split("=",1)
            service_info[key] = value

    return service_info

def collect_process_info(limit):
    result = run_command([
        "ps", "-eo", "pid,command,%cpu,%mem", "--sort=%cpu"
    ])

    if result is None or result.returncode != 0:
        print("[WARN] Could not retrieve processes")
        return

    lines = result.stdout.splitlines()

    print("\n[INFO] Processes sorted by CPU usage:")

    for line in lines[:limit + 1]:
        print(line)

def show_service_logs(service, lines):
    result = run_command([
        "journalctl",
        f"--unit={service}",
        f"--lines={lines}",
        "--no-pager",
        "--output=short-iso"
    ])

    print(f"\n[INFO] Recent logs for {service}:")

    if result is None:
        print("[WARN] Could not execute journalctl")
        return

    if result.returncode != 0:
        print("[WARN] Could not read journal entries")
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
        return

    if result.stderr.strip():
        print(f"[WARN] {result.stderr.strip()}", file=sys.stderr)

    print(result.stdout.strip() or "No accessible journal entries")


def main():
    parser = argparse.ArgumentParser(
        description="CloudOps Sentinel service diagnostic tool"
    )

    parser.add_argument(
        "--service",
        default="systemd-journald.service",
        help="Systemd service to inspect"
    )

    parser.add_argument(
        "--lines",
        type=int,
        default=5,
        help="Number of recent log entries"
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of processes to display"
    )

    args = parser.parse_args()

    if args.lines < 1 or args.top < 1:
        parser.error("--lines and --top must be positive")

    print(f"[INFO] Inspecting {args.service}")

    info = get_service_info(args.service)

    if info is None:
        return 1

    print(f"Load State:   {info.get('LoadState')}")
    print(f"Active State: {info.get('ActiveState')}")
    print(f"Sub State:    {info.get('SubState')}")
    print(f"Main PID:     {info.get('MainPID')}")

    collect_process_info(args.top)
    show_service_logs(args.service, args.lines)

    if (
        info.get("LoadState") == "loaded"
        and info.get("ActiveState") == "active"
    ):
        print("\n[PASS] Service is active")
        return 0

    print("\n[FAIL] Service is not active")
    return 1


if __name__ == "__main__":
    sys.exit(main())