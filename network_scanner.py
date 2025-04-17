import nmap
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import RPi.GPIO as GPIO

# LED-Konfiguration (Leuchtdiode) [[6]]
LED_PIN = 17  # GPIO 17 (BCM-Nummerierung)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# Thread-sichere Komponenten
file_lock = threading.Lock()

def scan_subnet(network):
    """Optimierte Subnetz-Scan-Funktion mit aggressiver Timings"""
    nm = nmap.PortScanner()
    
    # Schnelle Ping-Überprüfung (-sn: Kein Portscan, -T5: Maximale Geschwindigkeit) [[2]]
    nm.scan(hosts=network, arguments='-sn -T5 --min-hostgroup 100')
    
    if not nm.all_hosts():
        return f"Netzwerk {network} inaktiv\n"
    
    # Detail-Scan mit maximaler Parallelisierung [[6]]
    nm.scan(
        hosts=network,
        arguments='-sV -T5 --min-parallelism 100 --max-retries 1 --host-timeout 10s'
    )
    
    # Ergebnisverarbeitung (wie zuvor)
    # ... [Behalten Sie die vorhandene Ergebnisverarbeitung aus früheren Versionen] ...

def main():
    networks = ['10.0.0.0/24', '192.168.0.0/24', '172.16.0.0/24']
    output_file = 'scan_results.txt'
    
    try:
        with ThreadPoolExecutor(max_workers=15) as executor:  # Erhöhte Parallelität
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
        # LED aktivieren nach Abschluss [[6]]
        GPIO.output(LED_PIN, GPIO.HIGH)
        print(f"Scan abgeschlossen. Ergebnisse in {output_file} gespeichert.")
        print(f"LED an GPIO {LED_PIN} aktiviert!")

if __name__ == "__main__":
    main()
