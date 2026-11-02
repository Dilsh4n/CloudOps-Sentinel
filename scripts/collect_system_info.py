import json #convert python data to and from JSON
import os #Discover logical CPU count
import platform #Read the linux kernel verison
import shutil #Read file system disk usage
import socket #Read the hostname
import subprocess #Execute linux commands
import sys #print error and return exit codes

from datetime import datetime, timezone

def get_os_name():
    with open("/etc/os-release", "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("PRETTY_NAME="):
                return line.split("=", 1)[1].strip().strip('"')
    return "Unknown Linux"

def get_memory_info():
    memroy = {}

    with open("/proc/meminfo", "r", encoding="utf-8") as file:
        for line in file:
            key, value = line.split(":",1)

            memroy[key] = int(value.strip().split()[0])/1024

    total = memroy["MemTotal"]
    available = memroy["MemAvailable"]

    used_percetage = ((total - available) / total ) * 100

    return{
        "total_gib": round(total/1024,2),
        "available_gib": round(available/1024,2),
        "used_percentage": f"{round(used_percetage,2)}%"
    }

def collect_disk_info():
    usage = shutil.disk_usage("/")

    return {
        "total_gib": round(usage.total / (1024 ** 3), 2),
        "used_gib": round(usage.used / (1024 ** 3), 2),
        "free_gib": round(usage.free / (1024 ** 3), 2),
        "used_percent": round(
            (usage.used / usage.total) * 100, 2
        )
    }

def get_network_info():
    result = subprocess.run(
        ["ip", "-j", "addr", "show"],
        capture_output=True,
        text=True,
        check=True,
        timeout=5
    )

    interface_Date = json.loads(result.stdout)

    interfaces = []

    for interface in interface_Date:
        ipv4_address = []
        ipv6_address = []

        for address in interface.get("addr_info",[]):
            if address["family"] == "inet":
                ipv4_address.append(address["local"])
            elif address["family"] == "inet6":
                ipv6_address.append(address["local"])

        interfaces.append({
            "name": interface.get("ifname"),
            "state": interface.get("operstate"),
            "mac_address": interface.get("address"),
            "ipv4_addresses": ipv4_address,
            "ipv6_ addresses": ipv6_address
        })

    return interfaces


def collect_system_info():
    return{
        "collected at": datetime.now(timezone.utc).isoformat(),
        "host": {
            "hostname": socket.gethostname(),
            "os": get_os_name(),
            "kernel": platform.release()
        },
        "cpu": {
            "logical_cpus": os.cpu_count()
        },
        "memory": get_memory_info(),
        "disk": collect_disk_info(),
        "network": get_network_info()
    }

def main():
    try:
        system_info = collect_system_info()

    except(
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        ValueError,
        KeyError
    ) as error:
        print(
            f"[ERROR] Could not collect system infomation: {error}",
            file=sys.stderr
            )
        return 1


    print(json.dumps(system_info, indent=2))
    return 0

if __name__=="__main__":
    sys.exit(main())