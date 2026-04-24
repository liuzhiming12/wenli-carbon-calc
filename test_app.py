import streamlit as st
import pandas as pd

st.title("测试应用")
st.write("Streamlit环境测试")
st.write("scikit-learn已成功安装")

# 测试基本功能
df = pd.DataFrame({
    'name': ['test1', 'test2'],
    'value': [1, 2]
})
st.dataframe(df)