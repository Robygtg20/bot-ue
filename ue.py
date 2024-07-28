import requests
import json
import time
import sys
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# URLs for API endpoints
login_url = "https://zejlgz.com/api/login/tg"
assets_url = "https://zejlgz.com/api/user/assets"
info_url = "https://zejlgz.com/api/scene/info"
reward_url = "https://zejlgz.com/api/scene/egg/reward"
red_get_url = "https://zejlgz.com/api/red/get"
red_reward_url = "https://zejlgz.com/api/red/reward"

# Read data from accounts.txt
with open('accounts.txt', 'r') as file:
    accounts = file.readlines()

# Read code from code.txt
with open('code.txt', 'r') as file:
    code = file.read().strip()

# Headers for API requests
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
                
                # New section: Perform red get API call
                red_get_payload = {
                    "token": token_info['token'],
                    "code": code  # Include the code from code.txt
                }
                red_get_response = requests.post(red_get_url, data=json.dumps(red_get_payload), headers=headers)
                
                # Check response status code from red get
                if red_get_response.status_code == 200:
                    red_get_response_data = red_get_response.json()
                    if red_get_response_data.get('code') == 0:
                        print(Fore.MAGENTA + "Red get berhasil")
                        print("=================================")
                        
                        # New section: Perform red reward API call
                        red_reward_payload = {
                            "token": token_info['token'],
                            "code": code
                        }
                        red_reward_response = requests.post(red_reward_url, data=json.dumps(red_reward_payload), headers=headers)
                        
                        # Check response status code from red reward
                        if red_reward_response.status_code == 200:
                            red_reward_response_data = red_reward_response.json()
                            if red_reward_response_data.get('code') == 0:
                                print(Fore.GREEN + "Red reward claim berhasil")
                                print("=================================")
                            else:
                                print(f"Red reward claim gagal! Kode kesalahan: {red_reward_response_data.get('code')}")
                        else:
                            print("Red reward claim gagal!")
                            print("Status Code:", red_reward_response.status_code)
                            print("Response:", red_reward_response.text)
                    else:
                        error_code = red_get_response_data.get('code')
                        print(f"Red get gagal! Kode kesalahan: {error_code}")
                        print("Response data:", red_get_response_data)
                        # Implement specific handling for known error codes
                        if error_code == -2:
                            print("Error -2: Specific handling for this error.")
                        # Add more error handling as needed
                else:
                    print("Red get gagal!")
                    print("Status Code:", red_get_response.status_code)
                    print("Response:", red_get_response.text)

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
