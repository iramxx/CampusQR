import cgitb
cgitb.enable()

import os
import json
import urllib.request

def main():
    client_ip = os.environ.get('REMOTE_ADDR', '127.0.0.1')
    
    response_data = {
        'ip': client_ip,
        'lat': 53.1424,
        'lon': 8.2148,
        'city': 'Bremen (Default)',
        'error': None
    }

    if client_ip == '127.0.0.1' or client_ip.startswith('10.'):
        response_data['error'] = "Local or private IP, showing default location."
    else:
        try:
            api_url = f"https://ipinfo.io/{client_ip}/json"
            with urllib.request.urlopen(api_url) as response:
                ip_data = json.loads(response.read())
                
                if 'loc' in ip_data:
                    lat, lon = ip_data['loc'].split(',')
                    response_data['lat'] = float(lat)
                    response_data['lon'] = float(lon)
                    response_data['city'] = ip_data.get('city', 'Unknown City')
        except Exception as e:
            response_data['error'] = f"Could not retrieve location data: {e}"

    print("Content-Type: application/json\n")
    print(json.dumps(response_data))

if __name__ == "__main__":
    main()