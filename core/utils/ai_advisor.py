import requests
import json
import pandas as pd
from .config import QIANWEN_API_KEY

def generate_emission_reduction_suggestions(analysis_results: dict) -> str:
    """
    Generate carbon emission reduction suggestions using Qwen API.
    """
    if not QIANWEN_API_KEY or QIANWEN_API_KEY.startswith('sk-'):
        # Check if key looks like a valid format
        if not QIANWEN_API_KEY or len(QIANWEN_API_KEY) < 10:
            return _generate_fallback_suggestions(analysis_results, "API密钥未配置")
    
    try:
        summary = _prepare_analysis_summary(analysis_results)
        
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
    total_emission = emissions.get("总", 0)
    highest_energy = ""
    
    if emissions:
        energy_types = {k: v for k, v in emissions.items() if k != '总'}
        if energy_types:
            highest_energy = max(energy_types, key=energy_types.get)
    
    suggestions = f"""
    ## 🌱 智能减排建议
    
    **当前状态**：AI服务暂时不可用（{error_msg}），以下是基于校园碳排放最佳实践的通用建议：
    
    ### 1️⃣ 整体减排策略
    - 建立校园能源管理体系，定期监测和分析能耗数据
    - 制定年度碳减排目标，建议设定5%-10%的年度减排目标
    - 引入绿色能源采购，逐步提高可再生能源比例
    - 建立碳排放核算机制，定期发布碳足迹报告
    
    ### 2️⃣ 电力减排建议
    - 推广LED照明改造，替换传统荧光灯，可节能30%-50%
    - 安装智能控制系统，实现人走灯灭、空调自动调节
    - 鼓励使用节能设备，淘汰高能耗电器
    - 优化空调运行模式，设定合理温度（夏季不低于26℃，冬季不高于20℃）
    - 推广太阳能光伏发电，利用建筑屋顶空间
    
    ### 3️⃣ 水资源减排建议
    - 安装节水器具，减少水龙头流量
    - 修复漏水管道，定期检查维护
    - 开展水资源循环利用项目
    - 建设雨水收集系统，用于绿化灌溉
    - 推广中水回用技术
    
    ### 4️⃣ 燃气减排建议
    - 优化锅炉运行效率，定期维护保养
    - 推广集中供暖，提高能源利用效率
    - 考虑使用空气源热泵替代燃气供暖
    - 优化食堂灶具使用，推广节能灶
    - 加强燃气泄漏检测，确保安全运行
    
    ### 5️⃣ 部门针对性建议
    - **行政楼**：优化办公设备使用时间，推广无纸化办公，设置节能责任人
    - **教学楼**：合理安排教室使用，避免空教室浪费，推广智慧教室系统
    - **宿舍区**：加强节能宣传，培养学生节能意识，安装智能电表
    - **图书馆**：优化照明和空调使用时间，推广智能书架和自助借还系统
    - **食堂**：优化食材采购和加工流程，减少食物浪费，推广节能厨具
    
    ### 6️⃣ 短期和长期行动计划
    - **短期（1-6个月）**：完成能源审计，识别高能耗区域，开展节能宣传周活动
    - **中期（6-12个月）**：实施重点节能改造项目，建立能源管理平台，培训能源管理人员
    - **长期（1-3年）**：建立碳中和校园目标和路线图，推广绿色建筑标准，开展碳抵消项目
    
    ### 7️⃣ 预期效益评估
    - 完成上述措施后，预计可实现15%-25%的碳排放 Reduction
    - 投资回收期预计为3-5年
    - 提升校园绿色形象，符合国家双碳战略要求
    
    ---
    💡 *提示：当AI服务恢复后，将为您生成基于实际数据分析的个性化建议*
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
        summary += f"总碳排放量: {energy_data['emissions']['总']:.2f} 吨\n"
        summary += "各能源类型碳排放：\n"
        for energy_type, emission in energy_data['emissions'].items():
            if energy_type != '总':
                percentage = energy_data['percentages'][energy_type]
                summary += f"- {energy_type}: {emission:.2f} 吨 ({percentage:.1f}%)\n"
    
    if analysis_results.get("department_comparison") is not None:
        dept_data = analysis_results["department_comparison"]
        if isinstance(dept_data, pd.DataFrame) and not dept_data.empty:
            summary += "\n## 部门分析\n"
            for dept in dept_data.index:
                emission = dept_data.loc[dept, '总碳排放(吨)']
                percentage = dept_data.loc[dept, '占比(%)']
                summary += f"- {dept}: {emission:.2f} 吨 ({percentage:.1f}%)\n"
    
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
    # 使用正确的阿里云Qwen API endpoint
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
