import requests
import time

# SETTINGS
host_id = "000000"  # VMManager machine number (listed in the machine list, write without #)
aeza_id = "000000"  # Number of the machine in the Aeza panel (indicated in the URL, https://my.aeza.net/services/000000)
type_auth = "login"  # Login type (login - by username and password, direct - API key directly)
# login
login = "admin@example.org"  # e-mail
password = "12345678"  # password
# direct
key = "AAAAAAAAAAAAAAAAAAAAA"  # API key

# Headers for requests
headers = {}

def authenticate():
    if type_auth == "login":
        headers["authorization"] = "Bearer undefined"
        response = requests.post("https://core.aeza.net/api/auth?",
                                 json={"method": "credentials", "email": login, "password": password},
                                 headers=headers)
        key = response.json()['data']['session']
        headers["authorization"] = "Bearer " + key
    else:
        headers["X-API-Key"] = key
    return headers


def start_machine(headers):
    response = requests.get(f"https://core.aeza.net/api/services/{aeza_id}/goto?", headers=headers)
    key_vm = response.json()['data'].replace("https://vm.aeza.net/auth/key/", "")
    response = requests.post("https://vm.aeza.net/auth/v3/auth_by_key", headers=headers, json={"key": key_vm})
    session = response.json()
    session_key = session['session']
    real_key_vm = session['token']
    headers["X-API-Key"] = real_key_vm
    response = requests.post(f"https://vm.aeza.net/vm/v3/host/{host_id}/start", headers=headers)
    response_json = response.json()
    if 'id' in response_json:
        print("SUCCESS! The machine has been automatically started!")
    else:
        print("Error. Could not start the virtual machine. JSON response:")
        print(response_json)


def main():
    while True:
		headers = authenticate()
		start_machine(headers)
        time.sleep(60)  # The script will attempt to start the machine every 60 seconds

if __name__ == "__main__":
    main()
