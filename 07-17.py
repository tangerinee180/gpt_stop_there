import pandas as pd
import numpy as np
import matplotlib.pyplot as plt    
import seaborn as sns

df = pd.read_excel("file/cpi_2011to2023.xlsx")
df.head

df.rename(columns = {'시점':"year","전국" : "cpi"\
,"전국.2":"food_cpi"},inplace=True)
df.drop(0,inplace=True) #inplace = True 설명
df=df[['year','cpi','food_cpi']]
df.reset_index(drop=True,inplace=True)#선생님한테 물어보기
list = ["4,320","4,580","4,860","5,210","5,580","6,030",\
"6,470","7,530","8,350","8,590","8,720","9,160","9,620"]
df['min_wage'] = np.array(list)
df = df[['year',"min_wage", 'cpi', 'food_cpi']]
type(df["min_wage"][0])
for i in df["year"]:
    print(type(i))
df["min_wage"] = df["min_wage"].str.replace(',',"").astype(int) 
df["year"] = df["year"].astype(int) 

#cpi 2011기준으로 변환
cpi_coefficent=df['cpi'][0]/df['cpi'][9]
food_coefficent=df['food_cpi'][0]/df['food_cpi'][9]

df["cpi"] = df["cpi"]/cpi_coefficent
df["food_cpi"] = df["food_cpi"]/food_coefficent

df.head()



#inflation 계산
df["inflation"] = 0.0

for i in range(1, len(df)):\
    df.loc[i, "inflation"] = ((df.loc[i, "cpi"] - df.loc[i-1, "cpi"])\
    /df.loc[i-1, "cpi"]) * 100
df
#food inflation 계산
df['food_inflation'] = 0
for i in range(1, len(df)):\
    df.loc[i, "food_inflation"] = ((df.loc[i, "food_cpi"] - df.loc[i-1, "food_cpi"])\
    /df.loc[i-1, "food_cpi"]) * 100
#df['food_inflation'] = df['food_inflation'].fillna(0)

df

### 여기에서 inf,food_inf 시각화 두개 동시에 꺾은선 그래프
plt.clf()
sns.lineplot(data=df, x='year', y='inflation',color='red',label='Inflation', marker='o')
sns.lineplot(data=df, x='year', y='food_inflation',color='blue' ,label='Food Inflation', marker='o')
#percentage, 년도 수정
# 레이블과 제목 설정
plt.xticks(rotation = 0)
plt.xlabel('Year')
plt.ylabel('Percentage(%)')
plt.title('Inflation vs Food Inflation Over Years')
plt.legend()

# 그래프 표시
plt.show()

#인플레 조정 계수
infla_adj = np.array(100/df['cpi'])

df['real_wage'] = (df['min_wage'] / df['cpi']) * 100
df['real_wage'] = df['real_wage'].astype(int)

df["real_wage_roc"] = 0
for i in range(1, len(df)):\
    df.loc[i, "real_wage_roc"] = ((df.loc[i, "real_wage"] - df.loc[i-1, "real_wage"])\
    /df.loc[i-1, "real_wage"]) * 100
df["min_wage_roc"] = 0
for i in range(1, len(df)):\
    df.loc[i, "min_wage_roc"] = ((df.loc[i, "min_wage"] - df.loc[i-1, "min_wage"])\
    /df.loc[i-1, "min_wage"]) * 100

df = df[['year', 'min_wage','real_wage',"min_wage_roc","real_wage_roc", 'cpi', 'food_cpi', 'inflation', 'food_inflation',]]


### 여기에서 roc 두개 시각화 꺾은선 그래프
plt.clf()
sns.lineplot(data=df, x='year', y='min_wage_roc',color='red',label='Min Wage ROC', marker='o')
sns.lineplot(data=df, x='year', y='real_wage_roc',color='blue' ,label='Real Wage ROC', marker='o')
#percentage, 년도 수정
# 레이블과 제목 설정
plt.xticks(rotation = 0)
plt.xlabel('Year')
plt.ylabel('Percentage(%)')
plt.ylim(-2, 17)
plt.grid()
plt.title('Min Wage ROC vs Real Wage ROC Over Years')
plt.legend()
plt.show()

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
#환율/ppp
oecd["coefficient"] = oecd["exchange_rate"]/oecd["dollar_ppp"]
oecd["real_wage"] = oecd["min_wage"]*oecd["coefficient"]

oecd



#bar 그래프 == 
oecd

bar_colors = ['red' if country == 'Korea' else 'blue' for country in oecd['country']]
#리스트 컴프리핸션 구문 순서

plt.figure(figsize=(14, 8))
sns.barplot(data=oecd.sort_values("real_wage",ascending=True), \
x='country', y='real_wage', palette=bar_colors)

plt.xticks(rotation=45, ha='right', fontsize=6)  # 글씨 크기와 회전 각도 조정
plt.xlabel('Country', fontsize=12)  # 축 제목 글씨 크기 조정
plt.ylabel('Real Wage', fontsize=12)  # 축 제목 글씨 크기 조정
plt.title('Real Wage by Country (Bar Plot)', fontsize=14)  # 제목 글씨 크기 조정
plt.show()




### mean 값 추가 bar
mean1 = oecd["real_wage"].mean()
frame = pd.DataFrame({"country":'Mean',"real_wage":mean1},index=[0])
oecd1 = pd.concat([oecd,frame])
oecd1["country"]
oecd1 = oecd1.sort_values("real_wage",ascending=True).reset_index(drop=True)
bar_colors = ['red' if country == 'Korea' else 'blue' for country in oecd['country']]
bar_colors.insert(11,"green")

plt.figure(figsize=(14, 8))
sns.barplot(data=oecd1.sort_values("real_wage",ascending=True), \
x='country', y='real_wage', palette=bar_colors)
show_country_label = [0,3,7,9,11,13,14,16,18,20,22,24,27]
show_country = ['Mexico', 'Hungary', 'United States', 'Poland', 'Portugal', 'Mean',\
'Japan', 'Korea', 'Canada', 'Spain', 'United Kingdom', 'Germany', 'France',]
plt.xticks(rotation=45, ha='right', fontsize=6, ticks = show_country_label,labels =show_country )  # 글씨 크기와 회전 각도 조정
plt.xlabel('Country', fontsize=12)  # 축 제목 글씨 크기 조정
plt.ylabel('Real Wage', fontsize=12)  # 축 제목 글씨 크기 조정
plt.title('Real Wage by Country (Bar Plot)', fontsize=14)  # 제목 글씨 크기 조정
plt.subplots_adjust(bottom=0.2) # 하단 레이블 간격 조정
plt.show()
