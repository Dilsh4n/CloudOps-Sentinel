import argparse
import sys
import requests

def check_health(baseurl, timeout):
    health_url = f"{baseurl.rstrip('/')}/health"
    print(f"[INFO] Checking {health_url}")

    # send http request
    try:
        response = requests.get(health_url, timeout=timeout)

    except requests.exceptions.Timeout:
        print("[FAIL] Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("[FAIL] Cannot connect to the server")
        return False
    except requests.exceptions.RequestException as error:
        print(f"[FAIL] HTTP request failed: {error}")
        return False

    # validate the http request code
    if response.status_code != 200:
        print(f"[FAIL] HTTP Status: {response.status_code}")
        return False

    # Parse the JSON response
    try:
        data = response.json()
    except:
        print("[FAIL] Invalid JSON response")
        return False

    # validate the response data
    if not isinstance(data, dict):
        print("[FAIL] Expected a JSON object")
        return False

    if data.get("status") != "healthy":
        print("[FAIL] Application reports unhealthy status")
        return False

    print("[PASS] Application is healthy")
    print(f"[INFO] Timestamp: {data.get("timestamp")}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Cloudops Sentinel HTTP health checker")
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000",
        help="Application Base URL"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="HTTP request time in seconds"
    )

    
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be a positive value")

    if check_health(args.url, args.timeout):
        return 0

    return 1

if __name__== "__main__":
    sys.exit(main())
    