import requests
import pandas as pd



# https://www.finlab.tw/python%EF%BC%9A%E5%A6%82%E4%BD%95%E7%8D%B2%E5%BE%97%E4%B8%8A%E5%B8%82%E4%B8%8A%E6%AB%83%E8%82%A1%E7%A5%A8%E6%B8%85%E5%96%AE/

if __name__=="__main__":
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie":"IS_TOUCH_DEVICE=F; SCREEN_SIZE=WIDTH=1536&HEIGHT=864; _ga=GA1.1.134640417.1718698272; __gads=ID=b42b9ba3a594ff97:T=1718698274:RT=1718698274:S=ALNI_MZ1kFXN3htHHdY3ZGXMWn10JYhrSg; __gpi=UID=00000e5315d89fdd:T=1718698274:RT=1718698274:S=ALNI_MbuXU-bLcaSUcqYleIOzqDTTFxMKw; __eoi=ID=0b4097d725162137:T=1718698274:RT=1718698274:S=AA-AfjYZbznwQCxhcZLVvPaxBsjM; CLIENT%5FID=20240618161154117%5F156%2E59%2E34%2E83; TW_STOCK_BROWSE_LIST=1785; FCNEC=%5B%5B%22AKsRol9Vv6qLdMCxvuvjU1sRPiybs9UpKWKftBn8q79OO4v-hfpBOUrtI8lvc5IyBwM6YVFPrwpug-bkB5ZnUxeYa32E4ABhLsrT0WBiN7XtnBuMv34o7xKNpJr4oHhvNFGW7d-M66kzUq0TLx_w8ci83BQW9DAuiA%3D%3D%22%5D%5D; _ga_0LP5MLQS7E=GS1.1.1718698272.1.1.1718698563.60.0.0"
    }

    url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    response = requests.get(url=url, headers=headers)
    df = pd.read_html(response.text)[0]
    df.columns = df.iloc[0]
    df = df.iloc[2:]
    df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
    df["code"] = df.有價證券代號及名稱.str.split(expand=True)[0]
    df["name"] = df.有價證券代號及名稱.str.split(expand=True)[1]
    df = df[["code", "name", "上市日", "市場別", "產業別"]]
    df = df.rename(columns={"上市日": "release date", "市場別": "market type", "產業別": "industry type"})
    df.to_csv("stocknumbers/TWstockNums.csv", index=False, encoding="UTF-8")
    print("Done!")