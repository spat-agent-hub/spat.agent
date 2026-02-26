import os
from fastmcp import FastMCP
from .utils import is_active_subscriber

mcp = FastMCP("Spat Agent Base")

def gatekeeper(user_address: str):
    """Enforces the 100k $SPAT subscription on-chain."""
    if not is_active_subscriber(user_address):
        raise Exception(f"Access Denied: Wallet {user_address} needs 100,000 $SPAT subscription.")

@mcp.tool()
def autonomous_research(user_wallet: str, topic: str) -> str:
    """Scans Farcaster/X if user is a valid 100k $SPAT subscriber."""
    gatekeeper(user_wallet)
    # Neynar/Twitter API Logic here...
    return f"Premium research results for {topic}..."

@mcp.tool()
def execute_base_trade(user_wallet: str, amount_eth: float) -> str:
    """Premium Trading Tool for subscribers."""
    gatekeeper(user_wallet)
    # Privy Transaction Logic here...
    return "Trade executed successfully on Base."

app = mcp.http_app()
