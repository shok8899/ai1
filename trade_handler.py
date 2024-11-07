import os
from web3 import Web3
import market_trade_kiloex
import api_kiloex
from config import SYMBOL_TO_PRODUCT_ID, SLIPPAGE
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TradeHandler:
    def __init__(self):
        self.wallet = os.getenv('WALLET_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        self.setup_config()
    
    def setup_config(self):
        """Setup OPBNB configuration"""
        self.config = {
            'chain': 'OPBNB',
            'wallet': self.wallet,
            'private_key': self.private_key,
            'chain_id': 204,  # OPBNB chain ID
            'rpc': 'https://opbnb-mainnet-rpc.bnbchain.org',
            'margin_contract': '0x19653dc8D30E39442B9cc96cb60d755E49A2717c',
            'market_contract': '0xa02d433868C7Ad58C8A2A820d6C3FF8a15536ACc',
            'market_trigger_contract': '0xe0eE1Cb99843c6dCdeb701707DaaDf9Ea8b752f7',
            'order_book_contract': '0x43E3E6FFb2E363E64cD480Cbb7cd0CF47bc6b477',
            'vault_address': '0xA2E2F3726DF754C1848C8fd1CbeA6aAFF84FC5B2',
            'view_address': '0x796f1793599D7b6acA6A87516546DdF8E5F3aA9d',
            'usdt_contract': '0x9e5AAC1Ba1a2e6aEd6b32689DFcF62A509Ca96f3',
            'execution_fee': 7000000000000,
            'gas': 500000
        }
    
    def get_product_id(self, symbol):
        """Get product ID from symbol"""
        product_id = SYMBOL_TO_PRODUCT_ID.get(symbol.upper())
        if not product_id:
            raise ValueError(f"Unsupported symbol: {symbol}")
        return product_id
    
    def execute_trade(self, trade_data):
        """Execute market trade"""
        try:
            # Get product ID
            product_id = self.get_product_id(trade_data['symbol'])
            
            # Get current market price
            market_price = api_kiloex.index_price(product_id, 'OPBNB')
            logger.info(f"Current market price for {trade_data['symbol']}: {market_price}")
            
            # Trade parameters
            is_long = trade_data['side'].lower() == 'buy'
            leverage = float(trade_data['leverage'])
            margin = float(trade_data['margin'])
            
            # Set acceptable price with slippage
            acceptable_price = (
                market_price * (1 + SLIPPAGE) if is_long 
                else market_price * (1 - SLIPPAGE)
            )
            
            logger.info(f"Executing {'long' if is_long else 'short'} position: "
                       f"margin={margin}, leverage={leverage}, "
                       f"acceptable_price={acceptable_price}")
            
            # Execute market trade
            tx_hash = market_trade_kiloex.open_market_increase_position(
                config=self.config,
                product_id=product_id,
                margin=margin,
                leverage=leverage,
                is_long=is_long,
                acceptable_price=acceptable_price,
                referral_code=bytearray(32)
            )
            
            trade_result = {
                'tx_hash': tx_hash.hex(),
                'symbol': trade_data['symbol'],
                'side': 'LONG' if is_long else 'SHORT',
                'market_price': market_price,
                'acceptable_price': acceptable_price,
                'leverage': leverage,
                'margin': margin,
                'status': 'submitted'
            }
            
            logger.info(f"Trade submitted successfully: {trade_result}")
            return trade_result
            
        except Exception as e:
            logger.error(f"Error executing trade: {str(e)}", exc_info=True)
            raise