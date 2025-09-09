# Port Scanner

A fast, multi-threaded port scanner written in Python. This tool allows you to scan multiple hosts and port ranges efficiently.

## Features

- 🚀 Multi-threaded scanning for improved performance
- 🎯 Scan multiple hosts simultaneously
- 🔍 Detect common services and grab banners
- 📊 Export results to JSON and CSV formats
- 🛠️ Customizable timeout and thread count
- 🐍 Pure Python with no external dependencies (except standard library)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/port-scanner.git
   cd port-scanner
   ```

2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```
usage: scanner.py [-h] -t TARGET -p PORTS [-o OUTPUT] [--timeout TIMEOUT] [--threads THREADS]

Port Scanner

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target IP(s) or hostname(s), comma-separated
  -p PORTS, --ports PORTS
                        Port range (e.g., 20-80) or specific ports (e.g., 22,80,443)
  -o OUTPUT, --output OUTPUT
                        Output base name for results (without extension)
  --timeout TIMEOUT     Connection timeout in seconds (default: 1.0)
  --threads THREADS     Number of threads (default: 100)
```

## Examples

1. Scan a single host with a port range:
   ```bash
   python port_scanner/scanner.py -t 192.168.1.1 -p 20-100
   ```

2. Scan multiple hosts with specific ports:
   ```bash
   python port_scanner/scanner.py -t google.com,github.com -p 80,443,22
   ```

3. Save results to files with a custom name:
   ```bash
   python port_scanner/scanner.py -t example.com -p 1-1024 -o scan_results
   # Creates scan_results.json and scan_results.csv
   ```

4. Use custom timeout and thread count:
   ```bash
   python port_scanner/scanner.py -t 192.168.1.1 -p 1-1000 --timeout 0.5 --threads 200
   ```

## Output

The scanner will display open ports in the console with service information when available. When using the `-o` option, it will save the results in both JSON and CSV formats with the following structure:

```json
[
  {
    "host": "example.com",
    "port": 80,
    "service": "HTTP",
    "banner": "HTTP/1.1 200 OK",
    "scan_time": "2023-04-01 12:34:56"
  }
]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is intended for educational and authorized security testing purposes only. The author is not responsible for any misuse or damage caused by this program.
