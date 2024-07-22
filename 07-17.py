import pandas as pd
import numpy as np
import matplotlib.pyplot as plt    
import seaborn as sns
df = pd.read_csv("file/project.csv")
df.head
df.info()


#식품 물가지수 column 명 변경
df = df.rename(columns = {"food" : "food_cpi"})


#cpi 2011기준으로 변환
cpi_coefficent=df['cpi'][0]/df['cpi'][9]
food_coefficent=df['food_cpi'][0]/df['food_cpi'][9]
liv_coefficent=df['living_cpi'][0]/df['living_cpi'][9]

df["cpi"] = df["cpi"]/cpi_coefficent
df["food_cpi"] = df["food_cpi"]/food_coefficent
df["living_cpi"] = df["living_cpi"]/liv_coefficent

df.head()



#inflation 계산
df["inflation"] = 0.0

for i in range(1, len(df)):\
    df.loc[i, "inflation"] = ((df.loc[i, "cpi"] - df.loc[i-1, "cpi"]) / df.loc[i-1, "cpi"]) * 100
#food inflation 계산
df['food_inflation'] = df['food_cpi'].pct_change() * 100
#df['food_inflation'] = df['food_inflation'].fillna(0)
df.loc[0,"food_inflation"] = 0
df["min_wage"] = df["min_wage"].str.replace(',',"").astype(float) 
df

### 여기에서 inf,food_inf 시각화 두개 동시에 꺾은선 그래프
plt.clf()
plt.figure(figsize=(12, 6))

sns.lineplot(data=df, x='year', y='inflation', label='Inflation', marker='o')
sns.lineplot(data=df, x='year', y='food_inflation', label='Food Inflation', marker='o')

# 레이블과 제목 설정
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Inflation vs Food Inflation Over Years')
plt.legend()

# 그래프 표시
plt.show()


#다른 엑셀 데이터들에서 income 추출 후 원 데이터에 병합.
path1 = "file/1/2012_2017.xlsx"
path2 = "file/1/2018_2022.xlsx"
path3 = "file/1/2021_2023.xlsx"

#df2 = pd.read_excel(path1)
#df2
#df2.drop(0,inplace=True)
#df2.reset_index(drop=True,inplace=True)
#df2.columns

#함수 만들기 위해 경로 리스트 형성
path_list = [path1,path2,path3]

#
def extract_income(path):
    data = pd.read_excel(path)
    data.drop(0,inplace=True)
    data.reset_index(drop=True,inplace=True)
    income_data = data[data['항목'] == '가구소득(전년도) 평균 (만원)']
    result = income_data[['시점', '전체.1']].reset_index(drop=True) # 인덱스 정렬을 위해서 reset_index
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
temp_frame = pd.DataFrame({"year":2011,"income":630},index=[12])
result_frame = pd.concat([result_frame,temp_frame]).sort_values("year",ascending=True).reset_index(drop=True)
for x in result_frame["year"] :
    print(type(x))
for x in df["min_wage"] :
    print(type(x))
result_frame
df = pd.merge(df,result_frame,how="left",on="year")

df.rename(columns = {"income":"first_income"},inplace=True)
main_frame = df

# 인플레 조정계수 추가
k=1
main_frame["infla_adj"]=main_frame["cpi"][0]
while k<13:
    main_frame.loc[k,"infla_adj"]=(main_frame["cpi"][0]/main_frame["cpi"][k])
    k =k +1
# 실질 최저시급 추가
 
k=1
main_frame["min_wage_adj"]=main_frame["min_wage"][0]
while k<13:
    main_frame.loc[k,"min_wage_adj"]=(main_frame["min_wage"][k] * main_frame["infla_adj"][k])
    k =k +1
def up(e,b,c):
    k=1
    main_frame[b]=main_frame["min_wage"][0]
    rename=main_frame[e] #너무길어서 rename으로 바꿈
    while k<13:
        main_frame.loc[k,b]=((rename[k] - rename[k-1])/rename[k-1]) * 100
        k =k +1
    main_frame.loc[0,b] =0
    return main_frame[b]
up("min_wage_adj","min_wage_adj_up",main_frame) # 실질 최저시급 상승률 추가
up("min_wage","min_wage_up",main_frame) # 최저시급 상승률 추가
up("cpi","infla_up",main_frame)   #인플레율 추가 
#pct_change()

main_frame['first_income_up'] = 0.0
main_frame['first_income_up'] = main_frame['first_income'].pct_change() * 100
df['first_income_up'] = df['first_income_up'].fillna(0)
for i in range(1, len(df)):
    main_frame.loc[i, 'first_income_up'] = ((main_frame.loc[i, 'first_income'] - main_frame.loc[i-1, 'first_income']) / main_frame.loc[i-1, 'first_income']) * 100

type(main_frame["min_wage_adj_up"][0])

main_frame

#실질 최저 시급 상승률, 저소득층 소득 상승률 꺾은선으로
plt.clf()
plt.figure(figsize=(12, 6))

sns.lineplot(data=df, x='year', y='min_wage_adj_up', label='Min Wage Change', marker='o')
sns.lineplot(data=df, x='year', y='first_income_up', label='First Income Change', marker='o')

plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Min Wage Change versus First Income Change')
plt.legend(fontsize='small',
    markerscale=1.5,    handlelength=2,         # 항목 길이
    handleheight=2         # 항목 높이)
plt.show()


plt.clf()
#실질 최저 시급 상승률, 인플레이션 상승률 꺾은선으로

plt.clf()
plt.figure(figsize=(12, 6))

sns.lineplot(data=df, x='year', y='min_wage_adj_up', label='Min Wage Change', marker='o')
sns.lineplot(data=df, x='year', y='infla_up', label='Inflation Change', marker='o')

plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Min Wage Change versus Inflation Change')
plt.legend(fontsize='small',
    markerscale=1.5,    handlelength=2,         # 항목 길이
    handleheight=2)         # 항목 높이
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
#환율/ppp
oecd["coefficient"] = oecd["exchange_rate"]/oecd["dollar_ppp"]
oecd["real_wage"] = oecd["min_wage"]*oecd["coefficient"]

oecd
# bar 그래프
plt.clf()

plt.figure(figsize=(14, 8))
#case1
""""
bar_colors = []
for country in df['country']:
    if country == 'Korea':
        bar_colors.append('red')
    else:
        bar_colors.append('blue')
sns.barplot(x='country', y='real_wage', data=df, palette=bar_colors)
"""
#case2
oecd['color'] = np.where(oecd['country'] == 'Korea', 'red', 'blue')
plt.figure(figsize=(14, 8))
sns.barplot(x='country', y='real_wage', data=oecd, palette=oecd['color'].tolist())

plt.xticks(rotation = 270, ha='right')
plt.xlabel('Country')
plt.ylabel('Real Wage')
plt.title('Real Wage by Country (Bar Plot)')
plt.tight_layout()
##plt.subplots_adjust(bottom=0.5)
plt.show()

plt.close()


#scatter 그래프
# case1
plt.figure(figsize=(14, 8))
oecd['color'] = np.where(oecd['country'] == 'Korea', 'red', 'blue')
sns.scatterplot(x='country', y='real_wage', data=oecd, hue='country', palette=oecd['color'].tolist(),\
s=100, legend=False)
# case2
plt.figure(figsize=(14, 8))
palette_colors = ['red' if country == 'Korea' else 'blue' for country in df['country']]
sns.scatterplot(x='country', y='real_wage', data=df, hue='country', palette=bar_colors, s=100, legend=False)

plt.xticks(rotation=45, ha='right')
plt.xlabel('Country')
plt.ylabel('Real Wage')
plt.title('Real Wage by Country (Scatter Plot)')
plt.show()

plt.clf()
