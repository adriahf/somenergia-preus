```md
# Som Energia Price Fetcher

This Python script fetches indexed electricity prices from the Som Energia API, processes the data, and stores it in a CSV file. It combines the newly fetched data with the previous day's data to ensure continuity and accuracy.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Script](#running-the-script)
- [Running as a Service](#running-as-a-service)
- [Running the Script Daily at 11:55 AM](#running-the-script-daily-at-1155-am)
- [Configuration](#configuration)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
The script downloads daily indexed electricity prices for a specific tariff and geographical zone from Som Energia's API. It formats, processes, and appends the data to CSV files named by date (e.g., `prices_somenergia_2025-01-06.csv`).

---

## Features
- Fetches indexed electricity prices from Som Energia API.
- Merges new data with the previous day’s data.
- Automatically saves results in CSV format.
- Can be configured to run as a systemd service for automation.

---

## Requirements
- Python 3.6 or higher
- Required Python packages:
  - `requests`
  - `pandas`
  - `pytz`

Install the dependencies using:
```bash
pip3 install requests pandas pytz
```

---

## Installation
1. **Clone or Copy the Script:**
   ```bash
   sudo mkdir -p /opt/somenergia
   sudo cp your_script.py /opt/somenergia/
   ```

2. **Make the Script Executable:**
   ```bash
   sudo chmod +x /opt/somenergia/your_script.py
   ```

3. **Install Required Packages:**
   ```bash
   pip3 install requests pandas pytz
   ```

---

## Running the Script
Run the script manually by executing:
```bash
python3 /opt/somenergia/your_script.py
```

---

## Running as a Service
To automate execution, set up the script as a `systemd` service.

### 1. Create a Service File
```bash
sudo nano /etc/systemd/system/somenergia.service
```

### 2. Add the Following Content:
```ini
[Unit]
Description=Som Energia Price Fetcher
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/somenergia/your_script.py
WorkingDirectory=/opt/somenergia
Restart=on-failure
User=root
StandardOutput=append:/var/log/somenergia.log
StandardError=append:/var/log/somenergia_error.log

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start the Service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable somenergia.service
sudo systemctl start somenergia.service
```

---

## Running the Script Daily at 11:55 AM
To schedule the script to run every day at **11:55 AM**, set up a `systemd` timer.

### 1. Create a Timer File
```bash
sudo nano /etc/systemd/system/somenergia.timer
```

### 2. Add the Following Content:
```ini
[Unit]
Description=Timer to run Som Energia Price Fetcher daily at 11:55 AM

[Timer]
OnCalendar=*-*-* 11:55:00
Persistent=true

[Install]
WantedBy=timers.target
```

### 3. Enable and Start the Timer:
```bash
sudo systemctl daemon-reload
sudo systemctl enable somenergia.timer
sudo systemctl start somenergia.timer
```

### 4. Verify the Timer is Active:
```bash
sudo systemctl list-timers
```

### Testing the Timer:
To manually trigger the service for testing without waiting for the timer:
```bash
sudo systemctl start somenergia.service
```

---

## Configuration
- **Tariff and Geo Zone** – Modify the following lines in the script:
   ```python
   tariff = "2.0TD"  # Replace with your tariff
   geo_zone = "PENINSULA"  # Replace with your geo zone
   ```

- **File Naming** – CSV files are saved as `prices_somenergia_YYYY-MM-DD.csv`.

---

## Logging
- **Output Logs**: `/var/log/somenergia.log`
- **Error Logs**: `/var/log/somenergia_error.log`

To check logs:
```bash
sudo journalctl -u somenergia.service
```

---

## Contributing
Feel free to fork this repository and submit pull requests with improvements or additional features.

---

## License
This project is licensed under the MIT License.
```