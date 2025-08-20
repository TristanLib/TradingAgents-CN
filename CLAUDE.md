# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TradingAgents-CN is a Chinese-enhanced multi-agent trading framework based on LangGraph that uses multiple AI agents to analyze stocks and make trading decisions. This is a fork of TauricResearch/TradingAgents with comprehensive Chinese localization, A-share market support, and integration with Chinese LLM providers.

## Development Commands

### Installation and Setup
```bash
# Install project in development mode
pip install -e .

# Using uv (alternative package manager)
uv pip install -e .

# Install specific dependencies manually if needed
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the web interface (recommended)
python start_web.py

# Alternative web interface startup
python web/run_web.py
streamlit run web/app.py

# Command line interface
python -m cli.main

# Run main analysis script
python main.py
```

### Docker Deployment
```bash
# Build and start all services
docker-compose up -d --build

# Start services (without building)
docker-compose up -d

# Smart startup scripts that auto-detect if rebuild is needed
# Windows
powershell -ExecutionPolicy Bypass -File scripts\smart_start.ps1
# Linux/macOS
./scripts/smart_start.sh

# View logs
docker-compose logs -f web
```

### Testing and Validation
```bash
# Run basic tests
python tests/quick_test.py

# Test specific components
python tests/test_analysis.py
python tests/test_dashscope_integration.py

# Test OpenRouter integration
python examples/openrouter_deepseek_r1_demo.py
python examples/openrouter_deepseek_r1_demo.py --compare

# Check system status
python scripts/validation/check_system_status.py

# Validate configuration
python scripts/validation/verify_config.py

# Validate OpenRouter setup
python examples/openrouter_deepseek_r1_config.py
```

### Maintenance Commands
```bash
# Clean cache
python scripts/maintenance/cleanup_cache.py

# Check dependencies
python scripts/validation/check_dependencies.py

# Syntax validation
python scripts/quick_syntax_check.py
```

## Architecture Overview

### Core Framework
- **LangGraph**: Multi-agent orchestration framework
- **LangChain**: LLM integration and tool calling
- **Streamlit**: Web interface for user interaction
- **Python 3.10+**: Runtime environment

### Multi-Agent System
The system uses a sophisticated multi-agent architecture:

1. **Analyst Agents** (`tradingagents/agents/analysts/`):
   - `fundamentals_analyst.py`: Financial fundamentals analysis
   - `market_analyst.py`: Technical and market analysis
   - `news_analyst.py`: News sentiment and impact analysis (v0.1.12 enhanced)
   - `social_media_analyst.py`: Social media sentiment analysis

2. **Research Agents** (`tradingagents/agents/researchers/`):
   - `bull_researcher.py`: Bullish argument construction
   - `bear_researcher.py`: Bearish argument construction

3. **Management Agents** (`tradingagents/agents/managers/`):
   - `research_manager.py`: Coordinates research activities
   - `risk_manager.py`: Risk assessment and management

4. **Trading Agent** (`tradingagents/agents/trader/`):
   - `trader.py`: Final investment decision making

### LLM Provider Support (v0.1.11+)
The system supports multiple LLM providers:
- **DashScope** (Alibaba): `tradingagents/llm_adapters/dashscope_adapter.py`
- **DeepSeek**: `tradingagents/llm_adapters/deepseek_adapter.py`
- **Google AI**: Native LangChain integration
- **OpenRouter**: `tradingagents/llm_adapters/openai_compatible_base.py` (ChatOpenRouter)
  - Supports 60+ models including free models like DeepSeek R1
  - Unified API access with token tracking and function calling support
  - Free models: DeepSeek R1, Mistral Small 3.1, Llama 4 Maverick/Scout
- **OpenAI**: Standard OpenAI API

### Data Sources and Processing
Data layer (`tradingagents/dataflows/`):
- **Multi-market support**: A-shares (China), Hong Kong stocks, US stocks
- **Data providers**: Tushare, AkShare, FinnHub, Yahoo Finance
- **Caching system**: Multi-tier caching (Redis, MongoDB, local files)
- **Smart fallback**: Automatic data source switching on failures

### Graph Execution Engine
Core orchestration (`tradingagents/graph/`):
- `trading_graph.py`: Main orchestration class
- `setup.py`: Graph construction and configuration
- `propagation.py`: State propagation through agents
- `conditional_logic.py`: Decision routing logic
- `signal_processing.py`: Signal processing and filtering

## Key Configuration Files

### Environment Configuration
- `.env`: API keys and environment variables
- `tradingagents/default_config.py`: Default system configuration
- `config/database_config.py`: Database connection settings

### LLM Configuration
```python
# Example configuration for different providers
config = {
    "llm_provider": "openrouter",  # dashscope, deepseek, google, openrouter, openai
    "deep_think_llm": "deepseek/deepseek-r1-0528:free",  # For OpenRouter
    "quick_think_llm": "deepseek/deepseek-r1-0528:free",
    "max_debate_rounds": 2,
    "online_tools": True
}

# OpenRouter free models configuration examples:
openrouter_configs = {
    "deepseek_r1": {
        "deep_think_llm": "deepseek/deepseek-r1-0528:free",
        "quick_think_llm": "deepseek/deepseek-r1-0528:free"
    },
    "mistral_small": {
        "deep_think_llm": "mistralai/mistral-small-3.1-24b-instruct:free",
        "quick_think_llm": "mistralai/mistral-small-3.1-24b-instruct:free"
    },
    "llama_4": {
        "deep_think_llm": "meta-llama/llama-4-maverick:free",
        "quick_think_llm": "meta-llama/llama-4-scout:free"
    }
}
```

### Database Configuration
The system supports MongoDB and Redis for caching and persistence:
- MongoDB: Stock data, analysis results, user configurations
- Redis: Real-time caching, session management
- Fallback: Local file caching when databases unavailable

## News Analysis System (v0.1.12)

The latest version includes a sophisticated news analysis system:
- **Intelligent news filtering**: AI-powered relevance scoring
- **Multi-tier filtering**: Basic, enhanced, and integrated filtering
- **Quality assessment**: Automatic low-quality news detection
- **Unified news tool**: Integrated multi-source news retrieval

Key files:
- `tradingagents/tools/unified_news_tool.py`: Main news processing
- `tradingagents/utils/enhanced_news_filter.py`: Advanced filtering logic
- `tradingagents/utils/news_filter_integration.py`: Integration layer

## Web Interface (Streamlit)

### Main Application
- `web/app.py`: Main Streamlit application
- `web/components/`: Reusable UI components
- `web/utils/`: Utility functions for session management, progress tracking

### Key Features
- Real-time analysis progress tracking (v0.1.10+)
- Multi-LLM provider selection with persistence (v0.1.11+)
- Professional report export (Markdown, Word, PDF)
- 5-level research depth configuration
- Session state management across page refreshes

## Common Development Patterns

### Adding New Agents
1. Create agent class in appropriate `tradingagents/agents/` subdirectory
2. Implement required methods following existing agent patterns
3. Add agent to graph setup in `tradingagents/graph/setup.py`
4. Update conditional logic if needed in `tradingagents/graph/conditional_logic.py`

### Adding New Data Sources
1. Create adapter in `tradingagents/dataflows/`
2. Follow existing patterns (e.g., `tushare_utils.py`, `akshare_utils.py`)
3. Implement caching and error handling
4. Add to data source manager

### Adding New LLM Providers
1. Create adapter in `tradingagents/llm_adapters/`
2. Follow OpenAI-compatible interface pattern
3. Update `tradingagents/graph/trading_graph.py` to include new provider
4. Add configuration options to default config

## Testing Strategy

### Test Organization
- `tests/`: Main testing directory
- Integration tests: `tests/test_*_integration.py`
- Component tests: `tests/test_*.py`
- Quick validation: `tests/quick_test.py`

### Development Testing
```bash
# Quick system validation
python tests/quick_test.py

# Test specific LLM integration
python tests/test_dashscope_integration.py

# Test data sources
python tests/test_data_sources_comprehensive.py

# Test web interface
python tests/test_web_interface.py
```

## Important Notes

### Chinese Market Support
- A-share stock codes: Use 6-digit format (e.g., "000001", "600519")
- Hong Kong stocks: Use ".HK" suffix (e.g., "0700.HK")
- US stocks: Use standard symbols (e.g., "AAPL", "TSLA")

### Performance Optimization
- Enable MongoDB and Redis for better performance
- Use appropriate LLM providers based on cost/performance requirements
- Configure caching settings in `.env` file
- Monitor API usage through built-in token tracking

### Docker Deployment
- The Docker setup includes all necessary services (web app, MongoDB, Redis)
- Use volume mounts for development (`docker-compose.yml` already configured)
- Database services are automatically connected via Docker networking
- Health checks ensure proper service startup

### Logging and Debugging
- Comprehensive logging system with configurable levels
- Logs stored in `logs/` directory
- Debug mode available for detailed analysis tracing
- Real-time progress tracking in web interface

This project represents a significant enhancement of the original TradingAgents framework with comprehensive Chinese localization, multi-LLM support, advanced caching, and a production-ready web interface.