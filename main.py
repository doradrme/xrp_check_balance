import requests


OUTPUT_FILE = "xrp_balances.txt"
INPUT_FILE = "adress.txt"


def get_xrp_balance(address):
    url = "https://s1.ripple.com:51234/"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "method": "account_info",
        "params": [
            {
                "account": address,
                "strict": True,
                "ledger_index": "current",
                "queue": True
            }
        ]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        
        if "result" in response_data and "account_data" in response_data["result"]:
            balance = response_data["result"]["account_data"]["Balance"]
            return int(balance) / 1_000_000  # Convert drops to XRP
        else:
            error_message = response_data.get("error_message", "0")
            return f" {error_message}"

    except Exception as e:
        return f"An error occurred: {e}"

def check_balances_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            addresses = file.readlines()
        
        results = {}
        for address in addresses:
            address = address.strip()  
            if address: 
                balance = get_xrp_balance(address)
                results[address] = balance
                print(f"Address: {address}, Balance: {balance} XRP")
        
        return results
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return {}

def save_balances_to_file(balances, output_path):
    try:
        with open(output_path, 'w') as file:
            for address, balance in balances.items():
                file.write(f"{address} => {balance} XRP\n")
        print(f"\n✅ Results saved to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to save results: {e}")
balances = check_balances_from_file(INPUT_FILE)

save_balances_to_file(balances, OUTPUT_FILE)
