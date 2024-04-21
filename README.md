# Network Scanner

This is a simple Python script that performs network scans using Nmap and saves the results in a txt file.

## Requirements

- Raspberry Pi 3B+ (or similar model)
- Raspbian OS (or equivalent Linux-based operating system)
- Python 3
- `nmap` Python module


## Preparations
1. **Prepare Raspberry Pi**:
   - Flash the SD card with Raspberry Pi OS (Legacy - 64 Bit) Lite or the normal version.
   - Insert the flashed SD card into the Raspberry Pi and power it up.
   - Connect the Pi to your Ethernet.

2. **Find the IP Address of the Pi**:
   - Open your command prompt and type:
     ```
     ping raspberrypi -4
     ```
   - If you've changed the Pi's name, replace "raspberrypi" with the new name.

3. **SSH into your Raspberry Pi**:
   - Use the command line or a program like PuTTY:
     ```
     ssh pi@<IP>
     ```

## Installation

1. **Install Nmap**:
   - Ensure Nmap is installed:
     ```
     sudo apt-get update
     sudo apt-get install python3-nmap
     ```

2. **Upload the Script**:
   - Navigate to the directory containing the `network_scanner.py` script on your PC.
   - Upload the script to your Raspberry Pi:
     ```
     scp network_scanner.py pi@<PI_IP>:/home/pi
     ```

3. **Install Python dependencies**:
   - Verify and install Python 3:
     ```
     sudo apt update
     sudo apt install python3
     ```
     ```
     python3 --version
     ```

## Usage

1. **Run the Script**:
   - Execute the script in your terminal:
     ```
     python3 network_scanner.py
     ```

2. **Automated Execution with Cron**:
   - Configure the script to run at system startup:
     - Open Crontab:
       ```
       crontab -e
       ```
     - Add the following command to run the script automatically:
       ```
       @reboot sleep 60 && /usr/bin/python3 /home/pi/network_scanner.py >> /home/pi/scan_results.txt 2>&1
       ```

## Checking Cron Service

To verify the Cron service and script execution:

- `sudo systemctl status cron`: Check Cron service status.
- `cat scan_results.txt`: View the last scan results.

## Troubleshooting

- Allow 3-5 minutes after booting before connecting via SSH to access scan results.
- Check file permissions and installed dependencies if the script doesn't work.
- Review Crontab configuration for correctness and file paths.
- Larger subnets will result in longer scans; start with smaller ranges (e.g., 10.0.0.0/24).

## Customizing the Scan

- Adjust the `network_ranges` variable in the Python file to match your target range.
- Consider using specific Class ranges (A, B, C) for faster scans:
  - Class A: 10.0.0.0/8
  - Class B: 172.16.0.0/12
  - Class C: 192.168.0.0/16

 ## Version
- This is version 1 of the Network Scanner script. Updates and improvements are planned for future versions.
- Feel free to open issues or pull requests for any suggestions, bug reports, or feature requests.
