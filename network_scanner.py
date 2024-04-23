import nmap
from datetime import datetime

# Create the PortScanner object
nm = nmap.PortScanner()

# Function to scan multiple network areas and save the results to a file
def scan_networks(networks, output_file):
    results_text = ""
    for network in networks:
        results_text += f"Network: {network}\n"
        print(f"Scanning {network}...")  # Status message on the console
        nm.scan(hosts=network, arguments='-sV')

        for host in nm.all_hosts():
            results_text += f"    Host: {host}\n"
            results_text += f"        Hostname: {nm[host].hostname()}\n"
            results_text += f"        State: {nm[host].state()}\n"
            results_text += "        Protocols:\n"

            for protocol in nm[host].all_protocols():
                for port in sorted(nm[host][protocol].keys()):
                    results_text += f"            {protocol.upper()} Port: {port}\n"
                    results_text += f"                State: {nm[host][protocol][port]['state']}\n"
                    results_text += f"                Service: {nm[host][protocol][port]['name']}\n"
                    results_text += f"                Product: {nm[host][protocol][port].get('product', '')}\n"
                    results_text += f"                Version: {nm[host][protocol][port].get('version', '')}\n"

    # Prepare to save results to a file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header_text = f"Timestamp: {timestamp}\nScan Results:\n\n{results_text}"

    # Save results to a file
    with open(output_file, 'a') as f:  # Use 'a' (append) mode to append to the file
        if f.tell() != 0:  # Check if the file is not empty
            f.write("\n" * 5)  # Add five empty lines before appending new results
        f.write(header_text)
    print(f"Results appended to {output_file}")

# Network areas to scan
network_ranges = ['10.0.0.0/24','192.168.0.0/24','172.16.0.0/24']

if __name__ == "__main__":
    scan_networks(network_ranges, 'scan_results.txt')
