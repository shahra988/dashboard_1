
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 لوحة معلومات مشاريع التحزيم")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_excel("مشاريع التحزيم_.xlsx", sheet_name="Sheet1")
    df = df[['القطاع', 'اسم الشريك', 'المحافظة']].dropna()
    df.columns = ['القطاع', 'الشريك', 'المحافظة']
    return df

df = load_data()

# الشروط التفاعلية
sectors = st.multiselect("اختر قطاع/قطاعات:", df['القطاع'].unique(), default=df['القطاع'].unique())
partners = st.multiselect("اختر شريك/شركاء:", df['الشريك'].unique(), default=df['الشريك'].unique())
governorates = st.multiselect("اختر محافظة/محافظات:", df['المحافظة'].unique(), default=df['المحافظة'].unique())

# تصفية البيانات
filtered_df = df[
    (df['القطاع'].isin(sectors)) &
    (df['الشريك'].isin(partners)) &
    (df['المحافظة'].isin(governorates))
]

# توزيع حسب القطاع
col1, col2 = st.columns(2)
with col1:
    sector_count = filtered_df['القطاع'].value_counts().reset_index()
    sector_count.columns = ['القطاع', 'عدد المشاريع']
    fig = px.pie(sector_count, values='عدد المشاريع', names='القطاع', title="توزيع المشاريع حسب القطاع")
    st.plotly_chart(fig, use_container_width=True)

# توزيع حسب الشريك
with col2:
    partner_count = filtered_df['الشريك'].value_counts().reset_index()
    partner_count.columns = ['الشريك', 'عدد المشاريع']
    fig2 = px.bar(partner_count, x='عدد المشاريع', y='الشريك', orientation='h', title="عدد المشاريع حسب الشريك")
    st.plotly_chart(fig2, use_container_width=True)

# توزيع حسب المحافظة
col3, col4 = st.columns(2)
with col3:
    gov_count = filtered_df['المحافظة'].value_counts().reset_index()
    gov_count.columns = ['المحافظة', 'عدد المشاريع']
    fig3 = px.bar(gov_count, x='عدد المشاريع', y='المحافظة', orientation='h', title="عدد المشاريع حسب المحافظة")
    st.plotly_chart(fig3, use_container_width=True)

# خريطة حرارية
with col4:
    heatmap_data = filtered_df.groupby(['القطاع', 'المحافظة']).size().reset_index(name='عدد المشاريع')
    heatmap_pivot = heatmap_data.pivot(index='القطاع', columns='المحافظة', values='عدد المشاريع').fillna(0)
    st.write("### خريطة حرارية (القطاع × المحافظة)")
    st.dataframe(heatmap_pivot.style.background_gradient(cmap='YlOrBr'), use_container_width=True)

# جدول البيانات
st.markdown("### 📄 بيانات المشاريع بعد التصفية")
st.dataframe(filtered_df, use_container_width=True)
