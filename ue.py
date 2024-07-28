import requests
import json
import time
import sys
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# URL API
login_url = "https://zejlgz.com/api/login/tg"
assets_url = "https://zejlgz.com/api/user/assets"
info_url = "https://zejlgz.com/api/scene/info"
reward_url = "https://zejlgz.com/api/scene/egg/reward"

# Read data from accounts.txt
with open('accounts.txt', 'r') as file:
    accounts = file.readlines()

# Headers if needed, can be added
headers = {
    "Content-Type": "application/json"
}

def check_key(data, key, default=None):
    """Utility function to safely get a key from a dictionary."""
    return data.get(key, default)

def countdown_timer(seconds):
    """Displays a countdown timer for the specified number of seconds."""
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"Menunggu {remaining} detik")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r")
    sys.stdout.flush()

# ASCII Art
ascii_art = f"""
{Fore.BLUE}
██████╗  ██████╗ ████████╗    ██╗   ██╗███████╗
██╔══██╗██╔═══██╗╚══██╔══╝    ██║   ██║██╔════╝
██████╔╝██║   ██║   ██║       ██║   ██║█████╗  
██╔══██╗██║   ██║   ██║       ██║   ██║██╔══╝  
██████╔╝╚██████╔╝   ██║       ╚██████╔╝███████╗
╚═════╝  ╚═════╝    ╚═╝        ╚═════╝ ╚══════╝ 
"""

print(ascii_art)

while True:  # Infinite loop to keep claiming
    # Iterate through each account
    for account in accounts:
        init_data = account.strip()
        
        # Payload for login
        login_payload = {
            "init_data": init_data,
            "referrer": ""
        }

        # Perform POST request to API for login
        login_response = requests.post(login_url, data=json.dumps(login_payload), headers=headers)

        # Check response status code
        if login_response.status_code == 200:
            login_response_data = login_response.json()
            if login_response_data.get('code') == 0:
                token_info = login_response_data['data']['token']
                user_info = login_response_data['data']['user']
                
                print(Fore.RED + "Berhasil Login....")
                print(f"Name: {user_info['display_name']}")
                print(f"Token: {token_info['token']}")
                print("=================================")
                
                # Payload to check assets
                assets_payload = {
                    "token": token_info['token']
                }

                # Perform POST request to API to check assets
                assets_response = requests.post(assets_url, data=json.dumps(assets_payload), headers=headers)

                # Check response status code from check assets
                if assets_response.status_code == 200:
                    assets_response_data = assets_response.json()
                    if assets_response_data.get('code') == 0:
                        assets = assets_response_data['data']
                        diamond_amount = check_key(assets, 'diamond', {}).get('amount', 'N/A')
                        ue_amount = check_key(assets, 'ue', {}).get('amount', 'N/A')
                        usdt_amount = check_key(assets, 'usdt', {}).get('amount', 'N/A')
                        print(Fore.BLUE + "Cek aset....")
                        print(f"diamond: {diamond_amount}")
                        print(f"ue: {ue_amount}")
                        print(f"usdt: {usdt_amount}")
                        print("=================================")
                    else:
                        print(f"Cek aset gagal! Kode kesalahan: {assets_response_data.get('code')}")
                else:
                    print("Cek aset gagal!")
                    print("Status Code:", assets_response.status_code)
                    print("Response:", assets_response.text)

                # Payload to check info
                info_payload = {
                    "token": token_info['token']
                }

                # Perform POST request to API to check info
                info_response = requests.post(info_url, data=json.dumps(info_payload), headers=headers)

                # Check response status code from check info
                if info_response.status_code == 200:
                    info_response_data = info_response.json()
                    if info_response_data.get('code') == 0:
                        info = info_response_data['data']
                        claim_ue = sum(int(egg['amount']) for scene in info for egg in scene['eggs'] if egg['a_type'] == 'ue')
                        claim_usdt = sum(float(egg['amount']) for scene in info for egg in scene['eggs'] if egg['a_type'] == 'usdt')
                        print(Fore.YELLOW + "Cek info....")
                        print(f"claim ue : {claim_ue}")
                        print(f"claim usdt : {claim_usdt}")
                        print("=================================")
                        
                        # Claim each egg
                        for scene in info:
                            for egg in scene['eggs']:
                                egg_uid = egg['uid']
                                reward_payload = {
                                    "token": token_info['token'],
                                    "egg_uid": egg_uid
                                }
                                reward_response = requests.post(reward_url, data=json.dumps(reward_payload), headers=headers)
                                if reward_response.status_code == 200:
                                    reward_response_data = reward_response.json()
                                    if reward_response_data.get('code') == 0:
                                        print(Fore.GREEN + f"Claim berhasil untuk egg_uid: {egg_uid}")
                                    else:
                                        print(f"Claim gagal untuk egg_uid: {egg_uid}. Kode kesalahan: {reward_response_data.get('code')}")
                                else:
                                    print(f"Claim gagal untuk egg_uid: {egg_uid}. Status Code: {reward_response.status_code}")
                                    print("Response:", reward_response.text)
                        print("Semua telah berhasil terclaim")
                        print("=================================")

                        # Perform POST request to API to check assets again after claiming
                        assets_response = requests.post(assets_url, data=json.dumps(assets_payload), headers=headers)

                        # Check response status code from check assets
                        if assets_response.status_code == 200:
                            assets_response_data = assets_response.json()
                            if assets_response_data.get('code') == 0:
                                assets = assets_response_data['data']
                                diamond_amount = check_key(assets, 'diamond', {}).get('amount', 'N/A')
                                ue_amount = check_key(assets, 'ue', {}).get('amount', 'N/A')
                                usdt_amount = check_key(assets, 'usdt', {}).get('amount', 'N/A')
                                print("Saldo telah di perbaharui")
                                print(f"diamond: {diamond_amount}")
                                print(f"ue: {ue_amount}")
                                print(f"usdt: {usdt_amount}")
                            else:
                                print(f"Cek aset gagal! Kode kesalahan: {assets_response_data.get('code')}")
                        else:
                            print("Cek aset gagal!")
                            print("Status Code:", assets_response.status_code)
                            print("Response:", assets_response.text)
                    else:
                        print(f"Cek info gagal! Kode kesalahan: {info_response_data.get('code')}")
                else:
                    print("Cek info gagal!")
                    print("Status Code:", info_response.status_code)
                    print("Response:", info_response.text)
            else:
                print(f"Login gagal! Kode kesalahan: {login_response_data.get('code')}")
        else:
            print("Login gagal!")
            print("Status Code:", login_response.status_code)
            print("Response:", login_response.text)
        print("\n\n")
    
    # Delay of 960 seconds before starting the claim process again
    print("Semua akun telah terproses, claim berikutnya")
    countdown_timer(960)
