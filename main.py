import requests
import yaml
import time
import signal
from urllib.parse import urlparse
import logging

def check_endpoint(session, endpoint):
    try:
        method = endpoint.get('method', 'GET')
        headers = endpoint.get('headers', {})
        body = endpoint.get('body', '')

        if method == 'GET':
            response = session.get(endpoint['url'], headers=headers)
        elif method == 'POST':
            response = session.post(endpoint['url'], headers=headers, data=body)

        response.raise_for_status()

        latency = response.elapsed.total_seconds() * 1000  # Convert to milliseconds

        return "UP" if 200 <= response.status_code < 300 and latency < 500 else "DOWN"

    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking endpoint '{endpoint['name']}': {e}")
        return "DOWN"

def log_availability(domains):
    for domain, stats in domains.items():
        total_requests, up_requests = stats['total'], stats['up']
        availability_percentage = round(100 * (up_requests / total_requests)) if total_requests > 0 else 0
        logging.info(f"{domain} has {availability_percentage}% availability")

def load_endpoints(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main(config_file_path):
    logging.basicConfig(level=logging.INFO)

    domains = {}

    def signal_handler(signal, frame):
        log_availability(domains)
        logging.info("Program terminated.")
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    session = requests.Session()

    while True:
        endpoints = load_endpoints(config_file_path)

        for endpoint in endpoints:
            status = check_endpoint(session, endpoint)
            url_parts = urlparse(endpoint['url'])
            domain = url_parts.netloc.split(':')[0] if url_parts.netloc else url_parts.path.split('/')[0]
            
            if domain not in domains:
                domains[domain] = {'total': 0, 'up': 0}
            
            domains[domain]['total'] += 1
            if status == 'UP':
                domains[domain]['up'] += 1
            
            logging.info(f"Endpoint '{endpoint['name']}' is {status}")

        log_availability(domains)
        time.sleep(15)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logging.error("Usage: python script.py <config_file_path>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    main(config_file_path)
