import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as pl
from bs4 import BeautifulSoup
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
#Scraping stock trendings from https://stockanalysis.com/trending/
def stock_trending(url):
    #create a list of tickers to return
    tickers_list = []
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,'lxml')
    symbols = soup.find_all('tr',class_='svelte-1tv1ofl')
    for symbol in symbols:
        ticker = symbol.find_all('a')
        for i in ticker:
            tickers_list.append(i.get_text())
    return tickers_list

#Change background color 
def color_change(val):
    return f'background-color: yellow'





col1, col2, col3 = st.columns([1,1,1])

stock_trendingURL = "https://stockanalysis.com/trending/"

# Get the list of trending tickers 
trending_tickers = stock_trending(stock_trendingURL)

###### Streamlit UI########
st.title("Stock Analysis Stream")
st.caption("This is a real time list of stocks scraped from https://stockanalysis.com/trending/")

tab1, tab2 = st.tabs(["Trending Stocks", "Popular Stocks"])

with tab1:
    st.markdown("Pick Your **Stock**")
    
    stock = st.selectbox("Stock",trending_tickers)
    
    #Show data
    st.markdown("""
        ##### Data 
        """)


    #Selected stock 
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        button1 = st.button('1 Month')
    with col2:
        button2 = st.button('6 Months')
        stock_historical = yf.download(stock,period="6mo")
    with col3:
        button3 = st.button('YTD')
    with col4:
        button4 = st.button('2 Years')
    with col5:
        button5 = st.button('5 years')
    
    if button1:
        stock_historical = yf.download(stock,period="1mo")
    if button2:
        stock_historical = yf.download(stock,period="6mo")
    if button3:
        stock_historical = yf.download(stock,period="ytd")
    if button4:
        stock_historical = yf.download(stock,period="2y")
    if button5:
        stock_historical = yf.download(stock,period="5y")
    #Show dataframe
    st.dataframe(stock_historical.style.applymap(color_change, subset=["Open","Close"])
                ,use_container_width=True)
    
    #Show Chart

    #OHLC Chart
    st.markdown(""" 
    ##### OHLC Chart""")

    fig = go.Figure(data=go.Ohlc(x=stock_historical.index,
                    open=stock_historical['Open'],
                    high=stock_historical['High'],
                    low=stock_historical['Low'],
                    close=stock_historical['Close']))
    st.plotly_chart(fig)

    st.markdown(""" 
    ##### Candlestick Chart""")
    # Create figure with secondary y-axis
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # include candlestick with rangeselector
    fig2.add_trace(go.Candlestick(x=stock_historical.index,
                    open=stock_historical['Open'], high=stock_historical['High'],
                    low=stock_historical['Low'], close=stock_historical['Close']),
                secondary_y=True)

    # include a go.Bar trace for volumes
    fig2.add_trace(go.Bar(x=stock_historical.index, y=stock_historical['Volume']),
                secondary_y=False)

    fig2.layout.yaxis2.showgrid=False
    st.plotly_chart(fig2,use_container_width=True)

    st.markdown(""" 
    ##### Line Chart""")
    st.write("Open")
    fig3 = go.Figure([go.Scatter(x=stock_historical.index, y=stock_historical['Open'])])
    
    st.plotly_chart(fig3,use_container_width=True)

    st.write("Close")

    fig4 = go.Figure([go.Scatter(x=stock_historical.index, y=stock_historical['Close'])])
    
    st.plotly_chart(fig4,use_container_width=True)

    


with tab2:
   st.write("Nothing yet")