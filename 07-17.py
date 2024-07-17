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
