import os
from web3 import Web3

# Use your Alchemy/Infura URL or a public Base RPC
w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
CONTRACT_ADDR = os.getenv("SUB_CONTRACT_ADDRESS")

# ABI for the isActive check
ABI = '[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"isActive","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'

def is_active_subscriber(address: str) -> bool:
    if not address: return False
    contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDR), abi=ABI)
    try:
        return contract.functions.isActive(Web3.to_checksum_address(address)).call()
    except Exception as e:
        print(f"RPC Error: {e}")
        return False
      
