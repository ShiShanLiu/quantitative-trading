import pandas as pd
import numpy as np
import requests
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# chrome version above 4.11.2
# https://stackoverflow.com/questions/77111127/how-can-we-download-chromedriver-117
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def tableDetail(url: str, headers: dict) -> pd.DataFrame:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    # data = soup.select_one("#txtFinDetailData")
    data = soup.select_one("#tblDetail")
    df = pd.read_html(data.prettify())
    df = df[0]
    return df

def finDetail(url: str, headers: dict) -> pd.DataFrame:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.select_one("#divFinDetail")
    df = pd.read_html(data.prettify())
    df = df[0]
    return df

def mergeColumns(df: pd.DataFrame):
    new_columns = []
    for column in df.columns:
        column = "-".join(column)
        column = re.sub(string = column, pattern="  ", repl="")
        new_columns.append(column)
    df.columns = new_columns
    return df

class StockInfoRetriever():
    def __init__(self, stockNum, headers):
        self.stockNum = stockNum
        self.headers = headers
    
    # 獲利指標
    def stockPerformance(self):
        url = 'https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID=' + str(self.stockNum)
        df = tableDetail(url=url, headers=self.headers)
        df = mergeColumns(df=df)
        filename = str(self.stockNum) + "_獲利指標.xlsx"
        path = "goodInfo_outputs/" + filename
        df.to_excel(path, index=False)
        print("Saving is done!")
        return df

    # 現股當沖
    def dayTrading(self):
        url = "https://goodinfo.tw/tw/DayTrading.asp?STOCK_ID=" + str(self.stockNum)
        df = tableDetail(url=url, headers=self.headers)
        df = mergeColumns(df=df)
        filename = str(self.stockNum) + "_現股當沖.xlsx"
        path = "goodInfo_outputs/" + filename
        df.to_excel(path, index=False)
        print("Saving is done!")
        return df

    # 每月營收
    def monthChart(self):
        url = "https://goodinfo.tw/tw/ShowSaleMonChart.asp?STOCK_ID="  + str(self.stockNum)
        df = tableDetail(url=url, headers=self.headers)
        df = mergeColumns(df=df)
        filename = str(self.stockNum) + "_每月營收.xlsx"
        path = "goodInfo_outputs/" + filename
        df.to_excel(path, index=False)
        print("Saving is done!")
        return df

    # 財務評分
    def stockgrade(self):
        url = "https://goodinfo.tw/tw/StockFinGrade.asp?STOCK_ID="+ str(self.stockNum)
        df = finDetail(url=url, headers=self.headers)
        filename = str(self.stockNum) + "_財務評分.xlsx"
        path = "goodInfo_outputs/" + filename
        df.to_excel(path, index=False)
        print("Saving is done!")
        return df

    # 季度損益表
    def incomestatement_quarter(self):
        incomestatement_quarter_url = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=IS_M_QUAR_ACC&STOCK_ID=1785"
        df = finDetail(url=incomestatement_quarter_url, headers=self.headers)
        filename = str(self.stockNum) + "_季度損益表.xlsx"
        path = "goodInfo_outputs/" + filename
        df.to_excel(path, index=False)
        print("Saving is done!")
        return df

    # 季度資產負債表
    def balancesheet_quarter(self):
        balancesheet_quarter_url = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID=1785"
        df = finDetail(url=balancesheet_quarter_url, headers=self.headers)
        filename = str(self.stockNum) + "_季度資產負債表.xlsx"
        path = "goodInfo_outputs/" + filename
        df.to_excel(path, index=False)
        print("Saving is done!")
        return df

    # 季度現金流量表
    def cashflowsheet_quarter(self):
        cashflow_quarter_url = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=CF_M_QUAR_ACC&STOCK_ID=1785"
        df = finDetail(url=cashflow_quarter_url, headers=self.headers)
        filename = str(self.stockNum) + "_季度現金流量表.xlsx"
        path = "goodInfo_outputs/" + filename
        df.to_excel(path, index=False)
        print("Saving is done!")
        return df



if __name__=="__main__":
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie":"IS_TOUCH_DEVICE=F; SCREEN_SIZE=WIDTH=1536&HEIGHT=864; _ga=GA1.1.134640417.1718698272; __gads=ID=b42b9ba3a594ff97:T=1718698274:RT=1718698274:S=ALNI_MZ1kFXN3htHHdY3ZGXMWn10JYhrSg; __gpi=UID=00000e5315d89fdd:T=1718698274:RT=1718698274:S=ALNI_MbuXU-bLcaSUcqYleIOzqDTTFxMKw; __eoi=ID=0b4097d725162137:T=1718698274:RT=1718698274:S=AA-AfjYZbznwQCxhcZLVvPaxBsjM; CLIENT%5FID=20240618161154117%5F156%2E59%2E34%2E83; TW_STOCK_BROWSE_LIST=1785; FCNEC=%5B%5B%22AKsRol9Vv6qLdMCxvuvjU1sRPiybs9UpKWKftBn8q79OO4v-hfpBOUrtI8lvc5IyBwM6YVFPrwpug-bkB5ZnUxeYa32E4ABhLsrT0WBiN7XtnBuMv34o7xKNpJr4oHhvNFGW7d-M66kzUq0TLx_w8ci83BQW9DAuiA%3D%3D%22%5D%5D; _ga_0LP5MLQS7E=GS1.1.1718698272.1.1.1718698563.60.0.0"
    }

    tw_1880 = StockInfoRetriever(stockNum=1880, headers=headers)