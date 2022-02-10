# -*- coding: utf-8 -*-
"""
Created on Aug 30 18:04:22 2021

@author: larryprato
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import yahoo_fin.stock_info as si
from PIL import Image

html_header="""
<head>
<title>Benford_Law</title>
<meta charset="utf-8">
<meta name="keywords" content="benford's law">
<meta name="description" content="benforr law">
<meta name="author" content="Larry Prato">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Oswald|Noto+Sans">
</head>
<h2 style=" padding-top: 20px; padding-bottom: 0px; padding-left: 10px; background: #60759f; font-size:230%; color:#f0f2f6; font-family:Oswald, sans-serif;"> BENFORD'S LAW & STOCK MARKET <br>
 <h3 style=" padding-top: 0px; padding-bottom: 0px; color:#f0f2f6; font-size:70%; font-family:Oswald, sans-serif"> EXPRESS CHECKING</h3> <br>
 <hr style= " display: block;
  padding-top: 0px;
  padding-bottom: 0px;
  margin-top: 0em;
  margin-bottom: 0em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;"></h2>
"""

hide_streamlit_style = """
<style>
.css-hi6a2p {padding-top: 0rem;}
</style>
"""
st.set_page_config(page_title="BENFORD'S LAW", page_icon="♠️", layout="wide")
st.markdown(hide_streamlit_style, unsafe_allow_html=True) # it doesn't works with layout="wide" / only "centered" 
st.markdown('<style>body{background-color: #FFF1E5}</style>',unsafe_allow_html=True)
st.markdown(html_header, unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_data():
    stocks = si.tickers_sp500()
    return stocks
stocks = pd.read_excel('S&P500-wiki.xlsx')



X_expect = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
Y_expect = [0.30103, 0.17609, 0.12494, 0.09691, 0.07918, 0.06695, 0.05799, 0.05115, 0.04576]


def get_df(stock):
  inco_stmt= si.get_balance_sheet(stock)
  bal_sheet = si.get_balance_sheet(stock)
  cashflow = si.get_cash_flow(stock)
  ndf = cashflow.copy()
  for i in range(cashflow.shape[0]): #iterate over rows
      for j in range(cashflow.shape[1]): #iterate over columns
          first_digit = str(abs(cashflow.iloc[i,j]))
          first_digit = first_digit[0]
          ndf.iloc[i,j] = first_digit
  ndf1 = inco_stmt.copy()
  for i in range(inco_stmt.shape[0]): #iterate over rows
      for j in range(inco_stmt.shape[1]): #iterate over columns
          first_digit = str(abs(inco_stmt.iloc[i,j]))
          first_digit = first_digit[0]
          ndf1.iloc[i,j] = first_digit
  ndf2 = bal_sheet.copy()
  for i in range(bal_sheet.shape[0]): #iterate over rows
      for j in range(bal_sheet.shape[1]): #iterate over columns
          first_digit = str(abs(bal_sheet.iloc[i,j]))
          first_digit = first_digit[0]
          ndf2.iloc[i,j] = first_digit
  first_digits = pd.concat([ndf, ndf1, ndf2])
  categ = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
  df_values= pd.DataFrame(index = categ)
  df_values['val_obs'] =0
  for i in range(first_digits.shape[0]): #iterate over rows
    for j in range(first_digits.shape[1]): #iterate over columns
        if first_digits.iloc[i,j] == '1':
          df_values.iloc[[0,j]]+=1
        elif first_digits.iloc[i,j] == '2':
          df_values.iloc[[1,j]]+=1
        elif first_digits.iloc[i,j] == '3':
          df_values.iloc[[2,j]]+=1
        elif first_digits.iloc[i,j] == '4':
          df_values.iloc[[3,j]]+=1
        elif first_digits.iloc[i,j] == '5':
          df_values.iloc[[4,j]]+=1
        elif first_digits.iloc[i,j] == '6':
          df_values.iloc[[5,j]]+=1
        elif first_digits.iloc[i,j] == '7':
          df_values.iloc[[6,j]]+=1
        elif first_digits.iloc[i,j] == '8':
          df_values.iloc[[7,j]]+=1
        elif first_digits.iloc[i,j] == '9':
          df_values.iloc[[8,j]]+=1
  df_values["categ"] = categ
  df_values['freq_exp'] = Y_expect
  df_values['val_exp']= round(df_values['freq_exp']*df_values['val_obs'].sum(),0)
  df_values['x_sq'] =(df_values['val_obs']-df_values['val_exp'])**2/df_values['val_exp']
  return df_values


def generate_chart(stock):
  digits = get_df(stock)
  fig = px.bar(digits, x= 'categ', y= 'val_obs', labels={'categ':'<b>Digit</b>', 'val_obs':'<b>Real Value</b>'})
  fig.add_trace(go.Scatter(x= digits.categ, y= digits.val_exp, name="Benford's Law"))
  fig.update_layout(title={'text':stock, 'x': 0.5},  plot_bgcolor="#FFF9F5", paper_bgcolor = "#FFF9F5", 
        height= 280, width=500, margin=dict(l=10, r=10, b=10,t=40), showlegend=True, title_font=dict(size=18, family='Oswald, sans-serif', color='#262A33'),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
  fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5, opacity=0.6)
  fig.update_xaxes(showticklabels=True, title_font=dict(size=14, family='Oswald, sans-serif', color='#262A33'))
  fig.update_yaxes(title_font=dict(size=14, family='Oswald, sans-serif', color='#262A33'))
  return st.plotly_chart(fig)


def chi_square(stock):
  df_values=get_df(stock)
  p = 0.05
  GL = 8
  X_nom = 15.507 # X observado por tabla
  X_Cal = df_values['x_sq'].sum()
  if X_Cal <= X_nom:
    resp = print("X^2=", X_Cal, "// With 95% of confidence the distribuition fits to Benford's Law ", X_Cal)
  else:
    resp = print("X^2=", X_Cal, "// With 95% of confidence the distribuition does not fit to Benford's Law ", X_Cal)
  return resp

############################################################################################
html_content_1="""
<h2 style="font-family:Oswald, sans-serif; color:#262A33"><b>Benford's law</b></h2>
<p style=" line-height: 1.35; font-family:Oswald, sans-serif; color:#262A33; font-size: 20px;">
The first time I remember hearing about this topic was in the NETFLIX series "OZARK". 
It was in a scene where the main character of the series (Marty Byrde) was asking an FBI agent 
if she was trying to apply Benford's Law to find a predictable pattern in his business... 
So, I did some searching, and found that it seems to be a widely used resource to highlight any irregularities in accounting data.
Benford's Law, also called the law of anomalous numbers, or the first-digit law, 
is an observation about the frequency distribution of leading digits in many real-life 
sets of numerical data. The law states that in many naturally occurring collections of numbers, 
the leading digit is likely to be small. In sets that obey the law, the number 1 appears as 
the leading significant digit about 30% of the time, while 9 appears as the leading significant 
digit less than 5% of the time.
</p>
"""

X = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
Y = [0.30103, 0.17609, 0.12494, 0.09691, 0.07918, 0.06695, 0.05799, 0.05115, 0.04576]

st.write("")
st.write("")

with st.beta_expander("View / Hide explanation"):
    with st.beta_container():
        col1, col2, col3, col4, col5 = st.beta_columns([1,8,1,8,1])
        with col1:
            st.write("")
        with col2:
            st.markdown(html_content_1, unsafe_allow_html=True)

        with col3:
            st.write("")

        with col4:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            fig = px.bar(x= X_expect, y= Y_expect, labels={'x':'<b>Digit</b>', 'y':'<b>P D(%)</b>'})
            fig.add_trace(go.Scatter(x= X_expect, y= Y_expect, name="Benford's Law"))
            fig.update_layout(title={'text':"<b>Distribution of first digits</b>", 'x': 0.5},  plot_bgcolor="#FFF9F5", paper_bgcolor = "#FFF9F5", 
                 height= 280, width=500, margin=dict(l=10, r=10, b=10,t=40), showlegend=True, title_font=dict(size=18, family='Oswald, sans-serif', color='#262A33'),
                 legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
            fig.update_xaxes(title_font=dict(size=14, family='Oswald, sans-serif', color='#262A33'))
            fig.update_yaxes(title_font=dict(size=14, family='Oswald, sans-serif', color='#262A33'))
            st.plotly_chart(fig)

        with col5:
            st.write("")

############################################################################################
st.write("")
st.write("")

html_content_2="""
<h2 style="font-family:Oswald, sans-serif; color:#262A33"><b>Hands-on Benford's Law</b></h2>
<p style=" line-height: 1.35; font-family:Oswald, sans-serif; color:#262A33; font-size: 20px;">
Now, let's go to see how the publicly available financial information of companies in the stock market fits to this law.
</p>
"""

html_content_3="""
<h2 style="font-family:Oswald, sans-serif; color:#262A33"><b>Disclaimer</b></h2>
<p style=" line-height: 1.35; font-family:Oswald, sans-serif; color:#262A33; font-size: 20px;">
This application is for purely theoretical purposes and provides a quick glimpse to satisfy 
curiosity and see how the publicly available financial information of S&P500 companies conforms to this law.  
</p>
"""


with st.beta_container():
    col1, col2, col3 = st.beta_columns([1,5,1])
    with col1:
        st.write("")

    with col2:
        st.markdown(html_content_2, unsafe_allow_html=True)

    with col3:
        st.write("")

with st.beta_container():
    col1, col2, col3, col4, col5 = st.beta_columns([1,8,1,8,1])
    with col1:
        st.write("")
        
    with col2:
        st.markdown('***')
        st.markdown('### **Stock with a regular fit **')
        st.markdown('***')
        st.markdown("#### ** Distribution of first digits for: **")                    
        generate_chart("NVDA")
        st.markdown('***')
    with col3:
        st.write("")

    with col4:
        col4.markdown('***')
        col4.markdown('### ** Stock with irregular fit **')
        col4.markdown('***')
        st.markdown("#### ** Distribution of first digits for: **")
        generate_chart("DPZ")
        col4.markdown('***')

    with col5:
        st.write("")

############################################################################################
st.write("")
st.write("")

with st.beta_container():
    col1, col2, col3 = st.beta_columns([1,15,3])
    with col1:
        st.write("")
    with col2:
        image = Image.open('finviz.png')
        st.image(image, caption='Finviz S&P500 Map Sep.02.2021')
    with col3:
        st.write("")

st.write("")
st.write("") 

with st.beta_container():
    col1, col2, col3, col4, col5 = st.beta_columns([1,5,1, 5,1])
    with col1:
        st.write("")
    with col2:
        st.markdown("### ** Enter some stock ticker/symbol:**")
        user_input = st.text_input("Let's check to...", 'NVDA')
        if user_input:
            stock= user_input.upper()
        selected = stocks.loc[stocks['Symbol']==stock, 'Security']
        selected = selected.iloc[0]
        st.write()        
        st.markdown("### ** Selected stock: **")
        st.write(selected)

    with col3:
        st.write()         


    with col4:
        st.write()         
        st.markdown("#### ** Distribution of first digits for: **") 
        st.write()         
        generate_chart(stock)
        df_values=get_df(stock)
        p = 0.05
        GL = 8
        X_nom = 15.507 # X observado por tabla
        X_Cal = df_values['x_sq'].sum()
        if X_Cal <= X_nom:
            resp = print("X^2=", X_Cal, "// With 95% of confidence the distribuition fits to Benford's Law.")
        elif X_Cal > X_nom:
            resp = print("X^2=", X_Cal, "// With 95% of confidence the distribuition does not fit to Benford's Law.")
        a = resp
        st.markdown('### ** Chi-Square Statistic: ** ') 
        st.markdown(X_Cal)
        st.markdown("According to the Chi-Squared Test, in case the previous value was greater than 15.507 (critical value for 8 degrees of freedom and α = 0.05), means that the stock does not fit to Benford's Law.")

    with col5:
        st.write("")


html_content_3="""
<h3 style="font-family:Oswald, sans-serif; color:#262A33"><b>Disclaimer:</b></h3>
<p style=" line-height: 1.35; font-family:Oswald, sans-serif; color:#262A33; font-size: 15px;">
This application is for purely educational purposes and provides a quick glimpse to satisfy 
curiosity. It does not support any conclusive determination.  
</p>
"""
st.markdown(html_content_3, unsafe_allow_html=True)

html_br="""
<br>
"""
st.markdown(html_br, unsafe_allow_html=True)

html_line="""
<br>
<br>
<br>
<br>
<hr style= "  display: block;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  margin-left: auto;
  margin-right: auto;
  border-style: inset;
  border-width: 1.5px;">
<p style="color:Gainsboro; text-align: right;">By: larryprato@gmail.com</p>
"""
st.markdown(html_line, unsafe_allow_html=True)
