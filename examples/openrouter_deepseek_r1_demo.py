#!/usr/bin/env python3
"""
OpenRouter DeepSeek R1 免费模型演示

这个演示展示了如何使用OpenRouter的DeepSeek R1免费模型进行股票分析。

运行前请确保：
1. 设置了 OPENROUTER_API_KEY 环境变量
2. 安装了项目依赖: pip install -e .
"""

import os
import sys
import asyncio
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.openrouter_deepseek_r1_config import create_openrouter_config, validate_openrouter_setup
from tradingagents.graph.trading_graph import TradingGraph

async def run_deepseek_r1_analysis(stock_symbol: str = "000001", model_preset: str = "deepseek_r1"):
    """
    使用DeepSeek R1免费模型进行股票分析
    
    Args:
        stock_symbol: 股票代码 (默认: "000001" - 平安银行)
        model_preset: 模型预设 ("deepseek_r1", "mistral_small", "llama_4_maverick", "hybrid_mode")
    """
    
    print(f"🚀 开始使用OpenRouter DeepSeek R1分析股票: {stock_symbol}")
    print("=" * 60)
    
    # 验证API Key设置
    if not validate_openrouter_setup():
        return
    
    try:
        # 创建配置
        config = create_openrouter_config(model_preset)
        print(f"📊 使用模型预设: {model_preset}")
        print(f"   深度分析模型: {config['deep_think_llm']}")
        print(f"   快速分析模型: {config['quick_think_llm']}")
        
        # 初始化交易图
        print("\n🔧 初始化TradingAgents图...")
        trading_graph = TradingGraph(config)
        
        # 准备输入状态
        initial_state = {
            "messages": [],
            "stock": stock_symbol,
            "research_data": {},
            "analysis_data": {},
            "recommendation": "",
            "risk_assessment": "",
            "final_decision": "",
            "session_id": f"openrouter_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "analysis_type": "comprehensive_analysis"
        }
        
        print(f"\n📈 开始分析股票 {stock_symbol}...")
        print("⏳ 这可能需要几分钟时间，请耐心等待...")
        
        # 运行分析
        result = trading_graph.graph.invoke(initial_state)
        
        # 显示结果
        print("\n" + "="*60)
        print("📊 分析结果")
        print("="*60)
        
        if "final_decision" in result and result["final_decision"]:
            print(f"🎯 最终决策: {result['final_decision']}")
        
        if "recommendation" in result and result["recommendation"]:
            print(f"\n💡 投资建议: {result['recommendation']}")
        
        if "risk_assessment" in result and result["risk_assessment"]:
            print(f"\n⚠️ 风险评估: {result['risk_assessment']}")
        
        # 显示token使用统计
        if hasattr(trading_graph, 'token_tracker'):
            stats = trading_graph.token_tracker.get_session_stats(initial_state["session_id"])
            if stats:
                print(f"\n📊 Token使用统计:")
                print(f"   输入Token: {stats.get('total_input_tokens', 0)}")
                print(f"   输出Token: {stats.get('total_output_tokens', 0)}")
                print(f"   总成本: ${stats.get('total_cost', 0):.4f}")
        
        print("\n✅ 分析完成!")
        
    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

def demo_model_comparison():
    """演示不同免费模型的比较"""
    
    print("🔍 OpenRouter免费模型对比演示")
    print("=" * 50)
    
    models = {
        "deepseek_r1": {
            "名称": "DeepSeek R1",
            "特点": "推理能力强，适合复杂分析",
            "上下文": "32K tokens",
            "推荐用途": "深度股票分析"
        },
        "mistral_small": {
            "名称": "Mistral Small 3.1",
            "特点": "速度快，支持工具调用",
            "上下文": "96K tokens",
            "推荐用途": "快速市场分析"
        },
        "llama_4_maverick": {
            "名称": "Llama 4 Maverick",
            "特点": "大模型，推理能力极强",
            "上下文": "256K tokens",
            "推荐用途": "复杂策略分析"
        },
        "hybrid_mode": {
            "名称": "混合模式",
            "特点": "深度分析用大模型，快速分析用小模型",
            "上下文": "混合",
            "推荐用途": "平衡性能和成本"
        }
    }
    
    for preset, info in models.items():
        print(f"\n📋 {info['名称']} ({preset})")
        print(f"   特点: {info['特点']}")
        print(f"   上下文长度: {info['上下文']}")
        print(f"   推荐用途: {info['推荐用途']}")

async def main():
    """主函数"""
    
    print("🎯 OpenRouter DeepSeek R1 演示程序")
    print("=" * 50)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--compare":
            demo_model_comparison()
            return
        elif sys.argv[1] == "--help":
            print("使用方法:")
            print("  python openrouter_deepseek_r1_demo.py                    # 使用默认设置分析000001")
            print("  python openrouter_deepseek_r1_demo.py --compare          # 显示模型对比")
            print("  python openrouter_deepseek_r1_demo.py [股票代码] [模型预设]  # 自定义分析")
            print("\n可用模型预设:")
            print("  - deepseek_r1      # DeepSeek R1 (默认)")
            print("  - mistral_small    # Mistral Small 3.1")
            print("  - llama_4_maverick # Llama 4 Maverick")
            print("  - hybrid_mode      # 混合模式")
            return
    
    # 获取参数
    stock_symbol = sys.argv[1] if len(sys.argv) > 1 else "000001"
    model_preset = sys.argv[2] if len(sys.argv) > 2 else "deepseek_r1"
    
    # 运行分析
    await run_deepseek_r1_analysis(stock_symbol, model_preset)

if __name__ == "__main__":
    # 检查环境
    if not validate_openrouter_setup():
        print("\n💡 设置环境变量后重新运行:")
        print("export OPENROUTER_API_KEY='your_api_key_here'")
        print("python examples/openrouter_deepseek_r1_demo.py")
        sys.exit(1)
    
    # 运行演示
    asyncio.run(main())