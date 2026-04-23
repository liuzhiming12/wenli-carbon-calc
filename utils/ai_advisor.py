import requests
import json
from utils.config import QIANWEN_API_KEY

def generate_emission_reduction_suggestions(analysis_results: dict) -> str:
    """
    Generate carbon emission reduction suggestions using Qwen API.
    
    Parameters
    ----------
    analysis_results : dict
        Analysis results from analyze_carbon_emissions function
    
    Returns
    -------
    str
        Generated reduction suggestions
    """
    if not QIANWEN_API_KEY:
        return "Error: QIANWEN_API_KEY not set in environment variables"
    
    # Prepare analysis summary
    summary = _prepare_analysis_summary(analysis_results)
    
    # Prepare prompt for Qwen API
    prompt = f"""
    你是一位专注于校园碳中和的专家，基于以下校园碳排放分析结果，生成具体、可行的减排建议：
    
    {summary}
    
    请按照以下结构生成建议：
    1. 整体减排策略
    2. 电力减排建议
    3. 水资源减排建议
    4. 燃气减排建议
    5. 部门针对性建议
    6. 短期和长期行动计划
    
    建议要具体、可操作，结合齐晔教授的校园碳中和研究方向，考虑技术可行性和成本效益。
    """
    
    # Call Qwen API
    try:
        response = _call_qwen_api(prompt)
        return response
    except Exception as e:
        return f"Error generating suggestions: {str(e)}"

def _prepare_analysis_summary(analysis_results: dict) -> str:
    """
    Prepare a summary of the analysis results for the AI prompt.
    """
    summary = ""
    
    # Energy type analysis
    if analysis_results.get("energy_type_analysis"):
        energy_data = analysis_results["energy_type_analysis"]
        summary += "## 能耗类型分析\n"
        summary += f"总碳排放量: {energy_data['emissions']['总']:.2f} 吨\n"
        summary += "各能源类型碳排放：\n"
        for energy_type, emission in energy_data['emissions'].items():
            if energy_type != '总':
                percentage = energy_data['percentages'][energy_type]
                summary += f"- {energy_type}: {emission:.2f} 吨 ({percentage:.1f}%)\n"
    
    # Department analysis
    if analysis_results.get("department_comparison") and isinstance(analysis_results["department_comparison"], dict):
        summary += "\n## 部门分析\n"
        dept_data = analysis_results["department_comparison"]
        for dept, data in dept_data.items():
            summary += f"- {dept}: {data['总碳排放(吨)']:.2f} 吨 ({data['占比(%)']:.1f}%)\n"
    
    # Key metrics
    if analysis_results.get("key_metrics"):
        metrics = analysis_results["key_metrics"]
        summary += "\n## 关键指标\n"
        if "highest_emission_period" in metrics:
            period = metrics['highest_emission_period']['period']
            emission = metrics['highest_emission_period']['emission']
            summary += f"碳排放最高时期: {period} ({emission:.2f} 吨)\n"
        if "highest_emission_department" in metrics:
            dept = metrics['highest_emission_department']['department']
            emission = metrics['highest_emission_department']['emission']
            percentage = metrics['highest_emission_department']['percentage']
            summary += f"碳排放最高部门: {dept} ({emission:.2f} 吨, {percentage:.1f}%)\n"
    
    return summary

def _call_qwen_api(prompt: str) -> str:
    """
    Call Qwen API to generate suggestions.
    """
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QIANWEN_API_KEY}"
    }
    
    payload = {
        "model": "ep-20260423181345-5g2jn",  # Replace with the appropriate model
        "messages": [
            {
                "role": "system",
                "content": "你是一位专注于校园碳中和的专家，提供专业、具体、可行的减排建议。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    
    if "choices" in response_data and len(response_data["choices"]) > 0:
        return response_data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API error: {response_data.get('error', 'Unknown error')}")