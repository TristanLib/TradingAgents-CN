# OpenRouter DeepSeek R1 免费模型使用指南

本指南详细介绍如何在TradingAgents-CN项目中使用OpenRouter提供的DeepSeek R1免费模型进行股票分析。

## 📋 目录

- [概述](#概述)
- [准备工作](#准备工作)
- [配置步骤](#配置步骤)
- [使用方法](#使用方法)
- [模型对比](#模型对比)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

## 🎯 概述

OpenRouter是一个统一的AI模型访问平台，提供多种免费模型包括DeepSeek R1。DeepSeek R1是一个强大的推理模型，特别适合复杂的金融分析任务。

### 主要优势

- **完全免费**: DeepSeek R1免费版无需付费
- **强推理能力**: 适合复杂的股票分析和策略制定
- **工具调用支持**: 原生支持function calling
- **Token统计**: 内置token使用量追踪
- **统一接口**: 通过OpenRouter统一API访问

### 使用限制

- **请求限制**: 每分钟20次请求
- **日限制**: 
  - 余额<$10: 每天50次请求
  - 余额≥$10: 每天1000次请求
- **上下文长度**: 32,768 tokens

## 🚀 准备工作

### 1. 注册OpenRouter账号

1. 访问 [OpenRouter官网](https://openrouter.ai/)
2. 点击"Sign Up"注册账号
3. 验证邮箱地址

### 2. 获取API Key

1. 登录后访问 [API Keys页面](https://openrouter.ai/keys)
2. 点击"Create Key"创建新的API密钥
3. 复制生成的API密钥（请妥善保存）

### 3. 设置环境变量

```bash
# Linux/macOS
export OPENROUTER_API_KEY="your_api_key_here"

# Windows
set OPENROUTER_API_KEY=your_api_key_here

# 或者在.env文件中设置
echo "OPENROUTER_API_KEY=your_api_key_here" >> .env
```

### 4. 安装项目依赖

```bash
# 安装项目
pip install -e .

# 或使用uv
uv pip install -e .
```

## ⚙️ 配置步骤

### 方法1: 使用配置文件

创建配置文件 `config/openrouter_config.py`:

```python
from tradingagents.default_config import DEFAULT_CONFIG

config = {
    **DEFAULT_CONFIG,
    "llm_provider": "openrouter",
    "deep_think_llm": "deepseek/deepseek-r1-0528:free",
    "quick_think_llm": "deepseek/deepseek-r1-0528:free",
    "backend_url": "https://openrouter.ai/api/v1",
    "max_debate_rounds": 2,
    "online_tools": True,
    "analysis_depth": 3,
}
```

### 方法2: 使用环境变量

```bash
export LLM_PROVIDER="openrouter"
export DEEP_THINK_LLM="deepseek/deepseek-r1-0528:free"
export QUICK_THINK_LLM="deepseek/deepseek-r1-0528:free"
export BACKEND_URL="https://openrouter.ai/api/v1"
```

### 方法3: Web界面配置

1. 启动Web界面: `python start_web.py`
2. 在设置页面选择"OpenRouter"作为LLM提供商
3. 选择"deepseek/deepseek-r1-0528:free"作为模型

## 🎮 使用方法

### 基础使用

```python
from examples.openrouter_deepseek_r1_config import create_openrouter_config
from tradingagents.graph.trading_graph import TradingGraph

# 创建配置
config = create_openrouter_config("deepseek_r1")

# 初始化交易图
trading_graph = TradingGraph(config)

# 准备分析状态
initial_state = {
    "stock": "000001",  # 股票代码
    "messages": [],
    "research_data": {},
    "analysis_data": {},
    "session_id": "my_analysis_session"
}

# 运行分析
result = trading_graph.graph.invoke(initial_state)
print(result["final_decision"])
```

### 使用演示脚本

```bash
# 基础分析 (默认分析000001)
python examples/openrouter_deepseek_r1_demo.py

# 分析指定股票
python examples/openrouter_deepseek_r1_demo.py 600519

# 使用不同模型预设
python examples/openrouter_deepseek_r1_demo.py 600519 mistral_small

# 查看模型对比
python examples/openrouter_deepseek_r1_demo.py --compare

# 查看帮助
python examples/openrouter_deepseek_r1_demo.py --help
```

### Web界面使用

```bash
# 启动Web界面
python start_web.py

# 访问 http://localhost:8501
# 在设置中选择OpenRouter和DeepSeek R1模型
```

## 📊 模型对比

### 可用的免费模型

| 模型 | 模型ID | 参数规模 | 上下文长度 | 特点 | 推荐用途 |
|------|--------|----------|------------|------|----------|
| **DeepSeek R1** | `deepseek/deepseek-r1-0528:free` | - | 32K | 强推理能力 | 复杂股票分析 |
| **Mistral Small 3.1** | `mistralai/mistral-small-3.1-24b-instruct:free` | 24B | 96K | 速度快，工具调用 | 快速市场分析 |
| **Llama 4 Maverick** | `meta-llama/llama-4-maverick:free` | 400B/17B激活 | 256K | 大模型推理 | 复杂策略分析 |
| **Llama 4 Scout** | `meta-llama/llama-4-scout:free` | 109B/17B激活 | 512K | 高效推理 | 实时决策分析 |

### 模型选择建议

**金融分析场景推荐:**

1. **深度研究分析**: Llama 4 Maverick
   - 复杂的多因子分析
   - 长期投资策略制定
   - 综合风险评估

2. **快速市场分析**: Mistral Small 3.1
   - 日内交易决策
   - 快速新闻解读
   - 实时市场反应

3. **平衡性能**: DeepSeek R1
   - 中期投资分析
   - 技术指标解读
   - 基本面分析

4. **混合策略**: 不同任务使用不同模型
   - 深度分析: Llama 4 Maverick
   - 快速分析: DeepSeek R1

## 🎯 最佳实践

### 1. 合理设置分析参数

```python
config = {
    "max_debate_rounds": 2,  # 免费模型可适当增加
    "max_risk_discuss_rounds": 2,
    "analysis_depth": 3,  # 中等深度，平衡质量和速度
    "online_tools": True,  # 启用在线数据获取
}
```

### 2. 优化Token使用

- **批量分析**: 一次分析多只股票
- **重用会话**: 在同一session中分析相关股票
- **精简输入**: 避免过长的提示词

### 3. 错误处理

```python
try:
    result = trading_graph.graph.invoke(initial_state)
except Exception as e:
    if "rate limit" in str(e).lower():
        print("请求频率过高，请稍后重试")
    elif "quota" in str(e).lower():
        print("达到每日配额限制")
    else:
        print(f"分析错误: {e}")
```

### 4. 监控使用量

```python
# 检查token使用统计
if hasattr(trading_graph, 'token_tracker'):
    stats = trading_graph.token_tracker.get_session_stats(session_id)
    print(f"Token使用: {stats.get('total_input_tokens', 0)} + {stats.get('total_output_tokens', 0)}")
```

## 🛠️ 故障排除

### 常见问题

#### 1. API Key错误

```
错误: 401 Unauthorized
解决: 检查OPENROUTER_API_KEY是否正确设置
```

```bash
# 验证API Key
echo $OPENROUTER_API_KEY
# 重新设置
export OPENROUTER_API_KEY="your_correct_key"
```

#### 2. 请求限制错误

```
错误: 429 Too Many Requests
解决: 降低请求频率，等待一分钟后重试
```

#### 3. 模型不可用

```
错误: Model not found
解决: 确认模型ID正确，检查模型是否仍然免费可用
```

#### 4. 导入错误

```
错误: ImportError: cannot import name 'ChatOpenRouter'
解决: 确保已正确安装项目依赖
```

```bash
pip install -e .
```

### 调试模式

启用详细日志来诊断问题:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 或在配置中设置
config["debug_mode"] = True
config["log_level"] = "DEBUG"
```

### 验证设置

运行验证脚本:

```bash
python examples/openrouter_deepseek_r1_config.py
```

## 📞 获取帮助

1. **项目文档**: 查看CLAUDE.md和其他文档文件
2. **GitHub Issues**: 在项目仓库报告问题
3. **OpenRouter文档**: https://openrouter.ai/docs
4. **模型信息**: https://openrouter.ai/deepseek/deepseek-r1-0528:free

## 🔄 更新记录

- **v1.0**: 初始版本，支持DeepSeek R1免费模型
- **v1.1**: 添加多模型支持和token统计
- **v1.2**: 增加混合模式和性能优化

---

**注意**: OpenRouter的免费模型可用性可能会发生变化，请定期检查最新的模型列表和使用限制。