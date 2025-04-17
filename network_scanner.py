import nmap
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import RPi.GPIO as GPIO  # GPIO-Steuerung für LED [[9]]

# == LED-Konfiguration (Leuchtdiode) ==
LED_PIN = 17  # GPIO 17 (BCM-Nummerierung) [[9]]
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # LED initial aus

# Thread-sichere Komponenten
file_lock = threading.Lock()

def scan_subnet(network):
    """Optimierte Subnetz-Scan-Funktion mit aggressiver Timings [[7]]"""
    nm = nmap.PortScanner()
    results = {"network": network, "hosts": []}
    
    # Schnelle Ping-Überprüfung (-sn: Kein Portscan, -T5: Maximale Geschwindigkeit) [[7]]
    nm.scan(hosts=network, arguments='-sn -T5 --min-hostgroup 100')
    
    if not nm.all_hosts():
        return f"Netzwerk {network} inaktiv\n"
    
    # Detail-Scan mit maximaler Parallelisierung [[7]]
    nm.scan(
        hosts=network,
        arguments='-sV -T5 --min-parallelism 100 --max-retries 1 --host-timeout 10s'
    )
    
    # Ergebnisverarbeitung
    for host in nm.all_hosts():
        host_data = {
            "host": host,
            "hostname": nm[host].hostname(),
            "state": nm[host].state(),
            "protocols": {}
        }
        
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            host_data["protocols"][proto] = {
                port: nm[host][proto][port] for port in ports
            }
        
        results["hosts"].append(host_data)
    
    return results

def save_results(output_file, scan_results):
    """Ergebnisse in Datei speichern mit Zeitstempel"""
    with file_lock:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"\n{'='*40}\nZeitstempel: {timestamp}\n"
        
        with open(output_file, 'a') as f:
            f.write(header)
            
            for result in scan_results:
                if isinstance(result, str):  # Inaktive Netzwerkmeldung
                    f.write(result)
                    continue
                
                network = result['network']
                f.write(f"Netzwerk: {network}\n")
                
                for host in result['hosts']:
                    f.write(f"    Host: {host['host']} ({host['hostname']}) - {host['state']}\n")
                    
                    for proto, ports in host['protocols'].items():
                        f.write(f"        {proto.upper()} Protokoll:\n")
                        for port, details in ports.items():
                            service_info = f" ({details['product']} {details.get('version', '')})" if details.get('product') else ""
                            f.write(f"            Port {port}: {details['state']} - {details['name']}{service_info}\n")

def main():
    networks = ['10.0.0.0/24', '192.168.0.0/24', '172.16.0.0/24']
    output_file = 'scan_results.txt'
    
    try:
        with ThreadPoolExecutor(max_workers=15) as executor:  # Maximale Parallelität [[7]]
            future_to_net = {executor.submit(scan_subnet, net): net for net in networks}
            
            results = []
            for future in as_completed(future_to_net):
                net = future_to_net[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append(f"Scan fehlgeschlagen für {net}: {str(e)}\n")
        
        save_results(output_file, results)
        
    finally:
        # LED aktivieren nach Abschluss [[9]]
        GPIO.output(LED_PIN, GPIO.HIGH)
        print(f"\nScan abgeschlossen. Ergebnisse in {output_file} gespeichert.")
        print(f"LED an GPIO {LED_PIN} aktiviert! (Verbindung: LED-Anode → GPIO17, Kathode → GND mit 330Ω Widerstand)")

if __name__ == "__main__":
    main()
