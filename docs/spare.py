---
title: "최저 임금 데이터 분석"
jupyter: python3
---

### 최저 임금 데이터 분석

홈페이지 구성-

```{python}
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt    
import seaborn as sns

plt.rcParams.update({"figure.dpi": 150,
                     "figure.figsize": [8, 6],
                     "font.size": 11,
                     "font.family": "Malgun Gothic"})

intro = pd.read_excel("file/소비자동향조사.xlsx")
plt.figure(figsize = [5.5,4])
intro["year"]
sns.lineplot(data=intro, x='year', y='임금수준전망', color='dodgerblue', label='임금수준전망', marker='o')
sns.lineplot(data=intro, x='year', y='향후경기전망', color='salmon', label='향후경기전망', marker='o')
sns.lineplot(data=intro, x='year', y='현재경기판단', color='red', label='현재경기판단', marker='o')
plt.xlabel('Year',fontsize=14)
plt.ylabel('Percentage(%)',fontsize=14)
plt.title("소비자동향조사")
plt.legend(loc = "lower right")
plt.grid()
plt.show()
```

**소비자동향조사에 따르면, 소비자들은 경기를 부정적으로 판단하고 있는데, 그에 반해 임금 수준은 상승할 것이라고 예상한다. 그렇다면 임금은 정말 지속적으로 상승했는지, 소비자들이 임금 상승의 수혜를 제대로 받고 있는지 알아보기 위해 임금 데이터를 바탕으로 분석을 진행하고자 하였다. **

### 우리가 사용한 데이터와 수치들
<img src="./4.PNG" alt="Description" width="500" height="500">
![](./1.PNG)
![](./2.PNG)
![](./3.PNG)


발표 순서


* **CPI: 소비자물가지수란?**

***
![](./CPI.PNG)

CPI(소비자 물가 지수) :
소비자들이 일상 생활에서 구매하는 상품과 서비스의 가격 변동을 측정하는 지표이다. 그 측정을 위해 다양한 소비자 Basket을 사용하며, 일반적인 CPI의 Basket엔 식품, 주택, 의류, 교통, 교육, 의료 등 모든 상품과 서비스가 포함된다. 예시로 식품 물가 지수의 Basket 안엔 음식만 들어가있다고 보면 된다.
        



***
### 한국의 최저임금이 OECD의 다른 나라와 비교하면 어떨까?
OECD별 최저 시급 데이터가 있지만, 각 나라의 물가가 반영이 안 된 지표이기에  환율과 PPP 데이터를 사용하였다. * **다른 나라와 한국의 실질 최저 임금을 비교하기 위해서 (환율/PPP)를 변환 계수로 사용해 최저시급 (달러)에 곱하여, 각 나라 간 비교할 수 있는 실질 임금 지표를 만들었다.**


**

### PPP란?
**PPP는 구매력 평가라는 뜻으로, 실질 구매력을 나타내는 지표이다.**
**예를 들어 한국의 dollar PPP는 미국에서 1달러를 가지고 살 수 있는 상품을 한국에서 살 때 드는 금액으로 정의할 수 있다.**
예를 들어 환율이 1300이라면 미국에서 1달러를 가지고 살 수 있는 basket을 한국에서 살 때는 1300원이 든다는 뜻이지만, PPP가 800이라면 각 국가의 비교시, 미국에서 1달러를 가지고 살 수 있는 basket을 한국에서 살 때는 실질적으로 800원이 든다는 듯이다.


## OECD 국가 별 최저시급
* 칼럼 확인
```{python}
before_frame = pd.read_excel("file/2/최저임금데이터_df.xlsx")
path1, path2 = ["file/2/PPP원데이터_df.xlsx","file/2/환율원데이터_df.xlsx"]
df2 = pd.read_excel(path1) 
df2
```

* 추가 데이터 병합 및 열 지정 (1)
```{python}
df2.rename(columns = {"Reference area":"country","Unnamed: 3":"dollar_ppp"},inplace=True)
df2["dollar_ppp"] = df2["dollar_ppp"].astype(float)

names = {
"United Kingdom": 'UnitedKingdom', 'Türkiye': 'Turkiye', "New Zealand": 'NewZealand'
}
df2['country'] = df2['country'].replace(names)

temp_frame2 = df2[["country","dollar_ppp"]]     
before_frame = pd.merge(before_frame,temp_frame2,how="left",on="country")
before_frame.head()
```

* 추가 데이터 병합 및 열 지정 (2)
```{python}

df3 = pd.read_excel(path2) 
df3.rename(columns = {"Reference area":"country","Unnamed: 4":"exchange_rate"},inplace=True)
df3 = df3[df3['Transaction']=="Exchange rates, average"].reset_index(drop=True)
df3["exchange_rate"] = df3["exchange_rate"].astype(float)

df3['country'] = df3['country'].replace(names)

temp_frame3 = df3[["country","exchange_rate"]]
oecd = pd.merge(before_frame,temp_frame3,how="left",on="country")
oecd.loc[oecd['country'] == 'Turkiye', 'exchange_rate'] = 33.1
oecd.head()
```


* **다른 나라와 한국의 실질 최저 임금을 비교하기 위해서 (환율/PPP)를 변환 계수로 사용해 최저시급 (달러)에 곱하여, 각 나라 간 비교할 수 있는 실질 임금 지표를 만들었다.**

* 환율/ PPP 열 추가
```{python}
oecd["coefficient"] = oecd["exchange_rate"]/oecd["dollar_ppp"]
oecd["real_wage"] = oecd["min_wage"]*oecd["coefficient"]

oecd.head()
```

* OECD 국가별 최저임금 비교 
```{python}
#| messeage: false
#| warning: false 
oecd = oecd.sort_values("real_wage",ascending=True).reset_index(drop=True)
plt.clf()
plt.figure(figsize=(8,4))
bar_colors = np.where(oecd["country"]=="Korea","red","dodgerblue")
sns.barplot(data=oecd.sort_values("real_wage",ascending=True), \
x='country', y='real_wage', palette=bar_colors)

plt.xticks(rotation=45, fontsize=6)  # 글씨 크기와 회전 각도 조정
plt.yticks(fontsize=12)
plt.xlabel('Country',fontsize=14)  # 축 제목 글씨 크기 조정
plt.ylabel('Real Wage',fontsize=14)  # 축 제목 글씨 크기 조정
plt.title('OECD 국가별 실질 최저임금', fontsize=20)  # 제목 글씨 크기 조정
plt.legend()
plt.show()
```

* **상대적인 비교를 위해 OECD 실질 임금의 평균을 구하여 그래프에 추가하는 작업을 진행하였다.**



### OECD 평균 임금 추가한 그래프

```{python}
#| messeage: false
#| warning: false 

mean1 = oecd["real_wage"].mean()
#country 에 평균 임금을 추가.
frame = pd.DataFrame({"country":'Mean',"real_wage":mean1},index=[0])
oecd1 = pd.concat([oecd,frame])
oecd1 = oecd1.sort_values("real_wage",ascending=True).reset_index(drop=True)

```

* 
```{python}
#| messeage: false
#| warning: false 
#| eval: false
#Mean,Korea 색 다르게 하기
bar_colors = np.where(oecd1["country"]=="Korea","red",np.where(oecd1["country"]=="Mean","seagreen","dodgerblue"))

sns.barplot(data=oecd1.sort_values("real_wage",ascending=True),\
x='country', y='real_wage', palette=bar_colors)

plt.xlabel('Country',fontsize=14)  # 축 제목 글씨 크기 조정
plt.ylabel('Real Wage',fontsize=14)  # 축 제목 글씨 크기 조정
plt.title('OECD 주요국가별 실질 최저임금', fontsize=20)  # 제목 글씨 크기 조정
```

*
```{python}
oecd1["country"]
```

*
```{python}
#| messeage: false
#| warning: false 
#| eval: false
show_country_label = [0,3,7,9,11,13,14,16,18,20,22,24,27]

show_country = ['Mexico', 'Hungary', 'United States', 'Poland', 'Portugal', 'Mean','Japan', 'Korea', 'Canada', 'Spain',\
'United Kingdom', 'Germany', 'France']

plt.xticks(rotation=45, fontsize=10, ticks = show_country_label,labels =show_country )  # 글씨 크기와 회전 각도 조정
plt.yticks(fontsize=12)

plt.show()
```



## OECD 주요 국가의 평균 실질 임금 그래프

```{python}
#| messeage: false
#| warning: false 

mean1 = oecd["real_wage"].mean()
frame = pd.DataFrame({"country":'Mean',"real_wage":mean1},index=[0])
oecd1 = pd.concat([oecd,frame])
oecd1 = oecd1.sort_values("real_wage",ascending=True).reset_index(drop=True)
plt.figure(figsize=(5.5,4))

bar_colors = np.where(oecd1["country"]=="Korea","red",np.where(oecd1["country"]=="Mean","seagreen","dodgerblue"))

sns.barplot(data=oecd1.sort_values("real_wage",ascending=True),\
x='country', y='real_wage', palette=bar_colors)

plt.xlabel('Country',fontsize=14)  # 축 제목 글씨 크기 조정
plt.ylabel('Real Wage',fontsize=14)  # 축 제목 글씨 크기 조정
plt.title('OECD 주요국가별 실질 최저임금', fontsize=20)  # 제목 글씨 크기 조정
show_country_label = [0,3,7,9,11,13,14,16,18,20,22,24,27]

show_country = ['Mexico', 'Hungary', 'United States', 'Poland', 'Portugal', 'Mean','Japan', 'Korea', 'Canada', 'Spain',\
'United Kingdom', 'Germany', 'France']

plt.xticks(rotation=45, fontsize=10, ticks = show_country_label,labels =show_country )  # 글씨 크기와 회전 각도 조정
plt.yticks(fontsize=12)

plt.show()

```

* **우리나라의 실질 최저 임금이 OECD 평균보다 높다는 것으로, 한국의 최저 임금이 타 국가들과 비교해서 높은 편인 것을 알 수 있다. **


***     
# **결론**
<span style="font-size:125%">
<span style="background-color:#fff5b1">
**1)인플레이션의 영향으로 최저시급 상승률에 비해 실질 최저시급 상승률이 낮다.** </span></span>

**-> 최저 임금을 인상하는 만큼 그대로 소비자에게 전달되지 않는다.**


<span style="font-size:125%">  
<span style="background-color:#fff5b1">
**2) 실질 물가 상승은 일반 소비자에게 더 크게 다가온다.**    </span></span>

**-> 물가 상승시, 음식과 같은 필수재들의 물가는 소비자들에게 더 크게 다가올 수 있다.**
<br/><br/>

            
<span style="font-size:125%">  <span style="background-color:#fff5b1">
**3) 우리나라의 최저 임금은 OECD 내에서도 평균 이상이기 때문에, 최저임금의 대폭 인상은 바람직하지 않다.**  </span>
</span>
              


<span style="font-size:110%">  
**최저 시급의 대폭 인상은 인플레이션과 고용시장에의 부정적 영향 등의 부작용을 동반한다**<br/>
**최저임금 상승의 목적인 근로자의 소득 수준 상승과 그에 따른 소비 여력의 증가로 인한 경제 활성화는 노동, 복지 등의 다른 관점에서 접근하는 것이 유리할 수 있다.**
</span>
