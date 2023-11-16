# Health Check Monitoring System

## Overview
This project implements a health check monitoring system for HTTP endpoints. It periodically tests specified endpoints and logs their availability percentage over time. The system reads endpoint configurations from a YAML file and evaluates each endpoint based on response code and latency.

## Requirements
- Python 3.12
- `requests` library
- `yaml` library

## Installation
1. Ensure Python 3.12 is installed on your system.
2. Install the required Python packages:

pip install requests pyyaml

## Configuration
Create a YAML configuration file following the schema provided in the exercise description. Place this file in a known directory.

## Usage
Run the script from the command line:
python main.py /path/to/config.yaml

