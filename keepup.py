import requests

# Constants
BASE_URL = "https://core.aeza.net"
VM_URL = "https://vm.aeza.net"
AUTHORIZATION = "Bearer undefined"

# Settings
host_id = "000000"  # VMManager Machine ID
aeza_id = "000000"  # Machine ID in Aeza panel
auth_type = "login"  # Type of login: 'login' (by username and password) or 'direct' (API key directly)

# Login credentials
email = "admin@example.org"
password = "12345678"

# Direct API key
api_key = "AAAAAAAAAAAAAAAAAAAAA"

def get_auth_key():
    response = requests.post(f"{BASE_URL}/api/auth?",
                             json={"method": "credentials", "email": email, "password": password},
                             headers={"authorization": AUTHORIZATION})
    return response.json()['data']['session']

def get_vm_key(auth_key):
    response = requests.get(f"{BASE_URL}/api/services/346290/goto?",
                            headers={"authorization": f"Bearer {auth_key}"})
    return response.json()['data'].replace(f"{VM_URL}/auth/key/", "")

def authenticate_with_vm_key(vm_key):
    response = requests.post(f"{VM_URL}/auth/v3/auth_by_key",
                             headers={"cookie": f"_ym_d=1669657718; _ym_uid=1669657718468356443; ref=344585; _ym_isad=1; _ym_visorc=w; token={api_key}; ses6={vm_key}",
                             "json": {"key": vm_key}})
    return response.json()

def start_vm(real_key_vm, session_key):
    response = requests.post(f"{VM_URL}/vm/v3/host/{host_id}/start",
                             headers={"cookie": f"_ym_d=1669657718; _ym_uid=1669657718468356443; ref=344585; _ym_isad=1; _ym_visorc=w; token={real_key_vm}; ses6={session_key}",
                             "x-xsrf-token": real_key_vm})
    return response.json()

try:
    requests.get("http://1.1.1.1")  # Check the machine status
except:
    if auth_type == "login":
        auth_key = get_auth_key()
    vm_key = get_vm_key(auth_key)
    session = authenticate_with_vm_key(vm_key)
    session_key = session['session']
    real_key_vm = session['token']
    response_json = start_vm(real_key_vm, session_key)

    if 'id' in response_json:
        print("SUCCESS! The machine has been automatically started!")
    else:
        print("Error. Failed to start the virtual machine. JSON response:")
        print(response_json)
