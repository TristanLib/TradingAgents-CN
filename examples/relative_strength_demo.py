#!/usr/bin/env python3
"""
个股强弱指标演示
展示如何使用新增的"个股强弱"技术指标进行股票分析
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 导入日志模块
from tradingagents.utils.logging_manager import get_logger
logger = get_logger('default')

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


def demo_relative_strength_basic():
    """基础个股强弱指标演示"""
    
    logger.info("🚀 个股强弱指标基础演示")
    logger.info("=" * 50)
    
    # 演示不同市场的股票
    stocks_to_analyze = [
        {"symbol": "600519", "name": "贵州茅台", "market": "A股"},
        {"symbol": "000001", "name": "平安银行", "market": "A股"},
        {"symbol": "AAPL", "name": "苹果公司", "market": "美股"},
        {"symbol": "TSLA", "name": "特斯拉", "market": "美股"},
    ]
    
    try:
        from tradingagents.dataflows.relative_strength_utils import get_relative_strength_data
        
        for stock in stocks_to_analyze:
            logger.info(f"\n📊 分析 {stock['name']} ({stock['symbol']}) - {stock['market']}")
            logger.info("-" * 40)
            
            # 计算最近2个月的个股强弱
            start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            result = get_relative_strength_data(
                symbol=stock['symbol'],
                start_date=start_date,
                end_date=end_date
            )
            
            print(result)
            logger.info("-" * 40)
            
    except ImportError as e:
        logger.error(f"❌ 模块导入失败: {e}")
        logger.info("💡 请确保已正确安装所有依赖")
    except Exception as e:
        logger.error(f"❌ 演示失败: {e}")


def demo_relative_strength_custom_index():
    """自定义指数对比演示"""
    
    logger.info("\n🎯 自定义指数对比演示")
    logger.info("=" * 50)
    
    # 演示用不同指数对比
    comparisons = [
        {
            "stock": "600519",  # 贵州茅台
            "index": "000001",  # 上证指数
            "desc": "贵州茅台 vs 上证指数"
        },
        {
            "stock": "600519",  # 贵州茅台
            "index": "000300",  # 沪深300
            "desc": "贵州茅台 vs 沪深300"
        },
    ]
    
    try:
        from tradingagents.dataflows.relative_strength_utils import RelativeStrengthCalculator
        
        calculator = RelativeStrengthCalculator()
        
        for comparison in comparisons:
            logger.info(f"\n📈 {comparison['desc']}")
            logger.info("-" * 30)
            
            start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            result = calculator.calculate_relative_strength(
                symbol=comparison['stock'],
                start_date=start_date,
                end_date=end_date,
                custom_index=comparison['index']
            )
            
            if "error" not in result:
                logger.info(f"✅ 分析完成")
                logger.info(f"强弱评分: {result['analysis']['strength_score']}")
                logger.info(f"趋势判断: {result['analysis']['trend']}")
                logger.info(f"投资建议: {result['analysis']['recommendation']}")
                logger.info(f"总结: {result['analysis']['summary']}")
            else:
                logger.error(f"❌ {result['error']}")
            
            logger.info("-" * 30)
            
    except Exception as e:
        logger.error(f"❌ 自定义指数对比演示失败: {e}")


def demo_enhanced_market_analysis():
    """使用增强版市场分析师演示"""
    
    logger.info("\n🔥 增强版市场分析师演示")
    logger.info("=" * 50)
    
    # 检查API密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        logger.error("❌ 请先设置 DASHSCOPE_API_KEY 环境变量")
        logger.info("💡 在 .env 文件中添加: DASHSCOPE_API_KEY=your_api_key")
        return
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # 配置使用增强版分析师
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "dashscope"
        config["deep_think_llm"] = "qwen-plus"
        config["quick_think_llm"] = "qwen-turbo"
        config["online_tools"] = True
        
        # 测试股票
        test_stocks = ["600519", "000001", "AAPL"]
        
        for stock in test_stocks:
            logger.info(f"\n📊 使用增强版分析师分析: {stock}")
            logger.info("-" * 40)
            
            # 创建交易智能体（使用增强版分析师）
            ta = TradingAgentsGraph(
                selected_analysts=["enhanced_market"],  # 使用增强版市场分析师
                debug=True,
                config=config
            )
            
            # 执行分析
            state, decision = ta.propagate(stock, datetime.now().strftime('%Y-%m-%d'))
            
            logger.info(f"✅ 分析完成")
            logger.info(f"投资建议: {decision.get('action', 'N/A')}")
            logger.info(f"目标价格: {decision.get('target_price', 'N/A')}")
            logger.info(f"置信度: {decision.get('confidence', 'N/A')}")
            logger.info(f"风险评分: {decision.get('risk_score', 'N/A')}")
            
            break  # 只演示第一个股票，避免API调用过多
            
    except Exception as e:
        logger.error(f"❌ 增强版市场分析师演示失败: {e}")
        import traceback
        traceback.print_exc()


def demo_relative_strength_interpretation():
    """个股强弱指标解读指南"""
    
    logger.info("\n📚 个股强弱指标解读指南")
    logger.info("=" * 50)
    
    guide = """
🎯 **个股强弱指标 (Relative Strength) 详解**

📊 **计算公式:**
   个股强弱 = 股价 ÷ 指数价格
   标准化值 = (当前比率 ÷ 基期比率) × 100

📈 **指标含义:**
   ✅ 值 > 100: 个股强于大盘
   ❌ 值 < 100: 个股弱于大盘
   ➡️ 值 = 100: 个股与大盘同步

🔍 **趋势分析:**
   📈 持续上升: 个股走势强劲，相对优势明显
   📉 持续下降: 个股走势疲弱，跑输大盘
   ↔️ 横盘整理: 个股与大盘保持同步

💡 **实战应用:**
   
   1️⃣ **选股策略**
      - 寻找个股强弱值持续上升的股票
      - 关注在弱市中仍保持强势的个股
      
   2️⃣ **买入时机**
      - 个股强弱突破100并持续上升
      - 个股强弱在回调后重新向上
      
   3️⃣ **卖出信号**
      - 个股强弱持续下降跌破100
      - 个股强弱形成明显的下降趋势
      
   4️⃣ **风险控制**
      - 避免个股强弱持续走弱的股票
      - 在个股强弱出现背离时保持谨慎

🌟 **优势特点:**
   - 剔除市场整体影响，专注个股表现
   - 在震荡市中识别真正的强势股
   - 提供量化的强弱判断标准
   - 适用于不同市场环境

⚠️ **注意事项:**
   - 需要结合其他技术指标综合判断
   - 关注个股强弱的趋势而非绝对数值
   - 考虑市场风格轮动的影响
   - 配合基本面分析效果更佳
"""
    
    print(guide)


def main():
    """主演示函数"""
    
    logger.info("🎉 个股强弱指标完整演示")
    logger.info("=" * 60)
    
    # 1. 基础功能演示
    demo_relative_strength_basic()
    
    # 2. 自定义指数对比
    demo_relative_strength_custom_index()
    
    # 3. 增强版分析师演示（需要API密钥）
    demo_enhanced_market_analysis()
    
    # 4. 指标解读指南
    demo_relative_strength_interpretation()
    
    logger.info("\n" + "=" * 60)
    logger.info("🎊 演示完成！")
    logger.info("\n💡 接下来你可以:")
    logger.info("1. 修改股票代码测试其他股票")
    logger.info("2. 调整时间周期观察不同趋势")
    logger.info("3. 在Web界面中使用增强版分析师")
    logger.info("4. 结合其他技术指标进行综合分析")


if __name__ == "__main__":
    main()