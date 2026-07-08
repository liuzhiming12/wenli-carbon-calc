"""AI-powered emission reduction suggestions via Qwen (DashScope) API."""

import requests
import pandas as pd
from .config import QIANWEN_API_KEY, CARBON_INTENSITY


def generate_emission_reduction_suggestions(analysis_results: dict) -> str:
    """Generate carbon emission reduction suggestions using Qwen API.

    Falls back to template-based suggestions when API key is unavailable
    or the API call fails.
    """
    if not QIANWEN_API_KEY or len(QIANWEN_API_KEY) < 10:
        return _generate_fallback_suggestions(analysis_results)

    try:
        summary = _prepare_analysis_summary(analysis_results)
        prompt = f"""
你是一位专注于校园碳中和的专家，基于以下校园碳排放分析结果，生成具体、可行的减排建议。

{summary}

请按照以下结构生成建议：
1. 整体减排策略
2. 电力减排建议
3. 水资源减排建议
4. 燃气减排建议
5. 部门针对性建议
6. 短期和长期行动计划

建议要具体、可操作，考虑技术可行性和成本效益。
"""
        response = _call_qwen_api(prompt)
        return response
    except Exception as e:
        print(f"API call failed: {e}")
        return _generate_fallback_suggestions(analysis_results)


def _generate_fallback_suggestions(analysis_results: dict) -> str:
    """Generate template-based suggestions when API is unavailable."""
    energy_analysis = analysis_results.get("energy_type_analysis", {})
    emissions = energy_analysis.get("emissions", {})
    total = emissions.get("总排放", 0)

    tips = []

    # ── Data-driven suggestions ──
    if total > 0:
        tips.append(f"校园年碳排放总量为 **{total:.2f} 吨 CO₂**，建议设定 {total * 0.1:.1f} 吨（10%）的年度减排目标。")

    elec_pct = energy_analysis.get("percentages", {}).get("电力", 0)
    if elec_pct > 50:
        tips.append(f"电力排放占总排放的 {elec_pct:.1f}%，是最大的碳排放源，建议优先推进 LED 照明改造和智能空调节能。")
    gas_pct = energy_analysis.get("percentages", {}).get("燃气", 0)
    if gas_pct > 30:
        tips.append(f"燃气排放占比 {gas_pct:.1f}%，建议优化锅炉运行效率并考虑空气源热泵替代方案。")

    suggestions = f"""
## 智能减排建议

**当前状态**：AI 服务暂时不可用，以下是基于实际数据的分析建议。

> 碳排放因子参考：电力 {CARBON_INTENSITY['electricity']} kgCO₂/kWh（湖北电网 OM 因子 2023，MEE 2025）

### 数据驱动的洞察
{chr(10).join(f'- {t}' for t in tips) if tips else '- 数据不足以生成具体洞察，建议上传更完整的能耗数据。'}

### 整体减排策略
- 建立校园能源管理体系，定期监测和分析能耗数据
- 引入绿色能源采购，逐步提高可再生能源比例

### 电力减排建议
- 推广 LED 照明改造，替换传统荧光灯，可节能 30%-50%
- 安装智能控制系统，实现人走灯灭、空调自动调节
- 鼓励使用节能设备，淘汰高能耗电器

### 水资源减排建议
- 安装节水器具，减少水龙头流量
- 修复漏水管道，定期检查维护
- 开展水资源循环利用项目

### 燃气减排建议
- 优化锅炉运行效率，定期维护保养
- 推广集中供暖，提高能源利用效率
- 考虑使用空气源热泵替代燃气供暖

---
*提示：配置 QIANWEN_API_KEY 环境变量后，将生成基于实际数据的个性化 AI 减排建议。*
"""
    return suggestions


def _prepare_analysis_summary(analysis_results: dict) -> str:
    """Build a data-rich summary from analysis results for the AI prompt."""
    summary_parts = []

    # Energy type breakdown
    energy_data = analysis_results.get("energy_type_analysis")
    if energy_data:
        summary_parts.append("## 能耗类型分析")
        emissions = energy_data.get("emissions", {})
        percentages = energy_data.get("percentages", {})
        consumption = energy_data.get("consumption", {})

        summary_parts.append(f"- 总碳排放量: {emissions.get('总排放', 'N/A')} 吨")
        summary_parts.append(
            f"- 电力: {emissions.get('电力', 0):.2f} 吨 ({percentages.get('电力', 0):.1f}%), "
            f"消耗 {consumption.get('电力(kWh)', 0):.0f} kWh"
        )
        summary_parts.append(
            f"- 水: {emissions.get('水', 0):.2f} 吨 ({percentages.get('水', 0):.1f}%), "
            f"消耗 {consumption.get('用水量', 0):.0f} 吨"
        )
        summary_parts.append(
            f"- 燃气: {emissions.get('燃气', 0):.2f} 吨 ({percentages.get('燃气', 0):.1f}%), "
            f"消耗 {consumption.get('燃气(m3)', 0):.0f} m³"
        )
        summary_parts.append(f"- 碳排放因子: 电力 {CARBON_INTENSITY['electricity']} kgCO₂/kWh (湖北电网 OM 因子 2023)")

    # Department breakdown
    dept_data = analysis_results.get("department_comparison")
    if isinstance(dept_data, pd.DataFrame) and not dept_data.empty:
        summary_parts.append("\n## 部门碳排放分析")
        for dept in dept_data.index:
            row = dept_data.loc[dept]
            summary_parts.append(
                f"- {dept}: {row.get('总碳排放(吨)', 0):.2f} 吨"
            )

    # Time trend
    trend_data = analysis_results.get("time_trend")
    if isinstance(trend_data, pd.DataFrame) and not trend_data.empty:
        summary_parts.append("\n## 时间趋势")
        total_all = trend_data['总碳排放(吨)'].sum()
        avg_monthly = trend_data['总碳排放(吨)'].mean()
        summary_parts.append(f"- 总排放: {total_all:.2f} 吨")
        summary_parts.append(f"- 月均排放: {avg_monthly:.2f} 吨")

    return "\n".join(summary_parts) if summary_parts else "暂无分析数据"


def _call_qwen_api(prompt: str) -> str:
    """Call Qwen API (DashScope) to generate suggestions."""
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QIANWEN_API_KEY}",
    }

    payload = {
        "model": "qwen-plus",
        "messages": [
            {"role": "system", "content": "你是一位专注于校园碳中和的专家。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response_data = response.json()

    if "choices" in response_data and len(response_data["choices"]) > 0:
        return response_data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API error: {response_data.get('error', response_data)}")
