# Wenli Carbon Calculator · 文理碳算

校园级碳足迹计算器 — 批量处理水电燃气账单，生成 Scope 1/2/3 碳排放报告。

## What It Does

- 上传校园能耗 Excel 数据，一键计算碳排放
- 自动清洗脏数据：识别混合日期格式、规范部门名称、填补缺失值
- 按时间/部门/能源类型多维度分析
- 可视化仪表盘：趋势图、部门占比、桑基图、Scope 分类饼图
- 投入-产出强度指标（人均/单位面积碳排放）
- 基于历史数据的线性回归排放预测
- 碳汇抵消分析（树木、林地、草坪）
- AI 智能减排建议（通义千问 API，自动降级到模板）

## Architecture

```
core/
├── config.py             # 碳排放因子常量 + API 配置
├── data_loader.py        # Excel 读取 → 日期检测 → 列名规范化 → 缺失值填补
├── carbon_calculator.py  # 能耗数据 × 碳因子 → 碳排放量
├── analyzer.py           # 时间趋势 / 部门对比 / 强度指标 / 预测 / 碳汇
├── visualizer.py         # Plotly 图表生成
└── ai_advisor.py         # 通义千问 API 减排建议

ui/
└── app.py                # Streamlit 仪表盘

data/raw/
└── generate_sample_data.py  # 合成数据生成器（500+ 行校园账单）
```

### Data Flow

```
Excel 上传 (水电燃气账单)
        │
        ▼
  data_loader.py  ── 清洗、规范化
        │
        ▼
  carbon_calculator.py  ── 碳排放计算
        │
        ├──► analyzer.py  ── 多维分析 + 预测 + 碳汇
        │
        └──► visualizer.py  ── 图表
                   │
                   ▼
            Streamlit 仪表盘
```

## Tech Stack

Python 3.12 · Pandas · Streamlit · Plotly · scikit-learn · 通义千问 API

## Carbon Factors

使用 **湖北电网 OM 碳排放因子 0.4044 kgCO₂/kWh**（MEE 2025 年发布，2023 年各区域电网数据）：

| 能源类型 | 碳排放因子 | Scope |
|----------|-----------|-------|
| 电力 | 0.4044 kgCO₂/kWh | Scope 2 |
| 自来水 | 0.28 kgCO₂/t | Scope 3 |
| 天然气 | 2.17 kgCO₂/m³ | Scope 1 |

## Quick Start

```bash
git clone https://github.com/liuzhiming12/wenli-carbon-calc.git
cd wenli-carbon-calc

pip install -r requirements.txt
streamlit run ui/app.py
```

在浏览器中打开 `http://localhost:8501`，上传 Excel 数据即可开始分析。

## Data Journey

测试数据为 **500+ 行合成的校园月度能耗账单**，故意引入以下"脏数据"来测试清洗管线：

1. **日期混乱**：同一列中混合 `2023/1/1`、`2023-01-01`、`Jan 1 2023` 三种格式
2. **部门名称不一致**：同一部门写成 "Info. Sci." / "Information Science" / "信息学院"
3. **燃气账单缺失**：随机空值 → 用寒暑假外月均值填补
4. **寒暑假低能耗**：1-2 月、7-8 月零值 → 非假期均值填补

## Limitations

- 静态碳因子（0.4044）；合成数据验证，尚未在真实校园部署
- 无 IoT 实时接入，依赖手动上传 Excel
- 情景预测使用简单线性回归，未经过外部基准验证
- 缺失值填补策略较基础（均值填补）

## Recent Updates

- **Jul 2026**: 修复 gas factor 不一致、清理死代码、优化 AI advisor 数据摘要、移除无用依赖、UTF-8 .gitignore
- **May 2026**: 增强数据清洗管线，支持多种日期格式自动识别
- **May 2026**: 添加部门名称别名映射标准化
- **Apr 2026**: 构建合成数据生成器用于边界测试

## 🌐 红鸟碳眼 · Redbird Carbon Eye

**红鸟碳眼** 是我在红鸟挑战营第三期打造的碳管理产品矩阵，包含两个互补模块：

| 模块 | 定位 | 粒度 | 输入 | 场景 |
|------|------|------|------|------|
| **[江城碳眼 Pro](https://github.com/liuzhiming12/jiangcheng-carbon-eye)** | 实时代码级监测 | 进程级、秒级 | 代码片段/文件/文件夹 | 开发者自查 |
| **文理碳算** ← 本项目 | 批量机构碳核算 | 建筑级、月级 | 水电燃气账单 Excel | 校园/企业 ESG 报告 |

> 两个项目共享同一套碳排放因子引擎（湖北电网 OM 因子 0.4044 kgCO₂/kWh，MEE 2025），
> 从不同维度覆盖"代码运行→机构运营"的完整碳足迹链路。

## 👤 关于作者

**刘志明** · 武汉文理学院 · 红鸟挑战营第三期

- GitHub: [@liuzhiming12](https://github.com/liuzhiming12)
- Email: liuzhiming_2005@qq.com

> 武汉本地开发者普遍不关注代码碳排放，企业 ESG 报告中 IT 部门能耗数据常为空白。
> 我通过这两个项目，尝试用轻量级工具填补这一缺口——从一行代码到一个校园，碳皆可量化。

## License

MIT
