import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def visualize_carbon_emissions(
    analysis_results: dict,
    chart_type: str = "all",  # "trend", "department", "energy", "sankey", "all"
    output_format: str = "interactive"  # "interactive", "static"
) -> dict:
    """
    Visualize carbon emissions data.

    Parameters
    ----------
    analysis_results : dict
        Analysis results from analyze_carbon_emissions function
    chart_type : str, default "all"
        Type of chart to generate: "trend", "department", "energy", "sankey", or "all"
    output_format : str, default "interactive"
        Output format: "interactive" (Plotly) or "static" (Matplotlib)

    Returns
    -------
    dict
        Dictionary of chart objects or configurations
    """
    charts = {
        "trend_chart": None,
        "department_chart": None,
        "energy_chart": None,
        "sankey_chart": None
    }

    if chart_type in ["all", "trend"] and analysis_results.get("time_trend") is not None:
        trend_chart = _create_trend_chart(analysis_results["time_trend"])
        charts["trend_chart"] = trend_chart

    if chart_type in ["all", "department"] and analysis_results.get("department_comparison") is not None:
        dept_data = analysis_results["department_comparison"]
        if isinstance(dept_data, pd.DataFrame):
            dept_chart = _create_department_chart(dept_data)
            charts["department_chart"] = dept_chart

    if chart_type in ["all", "energy"] and analysis_results.get("energy_type_analysis") is not None:
        energy_data = analysis_results["energy_type_analysis"]
        energy_chart = _create_energy_chart(energy_data)
        charts["energy_chart"] = energy_chart

    if chart_type in ["all", "sankey"]:
        sankey_chart = _create_sankey_chart(analysis_results)
        charts["sankey_chart"] = sankey_chart

    return charts

def _create_trend_chart(trend_data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend_data.index,
        y=trend_data['总碳排放(�?'],
        name='总碳排放',
        mode='lines+markers',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))

    energy_types = {
        '电力碳排�?�?': '#ff7f0e',
        '水碳排放(�?': '#2ca02c',
        '燃气碳排�?�?': '#9467bd'
    }

    for col, color in energy_types.items():
        if col in trend_data.columns:
            fig.add_trace(go.Scatter(
                x=trend_data.index,
                y=trend_data[col],
                name=col.replace('碳排�?�?', ''),
                mode='lines',
                line=dict(color=color, width=1, dash='dash')
            ))

    fig.update_layout(
        title='校园碳排放时间趋�?,
        xaxis_title='时间',
        yaxis_title='碳排�?�?',
        legend_title='能源类型',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )

    return fig

def _create_department_chart(dept_data: pd.DataFrame) -> go.Figure:
    fig = go.Figure(data=[go.Pie(
        labels=dept_data.index,
        values=dept_data['总碳排放(�?'],
        hole=.3,
        hoverinfo='label+percent+value',
        textinfo='label+percent',
        textfont=dict(size=12),
        marker=dict(
            colors=px.colors.qualitative.Set3,
            line=dict(color='#ffffff', width=2)
        )
    )])

    fig.update_layout(
        title='各部门碳排放占比',
        legend_title='部门',
        template='plotly_white',
        height=500
    )

    return fig

def _create_energy_chart(energy_data: dict) -> go.Figure:
    energy_types = ['电力', '�?, '燃气']
    emissions = [energy_data['emissions'][et] for et in energy_types]
    percentages = [energy_data['percentages'][et] for et in energy_types]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=energy_types,
        y=emissions,
        name='碳排放量(�?',
        marker_color='#1f77b4'
    ))

    fig.add_trace(go.Bar(
        x=energy_types,
        y=percentages,
        name='占比(%)',
        marker_color='#ff7f0e'
    ))

    fig.update_layout(
        title='各能源类型碳排放分析',
        xaxis_title='能源类型',
        yaxis_title='数�?,
        legend_title='指标',
        barmode='group',
        template='plotly_white',
        height=500
    )

    return fig

def _create_sankey_chart(analysis_results: dict) -> go.Figure:
    energy_data = analysis_results.get("energy_type_analysis")
    if not energy_data:
        return None

    dept_data = analysis_results.get("department_comparison")
    if not isinstance(dept_data, pd.DataFrame):
        sources = [0, 0, 0]
        targets = [1, 2, 3]
        values = [
            energy_data['emissions']['电力'],
            energy_data['emissions']['�?],
            energy_data['emissions']['燃气']
        ]
        labels = ['总碳排放', '电力', '�?, '燃气']
    else:
        sources = []
        targets = []
        values = []
        labels = ['总碳排放', '电力', '�?, '燃气']

        energy_nodes = {}
        for i, et in enumerate(['电力', '�?, '燃气'], start=1):
            energy_nodes[et] = i
            sources.append(0)
            targets.append(i)
            values.append(energy_data['emissions'][et])

        dept_nodes = {}
        for i, dept in enumerate(dept_data.index, start=4):
            dept_nodes[dept] = i
            labels.append(dept)

        for dept, dept_idx in dept_nodes.items():
            dept_emission = dept_data.loc[dept, '总碳排放(�?']
            for et, et_idx in energy_nodes.items():
                percentage = energy_data['percentages'][et] / 100
                flow_value = dept_emission * percentage
                sources.append(et_idx)
                targets.append(dept_idx)
                values.append(flow_value)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=[px.colors.qualitative.Set3[i % len(px.colors.qualitative.Set3)] for i in range(len(values))]
        )
    )])

    fig.update_layout(
        title='校园碳流动桑基图',
        template='plotly_white',
        height=600,
        width=800
    )

    return fig
