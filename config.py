import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 交易配置
SLIPPAGE = float(os.getenv('SLIPPAGE', '0.001'))  # 默认滑点：0.1%

# 产品映射
SYMBOL_TO_PRODUCT_ID = {
    'ETHUSD': 1,
    'BTCUSD': 2,
    'BNBUSD': 3,
}