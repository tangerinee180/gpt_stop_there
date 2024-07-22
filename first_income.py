
#다른 엑셀 데이터들에서 1분위 소득 추출 후 \
#데이터 프레임에 병합.
path1 = "file/1/2012_2017.xlsx"
path2 = "file/1/2018_2022.xlsx"
path3 = "file/1/2021_2023.xlsx"

df2 = pd.read_excel(path1)
df2

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
    data.rename(columns = {"시점":"year","전체.1":"first_income"},inplace=True)
    income_data = data.query('항목 == "가구소득(전년도) 평균 (만원)"')
    result = income_data[['year', 'first_income']].reset_index(drop=True) # 인덱스 정렬을 위해서 reset_index
    return result

extract_income(path1)
extract_income(path2)
extract_income(path3)
result_frame = pd.DataFrame({})


for x in path_list:
    result_frame = pd.concat([result_frame, extract_income(x)])

result_frame["year"] = result_frame["year"].astype(int) 


result_frame = result_frame.sort_values("first_income",ascending=False)\
.drop_duplicates(subset = ['year'])


temp_frame = pd.DataFrame({"year":2011,"first_income":630},index=[12])
result_frame = pd.concat([result_frame,temp_frame])\
.sort_values("year",ascending=True).reset_index(drop=True)



df = pd.merge(df,result_frame,how="left",on="year")

df.columns

df['first_income_roc'] = 0.0
for i in range(1, len(df)):\
    df.loc[i, "first_income_roc"] = ((df.loc[i, "first_income"] - df.loc[i-1, "first_income"])\
    /df.loc[i-1, "first_income"]) * 100

#실질 최저 시급 상승률, 저소득층 소득 상승률 꺾은선으로
plt.clf()

plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='year', y='min_wage_roc', label='Min Wage Change', marker='o')
sns.lineplot(data=df, x='year', y='first_income_roc', label='First Income Change', marker='o')

plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Min Wage Change vs First Income Change')
plt.legend(fontsize='small',
    markerscale=1.5,    handlelength=2,
    handleheight=2)
#handlelength = 항목 넓이 handleheight = 항목 높이
plt.show()


