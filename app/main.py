import streamlit as st
import pandas as pd
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import load_campus_energy_data
from carbon_calculator import calculate_carbon_emissions
from analyzer import analyze_carbon_emissions
from visualizer import visualize_carbon_emissions
from utils.ai_advisor import generate_emission_reduction_suggestions

# Set page configuration
st.set_page_config(
    page_title="文理碳计 - 校园碳足迹计算器",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create sidebar
st.sidebar.title("🌍 文理碳计")
st.sidebar.markdown("武汉文理学院校园碳足迹计算器")
st.sidebar.divider()

# File upload section
st.sidebar.subheader("📁 数据上传")
uploaded_file = st.sidebar.file_uploader(
    "上传校园能耗数据Excel文件",
    type=["xlsx", "xls"]
)

# Analysis options
st.sidebar.subheader("🔧 分析设置")
analysis_type = st.sidebar.selectbox(
    "分析类型",
    ["全部", "时间趋势", "部门对比", "能耗类型"]
)

time_granularity = st.sidebar.selectbox(
    "时间粒度",
    ["月", "季度", "年"]
)

# Main content
st.title("🌍 文理碳计 - 校园碳足迹计算器")
st.markdown("## 武汉文理学院校园能耗与碳排放分析工具")

# If file is uploaded
if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_data.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Load and clean data
        st.info("正在加载和清洗数据...")
        df = load_campus_energy_data("temp_data.xlsx")
        
        # Calculate carbon emissions
        st.info("正在计算碳排放...")
        df_with_carbon = calculate_carbon_emissions(df)
        
        # Analyze data
        st.info("正在分析数据...")
        analysis_map = {
            "全部": "all",
            "时间趋势": "time",
            "部门对比": "department",
            "能耗类型": "energy"
        }
        time_map = {
            "月": "month",
            "季度": "quarter",
            "年": "year"
        }
        
        analysis_results = analyze_carbon_emissions(
            df_with_carbon,
            analysis_type=analysis_map[analysis_type],
            time_granularity=time_map[time_granularity]
        )
        
        # Generate visualizations
        st.info("正在生成可视化图表...")
        charts = visualize_carbon_emissions(analysis_results, chart_type="all")
        
        # Display results
        st.success("分析完成！")
        
        # Data preview
        st.subheader("📊 数据预览")
        st.dataframe(df_with_carbon.head(), use_container_width=True)
        
        # Key metrics
        st.subheader("📈 关键指标")
        if analysis_results.get("key_metrics"):
            metrics = analysis_results["key_metrics"]
            col1, col2 = st.columns(2)
            
            if "highest_emission_period" in metrics:
                col1.metric(
                    "碳排放最高时期",
                    f"{metrics['highest_emission_period']['period'].strftime('%Y-%m')}",
                    f"{metrics['highest_emission_period']['emission']:.2f} 吨"
                )
            
            if "highest_emission_department" in metrics:
                col2.metric(
                    "碳排放最高部门",
                    metrics['highest_emission_department']['department'],
                    f"{metrics['highest_emission_department']['emission']:.2f} 吨 ({metrics['highest_emission_department']['percentage']:.1f}%)"
                )
        
        # Energy type analysis
        st.subheader("⚡ 能耗类型分析")
        if analysis_results.get("energy_type_analysis"):
            energy_data = analysis_results["energy_type_analysis"]
            
            # Create energy type dataframe for display
            energy_df = pd.DataFrame({
                "能源类型": ["电力", "水", "燃气"],
                "碳排放量(吨)": [
                    energy_data['emissions']['电力'],
                    energy_data['emissions']['水'],
                    energy_data['emissions']['燃气']
                ],
                "占比(%)": [
                    energy_data['percentages']['电力'],
                    energy_data['percentages']['水'],
                    energy_data['percentages']['燃气']
                ],
                "能耗量": [
                    f"{energy_data['consumption']['电力(kWh)']:.0f} kWh",
                    f"{energy_data['consumption']['水(吨)']:.0f} 吨",
                    f"{energy_data['consumption']['燃气(m3)']:.0f} m3"
                ]
            })
            
            st.dataframe(energy_df, use_container_width=True)
        
        # Visualizations
        st.subheader("📈 数据可视化")
        
        # Time trend chart
        if charts.get("trend_chart"):
            st.markdown("### 碳排放时间趋势")
            st.plotly_chart(charts["trend_chart"], use_container_width=True)
        
        # Department chart
        if charts.get("department_chart"):
            st.markdown("### 部门碳排放占比")
            st.plotly_chart(charts["department_chart"], use_container_width=True)
        
        # Energy chart
        if charts.get("energy_chart"):
            st.markdown("### 能源类型分析")
            st.plotly_chart(charts["energy_chart"], use_container_width=True)
        
        # Sankey chart
        if charts.get("sankey_chart"):
            st.markdown("### 碳流动桑基图")
            st.plotly_chart(charts["sankey_chart"], use_container_width=True)
        
        # AI emission reduction suggestions
        st.subheader("🤖 AI 减排建议")
        try:
            st.info("正在生成减排建议...")
            suggestions = generate_emission_reduction_suggestions(analysis_results)
            st.markdown(suggestions)
        except Exception as e:
            st.warning(f"生成减排建议时出现错误: {str(e)}")
        
        # Clean up temporary file
        os.remove("temp_data.xlsx")
        
    except Exception as e:
        st.error(f"分析过程中出现错误: {str(e)}")
        # Clean up temporary file if it exists
        if os.path.exists("temp_data.xlsx"):
            os.remove("temp_data.xlsx")
else:
    # Welcome screen
    st.markdown("\n\n")
    st.markdown("### 📁 上传数据文件开始分析")
    st.markdown("请在左侧边栏上传校园能耗数据Excel文件，包含以下列：")
    
    # Sample data structure
    sample_data = pd.DataFrame({
        "日期": ["2024-01-01", "2024-02-01", "2024-03-01"],
        "电力(kWh)": [1200, 1100, 1300],
        "水(吨)": [50, 45, 55],
        "燃气(m3)": [100, 90, 110],
        "部门": ["行政楼", "教学楼", "宿舍区"]
    })
    
    st.markdown("#### 数据格式示例：")
    st.dataframe(sample_data, use_container_width=True)
    
    st.markdown("\n### 🎯 功能特点")
    features = [
        "✅ 自动识别和清洗数据",
        "✅ 基于湖北电网碳强度计算碳排放",
        "✅ 多维度数据分析（时间/部门/能耗类型）",
        "✅ 直观的数据可视化（趋势图/饼图/桑基图）",
        "✅ 智能识别寒暑假特殊情况"
    ]
    
    for feature in features:
        st.markdown(feature)
    
    st.markdown("\n### 🔍 分析结果")
    st.markdown("- 碳排放时间趋势分析")
    st.markdown("- 各部门碳排放占比")
    st.markdown("- 各能源类型碳排放分析")
    st.markdown("- 校园碳流动桑基图")
    st.markdown("- 关键指标和减排建议")