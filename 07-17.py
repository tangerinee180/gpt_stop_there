import pandas as pd
import numpy as np
import matplotlib.pyplot as plt    

df = pd.read_csv("file/project.csv")
df
df.info()

# 변환계수 설정, 2011년 기준으로 변환
num=df['cpi'][0]/df['cpi'][9]
df["fixed_cpi"] = df["cpi"]/num
df.head()

#compare 열 추가
df = df.rename(columns = {"food" : "food_cpi"})
df["Compare"] = np.where(df['cpi']>df["living_cpi"],'small','big')
#year 값 앞에 두개 자르기
#필터링
df_fil=df[df['year']>=2021]


df.sort_values(["year"], ascending =[True])

df['fixed_cpi'].plot.bar(rot=0)
plt.show()
plt.clf()
df
#infla 계산
df["infla"] = 0.0

for i in range(1, len(df)):\
    df.loc[i, "infla"] = ((df.loc[i, "cpi"] - df.loc[i-1, "cpi"]) / df.loc[i-1, "cpi"]) * 100
df
# df["min_wage"].str.replace(',',"").astype(int) min_wage 숫자 다뤄야하면 사용

#다른 엑셀 데이터들에서 income 추출 후 원 데이터에 병합.
path1 = "file/1/2012_2017.xlsx"
path2 = "file/1/2018_2022.xlsx"
path3 = "file/1/2021_2023.xlsx"

#df2 = pd.read_excel(path1)
#df2
#df2.drop(0,inplace=True)
#df2.reset_index(drop=True,inplace=True)
#df2.columns

path_list = [path1,path2,path3]
result_frame = pd.DataFrame({})
def extract_income(path):
    data = pd.read_excel(path)
    data.drop(0,inplace=True)
    data.reset_index(drop=True,inplace=True)
    income_data = data[data['항목'] == '가구소득(전년도) 평균 (만원)']
    result = income_data[['시점', '전체.1']].reset_index(drop=True)
    return result

extract_income(path1)
extract_income(path2)
extract_income(path3)
result_frame = pd.DataFrame({})
for x in path_list:
    result_frame = pd.concat([result_frame, extract_income(x)],ignore_index=True)

result_frame.rename(columns = {"시점":"year","전체.1":"income"},inplace=True)
result_frame["year"] = result_frame["year"].astype(int)
result_frame = result_frame.sort_values("income",ascending=False)\
.drop_duplicates(subset = ['year'])

result_frame = result_frame.reset_index(drop=True)

result_frame
temp_frame = pd.DataFrame({"year":2011,"income":600},index=[12])
result_frame = pd.concat([result_frame,temp_frame]).sort_values("income",ascending=True)
for x in result_frame["year"] :
    print(type(x))
for x in df["min_wage"] :
    print(type(x))
result_frame
df = pd.merge(df,result_frame,how="left",on="year")
df = "main_frame"
#다른 페이지 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

before_frame = pd.read_excel("file/2/최저임금데이터_df.xlsx")
path1, path2 = ["file/2/PPP원데이터_df.xlsx","file/2/환율원데이터_df.xlsx"]
df2 = pd.read_excel(path1) 
df2.columns
df2.rename(columns = {"Reference area":"country","Unnamed: 3":"dollar_ppp"},inplace=True)
df2["dollar_ppp"] = df2["dollar_ppp"].astype(float)

names = {
"United Kingdom": 'UnitedKingdom', 'Türkiye': 'Turkiye', "New Zealand": 'NewZealand'
}
df2['country'] = df2['country'].replace(names)
for x in ['country']:
    type(x)
temp_frame2 = df2[["country","dollar_ppp"]]     
before_frame = pd.merge(before_frame,temp_frame2,how="left",on="country")


df3 = pd.read_excel(path2) 
df3.columns
df3.rename(columns = {"Reference area":"country","Unnamed: 4":"exchange_rate"},inplace=True)
df3 = df3[df3['Transaction']=="Exchange rates, average"].reset_index(drop=True)
df3["exchange_rate"] = df3["exchange_rate"].astype(float)

names = {
"United Kingdom": 'UnitedKingdom', 'Türkiye': 'Turkiye', "New Zealand": 'NewZealand'
}
df3['country'] = df3['country'].replace(names)

temp_frame3 = df3[["country","exchange_rate"]]
before_frame = pd.merge(before_frame,temp_frame3,how="left",on="country")
before_frame.loc[before_frame['country'] == 'Turkiye', 'exchange_rate'] = 33.1
oecd = before_frame
oecd
