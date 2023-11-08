import inspect
import textwrap

import streamlit as st
import pandas as pd

file = st.file_uploader("Upload file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    
    n_rwos = st.slider('Choose number of rows to display', min_value=5, max_value=len(df), step=1)
    columns_to_show = st.multiselect('Select columns to show', df.columns.to_list(), default=df.columns.to_list())
    
    st.write(df[:n_rwos][columns_to_show])
    

def main():
    st.title("Streamlit ECharts Demo")

    with st.sidebar:
        st.header("Configuration")
        api_options = ("echarts", "pyecharts")
        selected_api = st.selectbox(
            label="Choose your preferred API:",
            options=api_options,
        )

        page_options = (
            list(ST_PY_DEMOS.keys())
            if selected_api == "pyecharts"
            else list(ST_DEMOS.keys())
        )
        selected_page = st.selectbox(
            label="Choose an example",
            options=page_options,
        )
        demo, url = (
            ST_DEMOS[selected_page]
            if selected_api == "echarts"
            else ST_PY_DEMOS[selected_page]
        )

        if selected_api == "echarts":
            st.caption(
                """ECharts demos are extracted from https://echarts.apache.org/examples/en/index.html, 
            by copying/formattting the 'option' json object into st_echarts.
            Definitely check the echarts example page, convert the JSON specs to Python Dicts and you should get a nice viz."""
            )
        if selected_api == "pyecharts":
            st.caption(
                """Pyecharts demos are extracted from https://github.com/pyecharts/pyecharts-gallery,
            by copying the pyecharts object into st_pyecharts. 
            Pyecharts is still using ECharts 4 underneath, which is why the theming between st_echarts and st_pyecharts is different."""
            )