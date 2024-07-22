'''# 실질 최저시급 상승률 추가
k=1
main_frame["min_wage_adj_up"]=main_frame["min_wage"][0]
rename=main_frame["min_wage_adj"] #너무길어서 rename으로 바꿈
while k<13:
    main_frame.loc[k,"min_wage_adj_up"]=((rename[k] - rename[k-1])/rename[k-1]) * 100
    k =k +1
main_frame.loc[0,"min_wage_adj_up"] =0
# 최저시급 상승률 추가
k=1
main_frame["min_wage_up"]=main_frame["min_wage"][0]
rename=main_frame["min_wage"] #너무길어서 rename으로 바꿈
while k<13:
    main_frame.loc[k,"min_wage_up"]=((rename[k] - rename[k-1])/rename[k-1]) * 100
    k =k +1
main_frame.loc[0,"min_wage_up"] =0
#인플레율 추가
k=1
main_frame["infla_up"]=main_frame["min_wage"][0]
rename=main_frame["fixed_cpi"] #너무길어서 rename으로 바꿈
while k<13:
    main_frame.loc[k,"infla_up"]=((rename[k] - rename[k-1])/rename[k-1]) * 100
    k =k +1
main_frame.loc[0,"infla_up"] =0
'''
