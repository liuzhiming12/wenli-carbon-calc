# 文理碳计 - 武汉文理学院校园碳足迹计算器

## 📋 项目概述

**文理碳计**是一款专为武汉文理学院设计的校园能耗与碳排放分析工具，旨在帮助学校了解校园能源使用情况，计算碳排放，并提供减排建议。

- **战略角色**：红鸟挑战营副项目 + 对齐齐晔教授"校园碳中和"研究方向
- **开发周期**：2026年6月13日 - 6月17日
- **技术栈**：Python 3.12 + Pandas 2.2.0 + Streamlit + Plotly

## 🎯 核心功能

### 1. 数据导入与清洗
- 支持读取校园水电燃气 Excel 数据
- 自动识别日期格式并转换
- 标准化列名与处理缺失值
- 智能处理寒暑假期间数据

### 2. 碳排放计算
- 基于湖北电网碳强度计算电力碳排放
- 支持水资源、燃气碳排放计算
- 提供详细的碳核算报告

### 3. 数据分析
- 时间趋势分析（按月/季度/年度）
- 部门对比分析（行政楼、教学楼、宿舍区）
- 能耗类型分析

### 4. 数据可视化
- 趋势折线图
- 部门饼图
- 能耗类型柱状图
- 校园碳流动桑基图（使用 Plotly）

### 5. AI 减排建议
- 结合齐晔教授研究方向
- 生成个性化校园减排建议

## 📁 项目结构

```
wenli_carbon_calc/
├── app/                  # Streamlit 应用
│   └── main.py           # 主应用入口
├── data/                 # 数据文件夹
│   └── raw/              # 原始数据
├── utils/                # 工具模块
│   ├── config.py         # 配置管理
│   └── ai_advisor.py     # AI 减排建议
├── data_loader.py        # 数据加载与清洗
├── carbon_calculator.py  # 碳排放计算
├── analyzer.py           # 数据分析
├── visualizer.py         # 数据可视化
├── README.md             # 项目说明
├── requirements.txt      # 依赖包
└── .env                  # 环境变量（需自行创建）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

项目使用 `.env` 文件来安全存储 API 密钥。请按照以下步骤创建配置文件：

#### Windows 系统

```powershell
# 在项目根目录下创建 .env 文件
echo QIANWEN_API_KEY=your_api_key_here > .env
```

#### 或手动创建

在项目根目录创建 `.env` 文件，内容如下：

```
QIANWEN_API_KEY=your_api_key_here
```

**注意**：
- `.env` 文件包含敏感信息，不会被提交到 Git
- 请将 `your_api_key_here` 替换为您的实际千问 API 密钥
- 切勿将 `.env` 文件分享或提交到版本控制系统

### 3. 运行应用

```bash
streamlit run app/main.py
```

### 4. 使用示例数据

项目提供了示例数据生成脚本，可以生成符合高校能耗规律的仿真数据：

```bash
cd data/raw
python generate_sample_data.py
```

生成的数据文件 `campus_energy_data.xlsx` 将保存在 `data/raw/` 目录下。

## 📊 数据格式要求

### Excel 数据格式

| 列名 | 说明 | 示例 |
|------|------|------|
| 日期 | 日期时间 | 2024-01-01 或 2024/1/1 |
| 电力(kWh) | 电力消耗(kWh) | 1200 |
| 水(吨) | 水消耗(吨) | 50 |
| 燃气(m3) | 燃气消耗(m³) | 100 |
| 部门（可选） | 消耗部门 | 行政楼/教学楼/宿舍区 |

## 🔧 技术实现

### 数据加载模块

```python
from data_loader import load_campus_energy_data

# 加载数据
df = load_campus_energy_data('data/raw/campus_energy.xlsx')
print(df.head())
```

### 碳排放计算模块

```python
from carbon_calculator import calculate_carbon_emissions

# 计算碳排放
df_with_carbon = calculate_carbon_emissions(df)
print(df_with_carbon.head())
```

### 数据分析模块

```python
from analyzer import analyze_carbon_emissions

# 分析数据
results = analyze_carbon_emissions(df_with_carbon, analysis_type="all")
```

### 数据可视化模块

```python
from visualizer import visualize_carbon_emissions

# 生成可视化图表
charts = visualize_carbon_emissions(results)
```

### AI 减排建议模块

```python
from utils.ai_advisor import generate_emission_reduction_suggestions

# 生成减排建议
suggestions = generate_emission_reduction_suggestions(results)
```

## 🤖 AI 功能配置

### 千问 API 密钥

项目使用千问 API 来生成智能减排建议。要启用此功能，您需要：

1. 获取千问 API 密钥
2. 将密钥配置到 `.env` 文件中

```bash
QIANWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**安全提示**：
- API 密钥属于敏感信息，请妥善保管
- 切勿将包含真实密钥的 `.env` 文件提交到 Git
- 定期更换 API 密钥以提高安全性

## 🎓 项目价值

1. **学术价值**：为校园碳中和研究提供数据支持
2. **实用价值**：帮助学校识别能耗高峰，优化能源使用
3. **教育价值**：作为校园 sustainability 教育的工具
4. **实践价值**：展示数据科学在环境领域的应用

## 🌟 特色亮点

- **数据驱动**：基于真实校园能耗数据模型
- **智能分析**：结合时间序列分析和部门对比
- **可视化呈现**：直观展示碳排放情况，包括高级桑基图
- **AI 增强**：基于千问 API 生成专业减排建议
- **用户友好**：交互式 Streamlit 界面
- **模块化设计**：代码结构清晰，易于扩展
- **安全存储**：API 密钥通过环境变量管理

## 📈 预期成果

- ✅ Excel 标准化碳核算报表
- ✅ 数据可视化图表（趋势图、饼图、桑基图）
- ✅ 交互式 Streamlit 应用
- ✅ 示例数据和完整代码
- ✅ AI 智能减排建议
- ⏳ 3 页精简版 PPT 汇报
- ⏳ PDF 分析报告

## 👥 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

MIT License

## 📞 联系方式

- **项目维护者**：[Your Name]
- **邮箱**：[your.email@example.com]
- **GitHub**：[https://github.com/liuzhiming12/wenli-carbon-calc](https://github.com/liuzhiming12/wenli-carbon-calc)