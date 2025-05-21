import streamlit as st
import pandas as pd
import plotly.express as px
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_title="لوحة تحليل البيانات", layout="wide")

st.title("📊 لوحة تحليل أي ملف - Excel / CSV")

# 1- حمِّل الملف
up_file = st.file_uploader("ارفع ملفك هنا", type=["xlsx", "xls", "csv"])
if up_file:
    # 2- اقرأ البيانات
    df = (pd.read_excel(up_file) if up_file.name.endswith(("xlsx", "xls"))
          else pd.read_csv(up_file))
    st.success(f"تم التحميل: ‎{up_file.name}‎ — ‎{len(df):,}‎ صفّ")
    
    # 3- معاينة و-تحرير
    edited = st.data_editor(df, use_container_width=True)  # جديد 2025
    with st.expander("إحصاءات سريعة"):
        st.dataframe(edited.describe(include="all").T)
    
    # 4- اختيار عمودين للرسم
    cols = edited.select_dtypes("number").columns
    if len(cols) >= 2:
        x = st.selectbox("المحور X", cols, key="x")
        y = st.selectbox("المحور Y", cols, key="y")
        fig = px.scatter(edited, x=x, y=y, trendline="ols",
                         title=f"{y} مقابل {x}")
        st.plotly_chart(fig, use_container_width=True)
    
    # 5- تقرير تلخيصي آلي
    if st.checkbox("🔍 إنشاء تقرير ذكي (Profiling)"):
        pr = ProfileReport(edited, minimal=True, progress_bar=False)
        st_profile_report(pr)
