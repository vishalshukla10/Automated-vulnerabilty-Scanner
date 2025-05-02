import subprocess
import sys
import os
from datetime import datetime

def run_command(cmd):
        try:
                result = subprocess.check_output(cmd, shell=True, text=True)
                return result
        except subprocess.CalledProcessError:
                return "[ERROR] Could not execute: " + cmd

def generate_html_report(target, nmap_results, nikto_results, sqlmap_results):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"report-{target.replace('.', '_')}.html"

        html = f"""
        <html>
        <head>
                <title>Vulnerability Report - {target}</title>
                <style>
                        body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
                        h1 {{ color: #c0392b; }}
                        pre {{ background: #fff; padding: 10px; border: 1px solid #ccc; overflow-x: auto; }}
                        .section {{ margin-bottom: 40px; }}
                </style>
        </head>
        <body>
                <h1>Vulnerability Report</h1>
                <p><strong>Target:</strong> {target}</p>
                <p><strong>Date:</strong> {timestamp}</p>

                <div class="section">
                        <h2>Nmap Results</h2>
                        <pre>{nmap_results}</pre>
                </div>

                <div class="section">
                        <h2>Nikto Results</h2>
                        <pre>{nikto_results}</pre>
                </div>

                <div class="section">
                        <h2>SQLMap Results</h2>
                        <pre>{sqlmap_results}</pre>
                 </div>
        </body>
        </html>
        """

        with open(filename, "w") as f:
                f.write(html)

        print(f"[+] HTML report saved to: {filename}")

def scan_target(target):
        print(f"[*] Scanning {target}...")

        # Nmap Scan
        print("[*] Running Nmap scan...")
        nmap_results = run_command(f"nmap -sV -O {target}")

        # Nikto Scan (Only if HTTP/HTTPS)
        print("[*] Running Nikto scan...")
        nikto_results = run_command(f"nikto -h http://{target}")

        # SQLMap Test
        print("[*] Running basic SQLMap test...")
        sqlmap_results = run_command(f"sqlmap -u http://{target} --batch --crawl=1 --random-agent --level=1 --risk=1")

        # Generate HTML Report
        generate_html_report(target, nmap_results, nikto_results, sqlmap_results)

# --- Main Entry ---
if __name__ == "__main__":
        if len(sys.argv) != 2:
                print("Usage: python3 scanner.py <target_ip_or_url>")
                sys.exit(1)

        target = sys.argv[1]
        scan_target(target)
                            
