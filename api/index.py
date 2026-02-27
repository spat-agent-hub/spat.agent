import os
import requests
from typing import List, Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastmcp import FastMCP
from web3 import Web3

# --- CONFIGURATION ---
# Replace with your actual $SPAT contract address on Base
SPAT_TOKEN_ADDRESS = os.getenv("SPAT_TOKEN_ADDRESS", "0xYourSpatTokenAddressHere")
BASE_RPC_URL = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
MIN_SPAT_BALANCE = 100_000  # 100k $SPAT requirement

# API Keys
NEYNAR_API_KEY = os.getenv("NEYNAR_API_KEY")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
PRIVY_APP_ID = os.getenv("PRIVY_APP_ID")
PRIVY_APP_SECRET = os.getenv("PRIVY_APP_SECRET")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))

# --- GATEKEEPER LOGIC ---
def is_active_subscriber(wallet_address: str) -> bool:
    """Checks if a wallet holds at least 100k $SPAT on Base."""
    if not w3.is_address(wallet_address):
        return False
    
    # ERC-20 Minimal ABI for balanceOf
    abi = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}]
    contract = w3.eth.contract(address=Web3.to_checksum_address(SPAT_TOKEN_ADDRESS), abi=abi)
    
    try:
        balance_wei = contract.functions.balanceOf(Web3.to_checksum_address(wallet_address)).call()
        # Assuming 18 decimals for $SPAT; adjust if different
        balance = balance_wei / 10**18
        return balance >= MIN_SPAT_BALANCE
    except Exception as e:
        print(f"Error checking balance: {e}")
        return False

# --- MCP SERVER SETUP ---
mcp = FastMCP("Spat Agent Server")

@mcp.tool()
async def autonomous_research(query: str, wallet_address: str) -> str:
    """
    Performs research across Farcaster (Neynar) and X (Twitter).
    Requires 100k $SPAT subscription.
    """
    if not is_active_subscriber(wallet_address):
        return "Access Denied: You must hold at least 100k $SPAT to use this tool."

    results = []
    
    # 1. Neynar (Farcaster) Search
    if NEYNAR_API_KEY:
        try:
            url = f"https://api.neynar.com/v2/farcaster/cast/search?q={query}"
            headers = {"accept": "application/json", "api_key": NEYNAR_API_KEY}
            response = requests.get(url, headers=headers)
            casts = response.json().get('result', {}).get('casts', [])
            results.append(f"Farcaster Highlights: {[c.get('text')[:100] for c in casts[:3]]}")
        except Exception:
            results.append("Farcaster search failed.")

    # 2. X (Twitter) Search
    if X_BEARER_TOKEN:
        try:
            url = f"https://api.twitter.com/2/tweets/search/recent?query={query}"
            headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
            response = requests.get(url, headers=headers)
            tweets = response.json().get('data', [])
            results.append(f"X Highlights: {[t.get('text')[:100] for t in tweets[:3]]}")
        except Exception:
            results.append("X search failed.")

    return "\n".join(results) if results else "No data found for this research query."

@mcp.tool()
async def execute_base_trade(token_in: str, token_out: str, amount: float, wallet_address: str) -> str:
    """
    Executes a trade on Base via Privy Server Wallets.
    Requires 100k $SPAT subscription.
    """
    if not is_active_subscriber(wallet_address):
        return "Access Denied: Trade execution requires 100k $SPAT."

    # Placeholder for Privy logic
    # You would typically initialize a Privy client and call a transaction method here
    return f"Trade simulated: Swapping {amount} {token_in} for {token_out} on Base."

# --- FASTAPI WRAPPER ---
# This creates the standard web app Vercel needs
mcp_app = mcp.streamable_http_app()

app = FastAPI(title="Spat Agent API")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>Spat Agent MCP Server</h1>
            <p>Status: <span style="color: green;">Online</span></p>
            <p>MCP Endpoint: <code>/sse</code></p>
            <hr>
            <p>To access tools, ensure you hold 100k $SPAT tokens on Base.</p>
        </body>
    </html>
    """

# Mount the MCP server's routes onto our FastAPI app
app.mount("/mcp", mcp_app)

# Vercel looks for 'app' in api/index.py
