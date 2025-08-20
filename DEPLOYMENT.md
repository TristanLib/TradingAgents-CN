# TradingAgents-CN 部署运行说明

## 快速开始

### 1. 环境要求

- **Python**: 3.10+ (推荐 3.11 或 3.12)
- **操作系统**: Windows/macOS/Linux
- **内存**: 建议 4GB+ RAM
- **网络**: 需要访问外网获取股票数据

### 2. 获取代码

```bash
git clone https://github.com/TristanLib/TradingAgents-CN.git
cd TradingAgents-CN
```

### 3. 环境设置

#### 方法一：使用venv (推荐)

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install -e .
```

#### 方法二：使用conda

```bash
conda create -n tradingagents python=3.11
conda activate tradingagents
pip install -r requirements.txt
pip install -e .
```

### 4. 配置API密钥

创建 `.env` 文件：

```bash
cp .env.example .env  # 如果有示例文件
# 或者直接创建 .env 文件
```

在 `.env` 文件中添加以下配置：

```env
# OpenRouter API (可选，免费版)
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_PROVIDER=openrouter
DEEP_THINK_LLM=deepseek/deepseek-r1-0528:free
QUICK_THINK_LLM=deepseek/deepseek-r1-0528:free

# 其他LLM提供商 (可选)
# OPENAI_API_KEY=your_openai_key
# GOOGLE_API_KEY=your_google_key
# DEEPSEEK_API_KEY=your_deepseek_key

# 数据库配置 (可选)
# MONGODB_URI=mongodb://localhost:27017/
# REDIS_URL=redis://localhost:6379

# 调试配置
DEBUG=False
LOG_LEVEL=INFO
```

### 5. 获取OpenRouter API Key (免费)

1. 访问 [OpenRouter.ai](https://openrouter.ai)
2. 注册账号
3. 进入 [Keys页面](https://openrouter.ai/keys)
4. 创建新的API Key
5. 将API Key添加到 `.env` 文件

**注意**: OpenRouter提供DeepSeek R1免费额度，无需付费即可开始使用。

## 启动方式

### Web界面 (推荐)

#### 真实数据分析界面

```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 启动真实数据Web界面
streamlit run real_data_web.py --server.port=8501
```

访问：http://localhost:8501

**特点**：
- ✅ 使用AkShare获取真实股价数据
- 📊 20+技术指标实时计算
- 🎯 个股强弱分析
- 📈 交互式图表展示

#### 项目原生Web界面

```bash
# 使用项目内置启动脚本
python start_web.py

# 或手动启动
streamlit run web/app.py --server.port=8501
```

### 命令行界面

```bash
# 基础分析
python -m cli.main

# 或使用主脚本
python main.py

# 示例配置演示
python examples/openrouter_deepseek_r1_demo.py
```

### Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d --build

# 仅启动Web服务
docker-compose up -d web

# 查看日志
docker-compose logs -f web
```

## 功能特性

### 1. 多智能体分析系统

- **市场分析师**: 技术面分析
- **基本面分析师**: 财务数据分析  
- **新闻分析师**: 新闻情感分析
- **社交媒体分析师**: 社交情感分析
- **交易决策员**: 综合决策制定

### 2. 技术指标 (20+)

**趋势指标**:
- MA (移动平均): 5, 10, 20, 60日
- EMA (指数移动平均)
- SMA (简单移动平均)

**动量指标**:
- RSI (相对强弱指标)
- MACD (指数平滑移动平均线)
- KDJ (随机指标)

**波动性指标**:
- 布林带 (Bollinger Bands)
- ATR (真实波动幅度)

**自研指标**:
- 🎯 个股强弱指标 (相对大盘表现)

### 3. 数据源

- **AkShare**: A股实时数据 (免费)
- **FinnHub**: 美股数据 (需API key)
- **Yahoo Finance**: 全球股票数据
- **Tushare**: 中国股票数据 (需Token)

### 4. 支持的LLM提供商

- **OpenRouter**: 60+免费模型 (包含DeepSeek R1)
- **DeepSeek**: 直接API调用
- **OpenAI**: GPT系列模型
- **Google AI**: Gemini系列
- **DashScope**: 阿里巴巴模型

## 使用示例

### 分析A股股票

```python
# 在Web界面中输入股票代码
股票代码: 600167  # 联美控股
分析类型: 完整分析

# 或使用命令行
python examples/openrouter_deepseek_r1_demo.py --stock_code 600167
```

### 个股强弱分析

```python
python examples/relative_strength_demo.py
```

### 自定义配置

```python
from examples.openrouter_deepseek_r1_config import get_openrouter_config

config = get_openrouter_config(
    model_preset="deepseek_r1_free",
    max_debate_rounds=3
)
```

## 故障排除

### 常见问题

1. **模块导入错误**
   ```bash
   pip install -e .
   ```

2. **AkShare连接超时**
   - 检查网络连接
   - 尝试使用VPN
   - 界面会自动使用备用数据源

3. **API Key无效**
   - 检查 `.env` 文件格式
   - 验证API Key是否正确
   - 确认API Key有余额

4. **端口被占用**
   ```bash
   # 更换端口启动
   streamlit run real_data_web.py --server.port=8502
   ```

### 性能优化

1. **启用数据库缓存**
   ```env
   MONGODB_URI=mongodb://localhost:27017/
   REDIS_URL=redis://localhost:6379
   ```

2. **调整分析深度**
   - Web界面中选择"快速分析"模式
   - 减少debate_rounds参数

3. **使用更快的模型**
   ```env
   QUICK_THINK_LLM=deepseek/deepseek-r1-0528:free
   ```

## 开发调试

### 启用调试模式

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### 查看日志

```bash
# 实时日志
tail -f logs/trading_agents.log

# 或在Web界面查看控制台输出
```

### 测试API连接

```python
python test_openrouter_config.py
```

## 贡献指南

1. Fork项目仓库
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -am 'Add new feature'`
4. 推送到分支: `git push origin feature/new-feature`
5. 创建Pull Request

## 支持与帮助

- **GitHub Issues**: [提交问题](https://github.com/TristanLib/TradingAgents-CN/issues)
- **讨论区**: [GitHub Discussions](https://github.com/TristanLib/TradingAgents-CN/discussions)
- **文档**: 查看 `docs/` 目录下的详细文档

## 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**免责声明**: 本工具仅供研究和教育目的，不构成投资建议。投资有风险，决策需谨慎。