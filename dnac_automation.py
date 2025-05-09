import os
import requests
from dotenv import load_dotenv
from utils.auth import get_dnac_token

# تحميل المتغيرات من .env
load_dotenv()

# استدعاء متغير URL من .env
DNAC_URL = os.getenv("DNAC_URL")

# دالة لعرض الـ interfaces الخاصة بكل جهازg
def get_interfaces_for_device(device_id, token):
    url = f"{DNAC_URL}/dna/intent/api/v1/interface/network-device/{device_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }

    response = requests.get(url, headers=headers, verify=False)
    interfaces = response.json()["response"]
    return interfaces

# دالة لعرض الأجهزة
def get_network_devices():
    token = get_dnac_token()
    url = f"{DNAC_URL}/dna/intent/api/v1/network-device"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }

    response = requests.get(url, headers=headers, verify=False)
    devices = response.json()["response"]

    for device in devices:
        if any(t in device.get("type", "") for t in ["Switch", "Router"]):
            hostname = device.get("hostname", "N/A")
            ip = device.get("managementIpAddress", "N/A")
            status = device.get("reachabilityStatus", "N/A")
            print(f"\n{hostname} - {ip} - {status}")

            interfaces = get_interfaces_for_device(device["id"], token)
            for intf in interfaces:
                print(f"  Interface: {intf['portName']} - {intf['status']}")

# تشغيل البرنامج
if __name__ == "__main__":
    get_network_devices()
