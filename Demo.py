import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(
    page_title="Telcom Data Dashboard",
    page_icon=":bar_chart:",
    layout='wide'
)
st.title('Telcom Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
f1 = st.file_uploader(":file_folder: Upload a file", type=(["csv", "text", "xlsx"]))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    os.chdir(r"/Users/debasishguru/Desktop/untitled folder/Next Project Hike 5/Demo.py")
    df = pd.read_csv('cleaned_dataset_1.csv', encoding="ISO-8859-1")
col1, col2 = st.columns((2))
df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate'])
Start_time = df['StartDate'].max()
End_time = df['EndDate'].max()
with col1:
    date1 = pd.to_datetime(st.date_input("Start date", Start_time))
with col2:
    date2 = pd.to_datetime(st.date_input("End date", End_time))
df_filtered = df[(df['StartDate'] >= date1) & (df['EndDate'] <= date2)].copy()
handset_manufacturer = st.sidebar.multiselect('Pick the Handset Manufacturer', df['Handset Manufacturer'].unique())
if not handset_manufacturer:
    df2 = df.copy()
else:
    df2 = df[df['Handset Manufacturer'].isin(handset_manufacturer)]
handset_type = st.sidebar.multiselect('Pick the Handset Type', df2['Handset Type'].unique())
if  not handset_type:
    df3=df.copy()
else:
    df3=df2[df2['Handset Type'].isin(handset_type)]
msisdn=st.sidebar.multiselect('Pick the misidn',df3['MSISDN/Number'].unique())
# Filter the data based on the handset manufacturer , handset type and msisdn/Number
if not handset_manufacturer and handset_type and msisdn:
    filtered_df=df
elif not  handset_type and msisdn:
    filtered_df=df[df['Handset Manufacturer'].isin(handset_manufacturer)]
elif not handset_manufacturer and msisdn:
    filtered_df=df[df['Handset Type'].isin(handset_type)]
elif  handset_type and msisdn:
    filtered_df=df3[df['Handset Type'].isin(handset_type)&df3['MSISDN/Number'].isin(msisdn)]
elif handset_manufacturer and msisdn:
    filtered_df=df3[df3['Handser Manufacturer'].isin(handset_manufacturer)&df3['MSISDN/Number'].isin(msisdn)]
elif handset_manufacturer and handset_type:
    filtered_df=df3[df3['Handset Manufacturer'].isin(handset_manufacturer)& df3['Handset Type'].isin(handset_type)]
elif msisdn:
    filtered_df=df3[df3['MSISDN/Number'].isin(msisdn)]
else:
    filtered_df=df3[df3['Handset Manufacturer'].isin(handset_manufacturer)& 
                    df3['Handset Type'].isin(handset_type) &
                    df3['MSISDN/Number'].isin(msisdn)]
category_df=filtered_df.groupby(by=['Netflix UL (Bytes)'], as_index=False)['Netflix DL (Bytes)'].count()
with col1:
    st.subheader('')
    fig=px.bar(category_df,x='Netflix UL (Bytes)',y='Netflix DL (Bytes)',
               template='seaborn')
    st.plotly_chart(fig,use_container_width=True,height=200)
with col2:
    st.subheader('Total UL and DL (Bytes customers)')
    fig=px.pie(filtered_df,values='Total UL (Bytes)',names='Handset Manufacturer',hole=0.5)
    fig.update_traces(text=filtered_df['Handset Manufacturer'],textposition='outside')
    st.plotly_chart(fig,use_container_width=True)
# Download the data 
cl1,cl2=st.columns(2)
with cl1:
    with st.expander('Netflix viewupdate'):
        st.write(category_df.style.background_gradient(cmap='viridis'))
        csv=category_df.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data',data=csv,file_name='ViewData.csv',mime='text/csv',
                           help='Click here to download the data as csv file')
with cl2:
    with st.expander('Total UL and DL bytes customers'):
        handset_manufacturer=filtered_df.groupby(by='Total UL (Bytes)',as_index=False)['Handset Manufacturer'].sum()
        st.write(handset_manufacturer.style.background_gradient(cmap='viridis'))
        csv=handset_manufacturer.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name='Total UL and DL Bytes customers',
                           mime='text/csv',help="click here to download the file as csv")
        
filtered_df['start_month_year']=filtered_df['StartDate'].dt.to_period("M")
filtered_df['end_month_year']=filtered_df['EndDate'].head(10).dt.to_period("M")
st.subheader('Timeseries Analysis')
linechart=pd.DataFrame(filtered_df.groupby(filtered_df['start_month_year'].dt.strftime("%Y:%b"))['Google DL (Bytes)'].sum()).reset_index()
fig2=px.line(linechart,x='start_month_year',y='Google DL (Bytes)',labels={'Google DL (Bytes)':'Bytes'},height=500,
             width=1000,template='gridon')
st.plotly_chart(fig2,use_container_width=True)

st.subheader('Manufacture Analysis')
linechart=pd.DataFrame(filtered_df.groupby(filtered_df['end_month_year'].dt.strftime("%Y : %b"))['Handset Manufacturer'].sum()).reset_index()
fig3=px.line(linechart,x='end_month_year',y='Handset Manufacturer',height=500,width=1000,template='gridon')
st.plotly_chart(fig2,use_container_width=True) 

with st.expander('view Data of Time series'):
    st.write(linechart.T.style.background_gradient(cmap='blue'))
    csv=linechart.to_csv(index=False).encode('utf-8')
    st.download_button('Downlad the data',data=csv,file_name='Time series.csv ',mime='text/csv')
    
# create a treem based on the handset Manufacurer, handset type and msisdn/number
st.subheader('Hierachical View of handset manufacturer')
fig3=px.treemap(filtered_df,path=['Handset Manufacturer','Handset Type','MSISDN/Number'],values='Netflix DL (Bytes)',
                hover_data=['Netflix DL (Bytes)'],color='MSISDN/Number')
fig3.update_layout(width=800,height=650)
st.plotly_chart(fig3,use_container_width=True)
     
chart1,chart2=st.columns((2))
with chart1:
    st.subheader('Other DL (Bytes)')
    fig=px.pie(filtered_df,values='Netflix DL (Bytes)',names='Manufacturer',template='plotly_dark')
    fig.update_traces(text=filtered_df['Other DL (Bytes)'],textposition='inside')
    st.plotly_chart(fig,use_container_width=True)
    
with chart2:
    st.subheader("Other UL (Bytes)")
    fig=px.pie(filtered_df,values="Other UL (Bytes)",names="Manufacturer",template='gridon')
    fig.update_traces(text=filtered_df['Manufacturer'],textposition='inside')
    st.plotly_chart(fig,use_container_width=True)
    
import plotly.figure_factory as ff
st.subheader(":point-righ:")
with st.expander("summry_Table"):
    df_sample=df[0:5][['Handset Manufacturer','Handset Type','MSISDN/Number','Netflix DL (Bytes)','Total UL (Bytes)','Other DL (Bytes)']]
    fig=ff.create_table(df_sample,colorscale='Cividis')
    st.plotly_chart(fig,use_container_width=True)
    
    #st.markdown('Other DL (Bytes) values per month')
    #filtered_df['end_month_year']=filtered_df['EndDate'].dt.month_name()
    #Other_DL_Bytes=pd.pivot_table(data=filtered_df,values='Manufacturer',
     #                             index=['Other DL (Bytes)'],columns='end_month_year')
    #st.write(Other_DL_Bytes.style.background_gradient(cmap='Blues'))
    
# Create a Scatter pot 
data1=px.scatter(filtered_df,x='Other DL (Bytes)',y='Netflix UL (Bytes)',size='Netflix DL (Bytes)')
data1['layout'].update(title='Relationship between Other DL (Bytes) and Manufacturer',
                       titlefont=dict(size=20),xaxis=dict(title="Other DL (Bytes)",titlefont=dict(size=19)),
                       yaxis=dict(title='Netflix DL (Bytes)',titlefont=dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))
# Dowload the original Dataset 
csv=df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data',data=csv,file_name='Data.csv',mime='text/csv')

