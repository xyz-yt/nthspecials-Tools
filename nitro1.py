import random
import string
import requests
import time
from colorama import Fore, init

init(autoreset=True)

print("nothing-nitrogenv1\n")


REAL_CHECK_INTERVAL = 0.5  
GEN_INTERVAL = 0.17   
TIMEOUT = (1.5, 2.0)       
VALID_CODES_FILE = "valid_codes.txt"  


CHARS = string.ascii_uppercase + string.digits
rate_limit_end = 0
session = requests.Session()  

def generate_code():
    return ''.join(random.choices(CHARS, k=16))

def save_valid_code(code):
    with open(VALID_CODES_FILE, "a") as f:
        f.write(f"https://discord.gift/{code}\n")
        f.write(f"Verified at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

def check_code(code):
    global rate_limit_end
    
    try:
        response = session.get(
            f"https://discord.com/api/v9/entitlements/gift-codes/{code}",
            params={
                'with_application': 'false',
                'with_subscription_plan': 'true'
            },
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}[VALID] https://discord.gift/{code}")
            save_valid_code(code)
            return True
        elif response.status_code == 429:
            rate_limit_end = time.time() + min(5, int(response.headers.get('Retry-After', 3)))
    except requests.exceptions.RequestException:
        pass
    
    print(f"{Fore.RED}[INVALID] https://discord.gift/{code}")
    return False

while True:
    current_time = time.time()
    
    if current_time < rate_limit_end:
        for _ in range(3):
            code = generate_code()
            print(f"{Fore.RED}[INVALID] https://discord.gift/{code}")
            time.sleep(GEN_INTERVAL)
        rate_limit_end = current_time  
    else:
        code = generate_code()
        if check_code(code):
            time.sleep(REAL_CHECK_INTERVAL)
        else:
            time.sleep(REAL_CHECK_INTERVAL)