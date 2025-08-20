# 个股强弱指标 (Relative Strength) 功能指南

## 📊 功能概述

个股强弱指标是TradingAgents-CN v0.1.13新增的技术分析工具，通过计算`股价/指数`的比值来判断个股相对于大盘的强弱走势。这个指标能够帮助投资者：

- 识别真正的强势股和弱势股
- 在市场震荡中找到相对优势的个股
- 评估个股跑赢大盘的能力
- 为投资决策提供量化依据

## 🎯 算法原理

### 计算公式

```
个股强弱值 = 股价 ÷ 指数价格
标准化值 = (当前比率 ÷ 基期比率) × 100
```

### 指标含义

- **值 > 100**: 个股强于大盘，表现优于指数
- **值 < 100**: 个股弱于大盘，表现逊于指数
- **值 = 100**: 个股与大盘同步，无相对优势

### 指数选择策略

系统自动为不同市场选择合适的对比指数：

| 市场类型 | 股票代码格式 | 默认指数 | 说明 |
|---------|-------------|---------|------|
| 沪市A股 | 600xxx, 601xxx | 上证指数(000001) | 反映沪市整体走势 |
| 深市A股 | 000xxx, 002xxx | 深证成指(399001) | 反映深市整体走势 |
| 科创板 | 688xxx | 沪深300(000300) | 使用大盘指数对比 |
| 美股 | AAPL, TSLA等 | 标普500(^GSPC) | 反映美股市场走势 |
| 港股 | xxxx.HK | 恒生指数(^HSI) | 反映港股市场走势 |

## 🛠️ 使用方法

### 1. 基础使用

```python
from tradingagents.dataflows.relative_strength_utils import get_relative_strength_data

# 分析贵州茅台的个股强弱
result = get_relative_strength_data(
    symbol="600519",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
print(result)
```

### 2. 自定义指数对比

```python
from tradingagents.dataflows.relative_strength_utils import RelativeStrengthCalculator

calculator = RelativeStrengthCalculator()

# 用沪深300对比贵州茅台
result = calculator.calculate_relative_strength(
    symbol="600519",
    start_date="2024-01-01",
    end_date="2024-12-31",
    custom_index="000300"  # 沪深300指数
)
```

### 3. Web界面使用

在Web界面中选择"增强版市场分析师"：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

# 配置使用增强版分析师
config = {
    "llm_provider": "dashscope",
    "deep_think_llm": "qwen-plus",
    "online_tools": True
}

ta = TradingAgentsGraph(
    selected_analysts=["enhanced_market"],  # 使用增强版分析师
    config=config
)

# 分析股票（自动包含个股强弱分析）
state, decision = ta.propagate("600519", "2024-01-15")
```

### 4. 演示脚本

运行完整演示：

```bash
python examples/relative_strength_demo.py
```

## 📈 分析结果解读

### 典型输出示例

```markdown
📊 个股强弱分析报告

基本信息:
- 股票代码: 600519
- 对比指数: 000001 (上证指数)
- 市场类型: china
- 分析期间: 2024-01-01 至 2024-12-31
- 数据点数: 243

最新数据 (2024-12-31):
- 股票价格: 1,680.50
- 指数数值: 2,915.38
- 相对强弱比率: 0.5767
- 标准化强弱值: 112.35
- 5日均线: 111.20
- 10日均线: 109.85

变化率:
- 1日变化: +0.85%
- 5日变化: +2.10%
- 20日变化: +5.20%

分析结论:
- 强弱水平: 强于大盘 (得分: 61.8)
- 趋势判断: 温和上升 (得分: 70)
- 波动特征: 中波动 (标准差: 3.24)
- 投资建议: 个股相对表现良好，可适度关注 (综合得分: 70)

总结:
600519 相对于 000001 目前强于大盘，走势温和上升，个股相对表现良好，可适度关注
```

### 关键指标说明

#### 1. 标准化强弱值
- **105-120**: 明显强于大盘，相对优势显著
- **100-105**: 略强于大盘，温和相对优势
- **95-100**: 略弱于大盘，表现接近大盘
- **80-95**: 明显弱于大盘，跑输指数

#### 2. 趋势判断
- **强势上升**: 个股强弱值>5日线>10日线，趋势明确向上
- **温和上升**: 个股强弱值>10日线，5日线>10日线
- **横盘整理**: 个股强弱值在均线附近波动
- **弱势下降**: 个股强弱值<5日线<10日线

#### 3. 投资建议评分
- **80+分**: 强烈建议关注，相对优势明显
- **60-80分**: 适度关注，表现良好
- **40-60分**: 中性观察，无明显优势
- **40分以下**: 谨慎对待，相对表现较弱

## 💡 实战应用策略

### 1. 选股策略

```python
# 筛选强势股示例
def find_strong_stocks(stock_list):
    strong_stocks = []
    
    for stock in stock_list:
        result = get_relative_strength_data(stock)
        if "error" not in result:
            # 筛选条件：强弱值>105且趋势向上
            latest = result['latest']
            analysis = result['analysis']
            
            if (latest['rs_normalized'] > 105 and 
                analysis['trend_score'] > 70):
                strong_stocks.append({
                    'symbol': stock,
                    'strength': latest['rs_normalized'],
                    'trend': analysis['trend']
                })
    
    return strong_stocks
```

### 2. 买入时机判断

```python
def check_buy_signal(symbol):
    result = get_relative_strength_data(symbol)
    
    if "error" in result:
        return False
    
    latest = result['latest']
    changes = result['changes']
    
    # 买入信号：
    # 1. 个股强弱突破100
    # 2. 近期表现持续改善
    # 3. 5日线上穿10日线
    
    buy_signal = (
        latest['rs_normalized'] > 100 and
        changes['5_day'] > 0 and
        latest['rs_ma5'] > latest['rs_ma10']
    )
    
    return buy_signal
```

### 3. 风险控制

```python
def check_risk_signal(symbol):
    result = get_relative_strength_data(symbol)
    
    if "error" in result:
        return True  # 无法获取数据时谨慎处理
    
    latest = result['latest']
    analysis = result['analysis']
    
    # 风险信号：
    # 1. 个股强弱持续下降
    # 2. 跌破关键支撑位
    # 3. 相对表现明显转弱
    
    risk_signal = (
        latest['rs_normalized'] < 95 and
        analysis['trend_score'] < 40 and
        analysis['recommendation_score'] < 30
    )
    
    return risk_signal
```

## ⚠️ 使用注意事项

### 1. 指标局限性

- **不是独立的交易信号**: 需要结合其他技术指标和基本面分析
- **适用于趋势行情**: 在震荡市中效果更佳，单边市中作用有限
- **滞后性**: 基于历史数据计算，存在一定滞后性

### 2. 市场环境考虑

- **牛市**: 关注个股强弱值持续上升的股票
- **熊市**: 寻找个股强弱值相对抗跌的股票
- **震荡市**: 重点关注个股强弱值突破的机会

### 3. 数据质量

- 确保股票代码格式正确
- 关注数据获取的成功率
- 注意处理停牌和除权除息的影响

## 🔧 技术扩展

### 自定义指标参数

```python
# 修改移动平均线周期
class CustomRelativeStrengthCalculator(RelativeStrengthCalculator):
    def calculate_relative_strength(self, symbol, start_date, end_date, 
                                   ma_periods=[3, 7, 21]):  # 自定义均线周期
        # 自定义计算逻辑
        pass
```

### 批量分析工具

```python
def batch_relative_strength_analysis(stock_list, start_date, end_date):
    """批量分析多只股票的个股强弱"""
    results = {}
    
    for stock in stock_list:
        try:
            result = get_relative_strength_data(stock, start_date, end_date)
            results[stock] = result
        except Exception as e:
            results[stock] = {"error": str(e)}
    
    return results
```

## 📚 相关文档

- [技术分析完整指南](./technical-analysis-guide.md)
- [市场分析师使用说明](../agents/analysts.md)
- [自定义算法开发指南](../development/custom-algorithms.md)
- [API参考文档](../api/dataflows-api.md)

## 🤝 贡献和反馈

如果您有改进建议或发现问题，欢迎：

1. 提交GitHub Issue
2. 贡献代码优化
3. 分享使用心得
4. 建议新功能

让我们一起完善这个强大的技术分析工具！