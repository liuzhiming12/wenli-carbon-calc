import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_loader import load_campus_energy_data
from core.carbon_calculator import calculate_carbon_emissions
from core.analyzer import (
    analyze_carbon_emissions,
    calculate_intensity_metrics,
    predict_future_emissions,
    calculate_carbon_sink,
    compare_emissions_with_sink
)
from core.visualizer import visualize_carbon_emissions
from core.utils.ai_advisor import generate_emission_reduction_suggestions

st.set_page_config(
    page_title="文理碳计 - 校园碳足迹计算器",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🌍 文理碳计")
st.sidebar.markdown("武汉文理学院校园碳足迹计算器")
st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(
    "上传校园能耗数据Excel文件",
    type=["xlsx", "xls"]
)

st.sidebar.subheader("🔧 分析设置")
analysis_type = st.sidebar.selectbox(
    "分析类型",
    ["全部", "时间趋势", "部门对比", "能耗类型"]
)

time_granularity = st.sidebar.selectbox(
    "时间粒度",
    ["月", "季度", "年"]
)

st.title("🌍 文理碳计 - 校园碳足迹计算器")
st.markdown("## 武汉文理学院校园能耗与碳排放分析工具")

if uploaded_file is not None:
    with open("temp_data.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        st.info("正在加载和清洗数据...")
        df = load_campus_energy_data("temp_data.xlsx")

        st.info("正在计算碳排放...")
        df_with_carbon = calculate_carbon_emissions(df)

        st.info("正在分析数据...")
        analysis_map = {"全部": "all", "时间趋势": "time", "部门对比": "department", "能耗类型": "energy"}
        time_map = {"月": "month", "季度": "quarter", "年": "year"}

        analysis_results = analyze_carbon_emissions(
            df_with_carbon,
            analysis_type=analysis_map[analysis_type],
            time_granularity=time_map[time_granularity]
        )

        st.info("正在生成可视化图表...")
        charts = visualize_carbon_emissions(analysis_results, chart_type="all")

        st.success("分析完成！")

        st.subheader("📊 数据预览")
        st.dataframe(df_with_carbon.head(), width='stretch')

        st.subheader("📈 关键指标")
        if analysis_results.get("key_metrics"):
            metrics = analysis_results["key_metrics"]
            col1, col2 = st.columns(2)

            if "highest_emission_period" in metrics:
                col1.metric(
                    "碳排放最高时期",
                    f"{metrics['highest_emission_period']['period']}",
                    f"{metrics['highest_emission_period']['emission']:.2f} 吨"
                )

            if "highest_emission_department" in metrics:
                col2.metric(
                    "碳排放最高部门",
                    metrics['highest_emission_department']['department'],
                    f"{metrics['highest_emission_department']['emission']:.2f} 吨 ({metrics['highest_emission_department']['percentage']:.1f}%)"
                )

        st.subheader("⚡ 能耗类型分析")
        if analysis_results.get("energy_type_analysis"):
            energy_data = analysis_results["energy_type_analysis"]
            energy_df = pd.DataFrame({
                "能源类型": ["电力", "水", "燃气"],
                "碳排放量(吨)": [energy_data['emissions']['电力'], energy_data['emissions']['水'], energy_data['emissions']['燃气']],
                "占比(%)": [energy_data['percentages']['电力'], energy_data['percentages']['水'], energy_data['percentages']['燃气']],
                "能耗量": [
                    f"{energy_data['consumption']['电力(kWh)']:.0f} kWh",
                    f"{energy_data['consumption']['水(吨)']:.0f} 吨",
                    f"{energy_data['consumption']['燃气(m3)']:.0f} m3"
                ]
            })
            st.dataframe(energy_df, width='stretch')

        st.subheader("📈 数据可视化")

        if charts.get("trend_chart"):
            st.markdown("### 碳排放时间趋势")
            st.plotly_chart(charts["trend_chart"], width='stretch')

        if charts.get("department_chart"):
            st.markdown("### 部门碳排放占比")
            st.plotly_chart(charts["department_chart"], width='stretch')

        if charts.get("energy_chart"):
            st.markdown("### 能源类型分析")
            st.plotly_chart(charts["energy_chart"], width='stretch')

        if charts.get("sankey_chart"):
            st.markdown("### 碳流动桑基图")
            st.plotly_chart(charts["sankey_chart"], width='stretch')

        st.markdown("---")
        st.subheader("📐 投入-产出分析")

        st.markdown("输入校园基本参数，计算人均和单位面积碳排放指标：")

        col_pop, col_area = st.columns(2)

        with col_pop:
            total_population = st.number_input(
                "校园总人数（人）",
                min_value=0,
                value=10000,
                step=100,
                help="包括学生和教职工总数"
            )

        with col_area:
            total_area = st.number_input(
                "总建筑面积（平方米）",
                min_value=0.0,
                value=100000.0,
                step=1000.0,
                help="校园总建筑面积"
            )

        if st.button("计算碳排放强度", type="primary"):
            intensity_results = calculate_intensity_metrics(
                df_with_carbon,
                total_population=total_population if total_population > 0 else None,
                total_area=total_area if total_area > 0 else None
            )

            st.info(f"总碳排放量：{intensity_results['total_emission']:.2f} 吨 CO2")

            metrics_col1, metrics_col2 = st.columns(2)

            if "per_capita" in intensity_results["available_metrics"]:
                metrics_col1.metric(
                    "人均碳排放",
                    f"{intensity_results['per_capita']['value']:.2f} kg CO₂/人",
                    help=f"基于{total_population}人计算"
                )

            if "per_area" in intensity_results["available_metrics"]:
                metrics_col2.metric(
                    "单位面积碳排放",
                    f"{intensity_results['per_area']['value']:.2f} kg CO₂/m²",
                    help=f"基于{total_area}m²计算"
                )

            st.markdown("""
            **价值说明**：将绝对数字转化为可比的管理指标，让不同规模的机构能够进行横向对标，为管理决策提供更科学的依据。
            """)

        st.markdown("---")
        st.subheader("🔮 情景预测")

        st.markdown("基于历史数据预测未来碳排放，模拟不同节能目标下的减排效果：")

        col_pred1, col_pred2 = st.columns(2)

        with col_pred1:
            prediction_months = st.slider(
                "预测月数",
                min_value=3,
                max_value=24,
                value=12,
                step=1,
                help="预测的未来月数"
            )

        with col_pred2:
            energy_savings_rate = st.slider(
                "预计节能率",
                min_value=0.0,
                max_value=50.0,
                value=0.0,
                step=1.0,
                format="%.0f%%",
                help="预计通过节能措施实现的能源消耗降低比例"
            ) / 100.0

        if st.button("生成预测", type="primary"):
            prediction_results = predict_future_emissions(
                df_with_carbon,
                energy_savings_rate=energy_savings_rate,
                prediction_months=prediction_months
            )

            if "error" not in prediction_results:
                st.info(f"当前趋势：{prediction_results['trend_direction']}（每月{'+' if prediction_results['trend_slope'] > 0 else ''}{prediction_results['trend_slope']:.2f} 吨）")

                pred_col1, pred_col2, pred_col3 = st.columns(3)

                pred_col1.metric(
                    "预测期总排放（基准）",
                    f"{prediction_results['baseline_total']:.2f} 吨",
                    help="不采取节能措施时的预测总排放"
                )

                pred_col2.metric(
                    "节能后预测排放",
                    f"{prediction_results['with_savings_total']:.2f} 吨",
                    help=f"节能率{energy_savings_rate*100:.0f}%时的预测排放"
                )

                saved = prediction_results['baseline_total'] - prediction_results['with_savings_total']
                pred_col3.metric(
                    "可减排量",
                    f"{saved:.2f} 吨",
                    delta=f"{(saved/prediction_results['baseline_total']*100):.1f}%",
                    help="通过节能措施可减少的碳排放量"
                )

                st.markdown("#### 未来排放预测趋势")
                st.line_chart(prediction_results['predictions'])

                st.markdown("""
                **价值说明**：从"看过去"到"看未来"，帮助管理者模拟不同节能策略下的减排效果，让碳管理从被动核算变为主动规划。
                """)
            else:
                st.warning(prediction_results["error"])

        st.markdown("---")
        st.subheader("🌳 碳汇抵消分析")

        st.markdown("引入校园绿化碳汇能力，展示距离碳中和的距离：")

        sink_col1, sink_col2, sink_col3 = st.columns(3)

        with sink_col1:
            tree_count = st.number_input(
                "树木数量（棵）",
                min_value=0,
                value=1000,
                step=50,
                help="校园内树木总数"
            )

        with sink_col2:
            forest_area = st.number_input(
                "森林面积（m²）",
                min_value=0.0,
                value=5000.0,
                step=100.0,
                help="校园森林/绿地面积"
            )

        with sink_col3:
            grass_area = st.number_input(
                "草坪面积（m²）",
                min_value=0.0,
                value=10000.0,
                step=100.0,
                help="校园草坪面积"
            )

        if st.button("计算碳汇", type="primary"):
            sink_data = calculate_carbon_sink(
                tree_count=tree_count if tree_count > 0 else None,
                forest_area=forest_area if forest_area > 0 else None,
                grass_area=grass_area if grass_area > 0 else None
            )

            emission_data = {"total_emission": analysis_results["energy_type_analysis"]["emissions"]["总"]}

            comparison = compare_emissions_with_sink(emission_data, sink_data)

            sink_col_a, sink_col_b = st.columns(2)

            sink_col_a.metric(
                "年碳汇吸收量",
                f"{sink_data['total_absorption']:.2f} 吨 CO₂",
                help="校园绿化每年可吸收的CO₂量"
            )

            sink_col_b.metric(
                "碳抵消比例",
                f"{comparison['offset_ratio']:.2f}%",
                delta=comparison['status_text'],
                help="碳汇占总排放的比例"
            )

            st.progress(
                min(comparison['offset_ratio'] / 100, 1.0),
                text=f"抵消进度：{comparison['offset_ratio']:.2f}%"
            )

            net = comparison['net_emission']
            if net > 0:
                st.warning(f"距离碳中和还需额外吸收：{comparison['additional_sink_needed']:.2f} 吨 CO₂")
            else:
                st.success("🎉 恭喜！您的校园已达到碳中和！")

            st.markdown("""
            **价值说明**：引入"碳中和"闭环思维，直观展示校园距离真正碳中和的距离，这是齐教授研究中非常关注的核心理念。
            """)

        st.markdown("---")
        st.subheader("🤖 AI 减排建议")
        try:
            with st.spinner("正在生成减排建议..."):
                suggestions = generate_emission_reduction_suggestions(analysis_results)
            st.markdown(suggestions)
        except Exception as e:
            st.warning(f"生成减排建议时出现错误: {str(e)}")

        os.remove("temp_data.xlsx")

    except Exception as e:
        st.error(f"分析过程中出现错误: {str(e)}")
        if os.path.exists("temp_data.xlsx"):
            os.remove("temp_data.xlsx")
else:
    st.markdown("\n\n")
    st.markdown("### 📁 上传数据文件开始分析")
    st.markdown("请在左侧边栏上传校园能耗数据Excel文件，包含以下列：")

    sample_data = pd.DataFrame({
        "日期": ["2024-01-01", "2024-02-01", "2024-03-01"],
        "电力(kWh)": [1200, 1100, 1300],
        "水(吨)": [50, 45, 55],
        "燃气(m3)": [100, 90, 110],
        "部门": ["行政楼", "教学楼", "宿舍区"]
    })

    st.markdown("#### 数据格式示例：")
    st.dataframe(sample_data, width='stretch')

    st.markdown("\n### 🎯 功能特点")
    features = [
        "✅ 自动识别和清洗数据",
        "✅ 基于湖北电网碳强度计算碳排放",
        "✅ 多维度数据分析（时间/部门/能耗类型）",
        "✅ 直观的数据可视化（趋势图/饼图/桑基图）",
        "✅ 人均和单位面积碳排放强度指标",
        "✅ 基于历史数据的未来排放预测",
        "✅ 校园碳汇抵消分析",
        "✅ 智能识别寒暑假特殊情况"
    ]

    for feature in features:
        st.markdown(feature)

    st.markdown("\n### 🔍 核心功能")
    st.markdown("- **投入-产出分析**：人均/单位面积碳排放强度")
    st.markdown("- **情景预测**：模拟不同节能目标下的减排效果")
    st.markdown("- **碳汇抵消**：展示距离碳中和的距离")
    st.markdown("- **AI 减排建议**：基于分析结果生成智能建议")