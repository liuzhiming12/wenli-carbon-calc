import requests
import json
import pandas as pd
from .config import QIANWEN_API_KEY

def generate_emission_reduction_suggestions(analysis_results: dict) -> str:
    """
    Generate carbon emission reduction suggestions using Qwen API.
    """
    if not QIANWEN_API_KEY or QIANWEN_API_KEY.startswith('sk-'):
        if not QIANWEN_API_KEY or len(QIANWEN_API_KEY) < 10:
            return _generate_fallback_suggestions(analysis_results, "API密钥未配置")

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
        print(f"API call failed: {str(e)}")
        return _generate_fallback_suggestions(analysis_results, str(e))

def _generate_fallback_suggestions(analysis_results: dict, error_msg: str = "") -> str:
    """
    Generate fallback suggestions when API is unavailable.
    """
    energy_analysis = analysis_results.get("energy_type_analysis", {})
    emissions = energy_analysis.get("emissions", {})

    suggestions = """
    ## 智能减排建议

    **当前状态**：AI服务暂时不可用，以下是基于校园碳排放最佳实践的通用建议。

    ### 整体减排策略
    - 建立校园能源管理体系，定期监测和分析能耗数据
    - 制定年度碳减排目标，建议设定5%-10%的年度减排目标
    - 引入绿色能源采购，逐步提高可再生能源比例

    ### 电力减排建议
    - 推广LED照明改造，替换传统荧光灯，可节能30%-50%
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
    提示：当AI服务恢复后，将为您生成基于实际数据分析的个性化建议
    """
    return suggestions

def _prepare_analysis_summary(analysis_results: dict) -> str:
    """
    Prepare a summary of the analysis results for the AI prompt.
    """
    summary = ""

    if analysis_results.get("energy_type_analysis"):
        energy_data = analysis_results["energy_type_analysis"]
        summary += "## 能耗类型分析\n"
        summary += f"总碳排放量待计算\n"

    if analysis_results.get("department_comparison") is not None:
        dept_data = analysis_results["department_comparison"]
        if isinstance(dept_data, pd.DataFrame) and not dept_data.empty:
            summary += "\n## 部门分析\n"

    return summary

def _call_qwen_api(prompt: str) -> str:
    """
    Call Qwen API to generate suggestions.
    """
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QIANWEN_API_KEY}"
    }

    payload = {
        "model": "qwen-plus",
        "input": {"prompt": prompt},
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 10000,
            "top_p": 0.9
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()

    if "output" in response_data and "text" in response_data["output"]:
        return response_data["output"]["text"]
    else:
        raise Exception(f"API error: {response_data.get('error', response_data)}")