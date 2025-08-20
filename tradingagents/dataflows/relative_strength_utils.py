#!/usr/bin/env python3
"""
个股强弱指标工具
实现股价相对于指数的强弱分析
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 导入日志模块
from tradingagents.utils.logging_manager import get_logger
logger = get_logger('agents')

# 导入现有数据源
from .akshare_utils import AKShareProvider
from .tushare_utils import TushareProvider
from .yfin_utils import get_YFin_data_online
from .cache_manager import get_cache


class RelativeStrengthCalculator:
    """个股强弱指标计算器"""
    
    def __init__(self):
        """初始化计算器"""
        self.cache = get_cache()
        self.akshare_provider = AKShareProvider()
        self.tushare_provider = TushareProvider()
        
        # 定义各市场对应的指数代码
        self.market_indices = {
            # A股指数
            'china': {
                'sh': '000001',      # 上证指数
                'sz': '399001',      # 深证成指
                'hs300': '000300',   # 沪深300
                'zz500': '000905'    # 中证500
            },
            # 美股指数
            'us': {
                'sp500': '^GSPC',    # 标普500
                'nasdaq': '^IXIC',   # 纳斯达克
                'dow': '^DJI'        # 道琼斯
            },
            # 港股指数
            'hk': {
                'hsi': '^HSI',       # 恒生指数
                'hscei': '^HSCE'     # 恒生中国企业指数
            }
        }
        
        logger.info("✅ 个股强弱指标计算器初始化完成")
    
    def detect_stock_market(self, symbol: str) -> Tuple[str, str]:
        """
        检测股票所属市场并选择合适的指数
        
        Args:
            symbol: 股票代码
            
        Returns:
            tuple: (市场类型, 推荐指数代码)
        """
        symbol = str(symbol).upper()
        
        # A股检测
        if symbol.isdigit() and len(symbol) == 6:
            if symbol.startswith(('000', '001', '002', '003')):
                return 'china', '399001'  # 深市用深证成指
            elif symbol.startswith(('600', '601', '603', '605')):
                return 'china', '000001'  # 沪市用上证指数
            elif symbol.startswith('688'):
                return 'china', '000688'  # 科创板用科创50（如果可用）
            else:
                return 'china', '000300'  # 默认用沪深300
        
        # 港股检测
        elif symbol.endswith('.HK') or symbol.endswith('.hk'):
            return 'hk', '^HSI'
        
        # 美股检测
        else:
            return 'us', '^GSPC'
    
    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        获取股票数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            DataFrame with columns: Date, Close
        """
        try:
            market_type, _ = self.detect_stock_market(symbol)
            
            if market_type == 'china':
                # A股数据
                if self.akshare_provider.connected:
                    logger.debug(f"📊 从AkShare获取A股数据: {symbol}")
                    df = self.akshare_provider.get_stock_daily_data(symbol, start_date, end_date)
                    if df is not None and not df.empty:
                        df = df.rename(columns={'日期': 'Date', '收盘': 'Close'})
                        df['Date'] = pd.to_datetime(df['Date'])
                        return df[['Date', 'Close']].sort_values('Date')
                
                # 备选Tushare
                if self.tushare_provider.connected:
                    logger.debug(f"📊 从Tushare获取A股数据: {symbol}")
                    df = self.tushare_provider.get_stock_daily_data(symbol, start_date, end_date)
                    if df is not None and not df.empty:
                        return df[['Date', 'Close']].sort_values('Date')
            
            else:
                # 美股/港股数据
                logger.debug(f"📊 从yfinance获取数据: {symbol}")
                from .yfin_utils import YFinProvider
                yfin_provider = YFinProvider()
                df = yfin_provider.get_stock_data(symbol, start_date, end_date)
                if df is not None and not df.empty:
                    return df[['Date', 'Close']].sort_values('Date')
            
            logger.warning(f"⚠️ 无法获取股票数据: {symbol}")
            return None
            
        except Exception as e:
            logger.error(f"❌ 获取股票数据失败 {symbol}: {e}")
            return None
    
    def get_index_data(self, index_symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        获取指数数据
        
        Args:
            index_symbol: 指数代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            DataFrame with columns: Date, Close
        """
        try:
            if index_symbol.startswith(('^', '000', '399')):
                # 指数数据
                if index_symbol.startswith(('^')):
                    # 美股/港股指数
                    from .yfin_utils import YFinProvider
                    yfin_provider = YFinProvider()
                    df = yfin_provider.get_stock_data(index_symbol, start_date, end_date)
                else:
                    # A股指数
                    if self.akshare_provider.connected:
                        df = self.akshare_provider.get_index_daily_data(index_symbol, start_date, end_date)
                        if df is not None and not df.empty:
                            df = df.rename(columns={'日期': 'Date', '收盘': 'Close'})
                            df['Date'] = pd.to_datetime(df['Date'])
                
                if df is not None and not df.empty:
                    return df[['Date', 'Close']].sort_values('Date')
            
            logger.warning(f"⚠️ 无法获取指数数据: {index_symbol}")
            return None
            
        except Exception as e:
            logger.error(f"❌ 获取指数数据失败 {index_symbol}: {e}")
            return None
    
    def calculate_relative_strength(self, symbol: str, start_date: str, end_date: str, 
                                  custom_index: str = None) -> Dict:
        """
        计算个股强弱指标
        
        Args:
            symbol: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            custom_index: 自定义指数代码（可选）
            
        Returns:
            包含相对强弱分析结果的字典
        """
        logger.info(f"🔍 计算个股强弱指标: {symbol}")
        
        try:
            # 确定使用的指数
            market_type, default_index = self.detect_stock_market(symbol)
            index_symbol = custom_index if custom_index else default_index
            
            logger.info(f"📈 股票: {symbol} ({market_type}市场)")
            logger.info(f"📊 对比指数: {index_symbol}")
            
            # 获取股票和指数数据
            stock_data = self.get_stock_data(symbol, start_date, end_date)
            index_data = self.get_index_data(index_symbol, start_date, end_date)
            
            if stock_data is None or stock_data.empty:
                return {"error": f"无法获取股票 {symbol} 的数据"}
            
            if index_data is None or index_data.empty:
                return {"error": f"无法获取指数 {index_symbol} 的数据"}
            
            # 合并数据（按日期）
            merged_data = pd.merge(stock_data, index_data, on='Date', suffixes=('_stock', '_index'))
            
            if merged_data.empty:
                return {"error": "股票和指数数据无法匹配"}
            
            # 计算相对强弱比率
            merged_data['relative_strength'] = merged_data['Close_stock'] / merged_data['Close_index']
            
            # 标准化：以第一个值为基准
            first_rs = merged_data['relative_strength'].iloc[0]
            merged_data['rs_normalized'] = (merged_data['relative_strength'] / first_rs) * 100
            
            # 计算移动平均线
            merged_data['rs_ma5'] = merged_data['rs_normalized'].rolling(window=5).mean()
            merged_data['rs_ma10'] = merged_data['rs_normalized'].rolling(window=10).mean()
            merged_data['rs_ma20'] = merged_data['rs_normalized'].rolling(window=20).mean()
            
            # 计算变化率
            merged_data['rs_change_1d'] = merged_data['rs_normalized'].pct_change() * 100
            merged_data['rs_change_5d'] = merged_data['rs_normalized'].pct_change(5) * 100
            merged_data['rs_change_20d'] = merged_data['rs_normalized'].pct_change(20) * 100
            
            # 分析结果
            latest_data = merged_data.iloc[-1]
            analysis_result = self._analyze_relative_strength(merged_data, symbol, index_symbol)
            
            # 构建返回结果
            result = {
                "symbol": symbol,
                "index": index_symbol,
                "market_type": market_type,
                "analysis_period": f"{start_date} 至 {end_date}",
                "data_points": len(merged_data),
                
                # 最新值
                "latest": {
                    "date": latest_data['Date'].strftime('%Y-%m-%d'),
                    "stock_price": round(latest_data['Close_stock'], 2),
                    "index_value": round(latest_data['Close_index'], 2),
                    "rs_ratio": round(latest_data['relative_strength'], 4),
                    "rs_normalized": round(latest_data['rs_normalized'], 2),
                    "rs_ma5": round(latest_data['rs_ma5'], 2) if not pd.isna(latest_data['rs_ma5']) else None,
                    "rs_ma10": round(latest_data['rs_ma10'], 2) if not pd.isna(latest_data['rs_ma10']) else None,
                    "rs_ma20": round(latest_data['rs_ma20'], 2) if not pd.isna(latest_data['rs_ma20']) else None,
                },
                
                # 变化率
                "changes": {
                    "1_day": round(latest_data['rs_change_1d'], 2) if not pd.isna(latest_data['rs_change_1d']) else 0,
                    "5_day": round(latest_data['rs_change_5d'], 2) if not pd.isna(latest_data['rs_change_5d']) else 0,
                    "20_day": round(latest_data['rs_change_20d'], 2) if not pd.isna(latest_data['rs_change_20d']) else 0,
                },
                
                # 分析结论
                "analysis": analysis_result,
                
                # 原始数据（最近20个交易日）
                "recent_data": merged_data[['Date', 'Close_stock', 'Close_index', 'rs_normalized', 'rs_ma5', 'rs_ma10']].tail(20).to_dict('records')
            }
            
            logger.info(f"✅ 个股强弱指标计算完成: {symbol}")
            return result
            
        except Exception as e:
            logger.error(f"❌ 计算个股强弱指标失败 {symbol}: {e}")
            return {"error": f"计算失败: {str(e)}"}
    
    def _analyze_relative_strength(self, data: pd.DataFrame, symbol: str, index_symbol: str) -> Dict:
        """
        分析相对强弱走势
        
        Args:
            data: 包含相对强弱数据的DataFrame
            symbol: 股票代码
            index_symbol: 指数代码
            
        Returns:
            分析结果字典
        """
        latest = data.iloc[-1]
        
        # 趋势判断
        rs_current = latest['rs_normalized']
        rs_ma5 = latest['rs_ma5'] if not pd.isna(latest['rs_ma5']) else rs_current
        rs_ma10 = latest['rs_ma10'] if not pd.isna(latest['rs_ma10']) else rs_current
        rs_ma20 = latest['rs_ma20'] if not pd.isna(latest['rs_ma20']) else rs_current
        
        # 强弱判断
        if rs_current > 100:
            strength_level = "强于大盘"
            strength_score = min(100, ((rs_current - 100) / 20) * 100)  # 转换为0-100分
        else:
            strength_level = "弱于大盘"
            strength_score = max(0, (rs_current / 100) * 100)
        
        # 趋势判断
        if rs_current > rs_ma5 > rs_ma10:
            trend = "强势上升"
            trend_score = 85
        elif rs_current > rs_ma10 and rs_ma5 > rs_ma10:
            trend = "温和上升"
            trend_score = 70
        elif rs_current < rs_ma5 < rs_ma10:
            trend = "弱势下降"
            trend_score = 30
        elif rs_current < rs_ma10 and rs_ma5 < rs_ma10:
            trend = "明显下降"
            trend_score = 15
        else:
            trend = "横盘整理"
            trend_score = 50
        
        # 计算波动率
        rs_std = data['rs_normalized'].tail(20).std()
        volatility = "高波动" if rs_std > 5 else "中波动" if rs_std > 2 else "低波动"
        
        # 生成建议
        if strength_score > 70 and trend_score > 70:
            recommendation = "个股表现优秀，相对强势明显，建议关注"
            recommendation_score = 85
        elif strength_score > 50 and trend_score > 60:
            recommendation = "个股相对表现良好，可适度关注"
            recommendation_score = 70
        elif strength_score < 30 or trend_score < 30:
            recommendation = "个股相对表现较弱，建议谨慎"
            recommendation_score = 25
        else:
            recommendation = "个股表现中性，建议观察"
            recommendation_score = 50
        
        return {
            "strength_level": strength_level,
            "strength_score": round(strength_score, 1),
            "trend": trend,
            "trend_score": trend_score,
            "volatility": volatility,
            "volatility_value": round(rs_std, 2),
            "recommendation": recommendation,
            "recommendation_score": recommendation_score,
            "summary": f"{symbol} 相对于 {index_symbol} 目前{strength_level}，走势{trend}，{recommendation}"
        }


def get_relative_strength_data(symbol: str, start_date: str = None, end_date: str = None, 
                              custom_index: str = None) -> str:
    """
    获取个股强弱指标数据的接口函数
    
    Args:
        symbol: 股票代码
        start_date: 开始日期，默认为30天前
        end_date: 结束日期，默认为今天
        custom_index: 自定义对比指数
        
    Returns:
        格式化的个股强弱分析报告
    """
    # 默认日期处理
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')  # 60天数据
    
    calculator = RelativeStrengthCalculator()
    result = calculator.calculate_relative_strength(symbol, start_date, end_date, custom_index)
    
    if "error" in result:
        return f"❌ 个股强弱分析失败: {result['error']}"
    
    # 格式化输出
    report = f"""
📊 **个股强弱分析报告**

**基本信息:**
- 股票代码: {result['symbol']}
- 对比指数: {result['index']}
- 市场类型: {result['market_type']}
- 分析期间: {result['analysis_period']}
- 数据点数: {result['data_points']}

**最新数据 ({result['latest']['date']}):**
- 股票价格: {result['latest']['stock_price']}
- 指数数值: {result['latest']['index_value']}
- 相对强弱比率: {result['latest']['rs_ratio']}
- 标准化强弱值: {result['latest']['rs_normalized']}
- 5日均线: {result['latest']['rs_ma5'] or 'N/A'}
- 10日均线: {result['latest']['rs_ma10'] or 'N/A'}
- 20日均线: {result['latest']['rs_ma20'] or 'N/A'}

**变化率:**
- 1日变化: {result['changes']['1_day']}%
- 5日变化: {result['changes']['5_day']}%
- 20日变化: {result['changes']['20_day']}%

**分析结论:**
- 强弱水平: {result['analysis']['strength_level']} (得分: {result['analysis']['strength_score']})
- 趋势判断: {result['analysis']['trend']} (得分: {result['analysis']['trend_score']})
- 波动特征: {result['analysis']['volatility']} (标准差: {result['analysis']['volatility_value']})
- 投资建议: {result['analysis']['recommendation']} (综合得分: {result['analysis']['recommendation_score']})

**总结:**
{result['analysis']['summary']}

**指标解读:**
- 标准化强弱值 > 100: 表示个股强于指数
- 标准化强弱值 < 100: 表示个股弱于指数
- 标准化强弱值持续上升: 表示个股相对走强
- 标准化强弱值持续下降: 表示个股相对走弱
"""
    
    return report


# 为了集成到现有工具中，提供统一接口
def get_stock_relative_strength(
    symbol: str,
    start_date: str = None,
    end_date: str = None
) -> str:
    """
    获取股票相对强弱指标 - 工具接口
    """
    return get_relative_strength_data(symbol, start_date, end_date)