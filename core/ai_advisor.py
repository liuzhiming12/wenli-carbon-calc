"""AI-powered emission reduction suggestions via ZhipuAI (智谱) API.

Falls back to template-based reports when API is unavailable.
Uses the same API key as the vision MCP server.
"""

import os
import json
import pandas as pd
from openai import OpenAI


# ── ZhipuAI config ─────────────────────────────────────────────────
ZHIPU_API_KEY = os.environ.get(
    'ZHIPU_API_KEY',
    '3481e6f4b8884103954f6d790865b5a1.KvVbtt5R5RBKP9R1'
)
ZHIPU_BASE_URL = 'https://open.bigmodel.cn/api/paas/v4'
AI_MODEL = 'glm-4-flash'


def _get_client() -> OpenAI | None:
    try:
        return OpenAI(api_key=ZHIPU_API_KEY, base_url=ZHIPU_BASE_URL)
    except Exception:
        return None


def _call_llm(prompt: str, system_prompt: str = "") -> str | None:
    """Call ZhipuAI LLM and return text response."""
    client = _get_client()
    if client is None:
        return None

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[AI Advisor] LLM call failed: {e}")
        return None


# ── Carbon factors (Hubei grid) ────────────────────────────────────
CARBON_INTENSITY = {
    'electricity': 0.4044,  # kgCO2/kWh
    'water': 0.28,          # kgCO2/t
    'gas': 2.17,            # kgCO2/m³
}


# ── Main function ──────────────────────────────────────────────────

def generate_emission_reduction_suggestions(analysis_results: dict) -> str:
    """Generate carbon emission reduction suggestions using ZhipuAI API.

    Falls back to template-based suggestions when API is unavailable
    or the API call fails.
    """
    summary = _prepare_analysis_summary(analysis_results)

    prompt = f"""你是一位专注于校园碳中和的专家，基于以下校园碳排放分析结果，生成具体、可行的减排建议。

{summary}

请按照以下结构生成建议：
1. 整体减排策略
2. 电力减排建议
3. 水资源减排建议
4. 燃气减排建议
5. 部门针对性建议
6. 短期和长期行动计划

建议要具体、可操作，考虑技术可行性和成本效益。

重要约束：只能使用上述数据中的数值，不得编造任何数字。"""
    system = "你是一位专注于校园碳中和的专家。回答使用中文。只使用用户提供的数据，不编造任何数字。"

    report = _call_llm(prompt, system)
    if report:
        return report

    return _generate_fallback_suggestions(analysis_results)


def _generate_fallback_suggestions(analysis_results: dict) -> str:
    """Generate template-based suggestions when API is unavailable."""
    energy_analysis = analysis_results.get("energy_type_analysis", {})
    emissions = energy_analysis.get("emissions", {})
    total = emissions.get("总排放", 0)

    tips = []

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
{'  \n'.join(f'- {t}' for t in tips) if tips else '- 数据不足以生成具体洞察，建议上传更完整的能耗数据。'}

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
*提示：配置 ZHIPU_API_KEY 环境变量后，将生成基于实际数据的个性化 AI 减排建议。*
"""
    return suggestions


def _prepare_analysis_summary(analysis_results: dict) -> str:
    """Build a data-rich summary from analysis results for the AI prompt."""
    summary_parts = []

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

    dept_data = analysis_results.get("department_comparison")
    if isinstance(dept_data, pd.DataFrame) and not dept_data.empty:
        summary_parts.append("\n## 部门碳排放分析")
        for dept in dept_data.index:
            row = dept_data.loc[dept]
            summary_parts.append(
                f"- {dept}: {row.get('总碳排放(吨)', 0):.2f} 吨"
            )

    trend_data = analysis_results.get("time_trend")
    if isinstance(trend_data, pd.DataFrame) and not trend_data.empty:
        summary_parts.append("\n## 时间趋势")
        total_all = trend_data['总碳排放(吨)'].sum()
        avg_monthly = trend_data['总碳排放(吨)'].mean()
        summary_parts.append(f"- 总排放: {total_all:.2f} 吨")
        summary_parts.append(f"- 月均排放: {avg_monthly:.2f} 吨")

    return "\n".join(summary_parts) if summary_parts else "暂无分析数据"
