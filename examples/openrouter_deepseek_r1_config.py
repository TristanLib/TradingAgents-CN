#!/usr/bin/env python3
"""
OpenRouter DeepSeek R1 免费模型配置示例

这个示例展示了如何使用OpenRouter提供的DeepSeek R1免费模型来运行TradingAgents-CN。

使用前准备：
1. 注册OpenRouter账号: https://openrouter.ai/
2. 获取免费API Key: https://openrouter.ai/keys
3. 设置环境变量 OPENROUTER_API_KEY
"""

import os
from tradingagents.default_config import DEFAULT_CONFIG

# DeepSeek R1免费模型配置
OPENROUTER_DEEPSEEK_R1_CONFIG = {
    **DEFAULT_CONFIG,
    
    # LLM 提供商设置
    "llm_provider": "openrouter",
    
    # 模型配置 - 使用DeepSeek R1免费版
    "deep_think_llm": "deepseek/deepseek-r1-0528:free",  # 深度思考模型
    "quick_think_llm": "deepseek/deepseek-r1-0528:free", # 快速思考模型
    
    # OpenRouter配置
    "backend_url": "https://openrouter.ai/api/v1",
    
    # 分析配置
    "max_debate_rounds": 2,  # 可以增加辩论轮数，因为免费模型
    "max_risk_discuss_rounds": 2,
    
    # 工具设置
    "online_tools": True,  # 启用在线工具
    
    # 分析深度
    "analysis_depth": 3,  # 中等深度分析 (1-5级)
}

# 其他OpenRouter免费模型选择
ALTERNATIVE_FREE_MODELS = {
    # Mistral小型模型 - 适合快速分析
    "mistral_small": {
        "deep_think_llm": "mistralai/mistral-small-3.1-24b-instruct:free",
        "quick_think_llm": "mistralai/mistral-small-3.1-24b-instruct:free",
    },
    
    # Llama 4 Maverick - 大模型，推理能力强
    "llama_4_maverick": {
        "deep_think_llm": "meta-llama/llama-4-maverick:free",
        "quick_think_llm": "meta-llama/llama-4-scout:free",  # 快速思考用Scout
    },
    
    # 混合模式 - 深度分析用大模型，快速分析用小模型
    "hybrid_mode": {
        "deep_think_llm": "meta-llama/llama-4-maverick:free",
        "quick_think_llm": "deepseek/deepseek-r1-0528:free",
    }
}

def create_openrouter_config(model_preset="deepseek_r1"):
    """
    创建OpenRouter配置
    
    Args:
        model_preset: 模型预设 ("deepseek_r1", "mistral_small", "llama_4_maverick", "hybrid_mode")
    
    Returns:
        dict: 配置字典
    """
    
    if model_preset == "deepseek_r1":
        return OPENROUTER_DEEPSEEK_R1_CONFIG
    elif model_preset in ALTERNATIVE_FREE_MODELS:
        config = OPENROUTER_DEEPSEEK_R1_CONFIG.copy()
        config.update(ALTERNATIVE_FREE_MODELS[model_preset])
        return config
    else:
        raise ValueError(f"不支持的模型预设: {model_preset}")

def validate_openrouter_setup():
    """验证OpenRouter设置"""
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ 错误: 未找到OPENROUTER_API_KEY环境变量")
        print("请按以下步骤设置:")
        print("1. 访问 https://openrouter.ai/keys")
        print("2. 注册账号并获取API Key")
        print("3. 设置环境变量:")
        print("   export OPENROUTER_API_KEY='your_api_key_here'")
        return False
    
    print(f"✅ OpenRouter API Key已设置: {api_key[:20]}...")
    return True

if __name__ == "__main__":
    print("🚀 OpenRouter DeepSeek R1 配置示例")
    print("=" * 50)
    
    # 验证设置
    if not validate_openrouter_setup():
        exit(1)
    
    # 显示配置
    config = create_openrouter_config("deepseek_r1")
    print(f"📋 配置信息:")
    print(f"  LLM提供商: {config['llm_provider']}")
    print(f"  深度思考模型: {config['deep_think_llm']}")
    print(f"  快速思考模型: {config['quick_think_llm']}")
    print(f"  API端点: {config['backend_url']}")
    print(f"  分析深度: {config['analysis_depth']}")
    
    print("\n🎯 使用示例:")
    print("from examples.openrouter_deepseek_r1_config import create_openrouter_config")
    print("config = create_openrouter_config('deepseek_r1')")
    print("# 然后在TradingAgents中使用这个配置")
    
    print("\n💡 其他可用的免费模型预设:")
    for preset, models in ALTERNATIVE_FREE_MODELS.items():
        print(f"  - {preset}: {models['deep_think_llm']}")