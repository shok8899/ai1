# Kiloex TradingView Webhook for OPBNB

A webhook server for receiving TradingView signals and executing trades on Kiloex OPBNB.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
```
Edit the .env file with your configuration:
- WALLET_ADDRESS: Your wallet address
- PRIVATE_KEY: Your private key
- SLIPPAGE: Slippage setting (default: 0.1%)

## TradingView Configuration

1. Webhook URL in Alert settings:
```
http://your_server:5000/webhook
```

2. Alert message format (JSON):
```json
{
    "symbol": "ETHUSD",
    "side": "buy",
    "leverage": 2,
    "margin": 20
}
```

## Supported Trading Pairs

- ETHUSD (ID: 1)
- BTCUSD (ID: 2)
- BNBUSD (ID: 3)

## Running the Server

```bash
python webhook_server.py
```

## Features

- Market order trading on OPBNB
- Automatic slippage protection
- Full parameter validation
- Detailed error logging