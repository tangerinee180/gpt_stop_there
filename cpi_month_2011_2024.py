import pandas as pd
import numpy as np    
import matplotlib.pyplot as plt    
#파일 불러오기
df1=pd.read_csv('data/생활물가지수_2011_2014.csv', encoding='utf-8')
df1.head()
#2011-2014 월별 생활물가지수 df에 저장
cpi_2011=df1.iloc[:,[0,2]]
cpi_2011.rename(columns={'전국.1':"CPI", '시점':'date'},inplace=True)
cpi_2011.drop(index=0, inplace=True)

#파일 불러오기
df2=pd.read_csv('data/생활물가지수_2015_2024.csv', encoding='utf-8')
df2.tail()
#2015-2024.06 월별 생활물가지수 df에 저장
cpi_2015=df2.iloc[:,[0,2]]
cpi_2015.rename(columns={'전국.1':"CPI", '시점':'date'},inplace=True)
cpi_2015.drop(index=0, inplace=True)
#2024.01~2024.06 data제거
cpi_2015.drop(index=np.arange(109,115),inplace=True)

#합치기, index 재지정
cpi=pd.concat([cpi_2011,cpi_2015],axis=0,ignore_index=True)
########
 시점 = 연도/ 월 분리
cpi[['year','month']]=cpi['date'].str.split('.') #expand=True
cpi['date']=pd.to_datetime(cpi['date'])
cpi['year']=cpi['date'].dt.year
cpi['month']=cpi['date'].dt.month
#date 칼럼 삭제
cpi.drop(columns='date',inplace=True)
#######

#그래프
plt.figure(figsize=(30,25))
plt.plot(cpi['date'],cpi['CPI'])
#plt.xticks(ticks=[0,12,24,34,102,106], labels=['2022.01','2012.01','2013.01','2013-11','2019.07','2019.11'])
#plt.yticks(ticks=[0,12,24,34,102,106], labels=[cpi['CPI'][0],cpi['CPI'][12],cpi['CPI'][24],cpi['CPI'][34],cpi['CPI'][102],cpi['CPI'][106]])




plt.xlabel('year.month')
plt.ylabel('cpi')
plt.xticks(rotation=70,fontsize=4)
plt.yticks(fontsize=4)
plt.title('CPI-Month')
plt.show()

plt.clf()


