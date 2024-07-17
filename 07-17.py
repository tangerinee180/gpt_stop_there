import pandas as pd
import numpy as np
import matplotlib.pyplot as plt    

df = pd.read_csv("project.csv")
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
df_fil
df

df.sort_values(["year"], ascending =[True])

df['fixed_cpi'].plot.bar(rot=0)
plt.show()
plt.clf()
df
#infla 계산
adf["infla"] = 0.0
for i in range(1, len(df)):\
    df.loc[i, "infla"] = ((df.loc[i, "cpi"] - df.loc[i-1, "cpi"]) / df.loc[i-1, "cpi"]) * 100
df

path1 = "file/2012_2017.xlsx"
path2 = "file/2018_2022.xlsx"
path3 = "file/2021_2023.xlsx"

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
result_frame = result_frame.sort_values("income",ascending=True).reset_index(drop=True)\
.drop_duplicates(subset = ['year'])
