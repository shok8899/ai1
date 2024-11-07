# TradingView 警报配置指南

## 1. 创建新警报

1. 在 TradingView 图表上点击"警报"按钮
2. 点击"创建新警报"

## 2. 警报设置

### Webhook URL 设置
在警报设置的 "通知" 部分：
1. 勾选 "Webhook URL"
2. 输入你的服务器地址：
```
http://your_server:5000/webhook
```

### 消息正文设置
在 "消息" 部分，选择 "JSON 格式" 并输入：
```json
{
    "symbol": "{{ticker}}",
    "side": "{{strategy.order.action}}",
    "leverage": 2,
    "margin": 20
}
```

### 自定义头部设置
1. 展开 "Webhook 设置"
2. 点击 "添加头部"
3. 添加以下头部：
```
名称: X-Tradingview-Signature
值: {{signature}}
```

## 3. 签名验证说明

签名验证使用 HMAC SHA256 算法，确保请求来自 TradingView：

1. TradingView 会使用你设置的 WEBHOOK_SECRET 对请求内容进行签名
2. 服务器收到请求后会验证签名是否匹配
3. 只有签名正确的请求才会被处理

## 4. 变量说明

- {{ticker}}: 当前交易对符号
- {{strategy.order.action}}: 交易方向 (buy/sell)
- {{signature}}: TradingView 生成的请求签名

## 5. 支持的交易对格式

请确保使用正确的交易对格式：
- ETHUSD
- BTCUSD
- BNBUSD

## 6. 注意事项

1. 确保 WEBHOOK_SECRET 与服务器配置的一致
2. 验证交易对格式是否正确
3. 检查 leverage 和 margin 值是否合理
4. 测试时建议先使用小额交易