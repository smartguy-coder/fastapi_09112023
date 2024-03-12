import requests
import csv
import time

def fetch_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()
    timestamp = data['timestamp']
    latitude = data['iss_position']['latitude']
    longitude = data['iss_position']['longitude']
    return timestamp, latitude, longitude

def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)

def main():
    filename = 'iss_location.csv'
    headers = ['Timestamp', 'Latitude', 'Longitude']
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)
    while True:
        timestamp, latitude, longitude = fetch_iss_location()
        data = [timestamp, latitude, longitude]
        write_to_csv(filename, data)
        print("Data recorded to CSV")
        time.sleep(5)

if __name__ == "__main__":
    main()
