#!/usr/bin/env python
# coding: utf-8

# In[63]:


import json
import math

## 규칙 단어들 소환하기
with open('./pattern.json', 'r',encoding='utf-8') as e:
    config2 = json.load(e)
rule_word = config2['pattern_word']['rule_word']
numbers_list1 = config2['pattern_word']['numbers_list1']
numbers_list2 = config2['pattern_word']['numbers_list2']
numbers1 = config2['pattern_word']['numbers1']
numbers2 = config2['pattern_word']['numbers2']


# In[105]:


## 한글 숫자 -> 아라비아 숫자로 변환해주는 함수 

def kor2num(korean_num):
    decode_result = []
    result = 0
    temp_result = 0
    index = 0
    count = 0
    if '만' == korean_num[0]: korean_num = '일' + korean_num
    ## 숫자 서열 어긋나는거 제외(백천동)
    if len(korean_num) >= 2 and korean_num[0] == '백' and korean_num[1] == '천':
        return ('변환 불가')
    ## 숫자가 포함되어있지 않은 단어는 이스케이프 - (숫자로만 구성된 단어를 파악하기 위해 count 변수 삽입)
    for z in range(len(korean_num)):
        if korean_num[z:z+2] in numbers_list2:
            count += 2
    count += len(list(filter(lambda x: x in numbers_list1,list(korean_num))))
    if count == 0: 
        return ('변환 불가')
    ## 규칙단어, 숫자 제외 후 다른 단어가 있을 경우 이스케이프
    a = korean_num; a = a.replace(' ','')
    for rule1 in rule_word:
        ## 천호동, 일호동, 동구 등을 숫자로 안바꾸게
        if korean_num[-1] == '동' and rule1 in korean_num[-2]:
            return ('변환 불가')
        ## 동일로
        if len(korean_num) >= 3 and korean_num[0] in rule_word and korean_num[-1] in rule_word:
            return ('변환 불가')
        if rule1 in a:
            a = a.replace(rule1,'x')
    for num1 in numbers_list1:
        if num1 in a:
            a = a.replace(num1,'x')
    a = a.replace('x','')
    if len(a) != 0:
        return ('변환 불가')
    
    ## 백, 십, 천, 만이 들어가 있는 한글 숫자 일 경우
    if '만' in korean_num or '백' in korean_num or '십' in korean_num or '천' in korean_num or '열' in korean_num:
        wow = ''
        for rule in rule_word:
            ### 2가지 or 조건 -> 1. 한글 숫자가 포함되어있고 특정단어가 들어간 경우 or 2. 한글 숫자로만 구성된 단어
            if (len(rule) == 1 and rule in korean_num[-1:]) or (len(rule) == 2 and rule in korean_num[-2:]) or count >= len(korean_num):
                wow = rule
                while index < len(korean_num):
                    for number, true_value in numbers1:
                        if index + len(number) <= len(korean_num):
                            if korean_num[index:index + len(number)] == number:
                                decode_result.append((true_value, math.log10(true_value).is_integer()))
                                # 단어가 2글자인 경우 인덱싱 오류가 나기 때문에 for문을 나가야함
                                if len(number) == 2:
                                    index += 1
                                break
                    index += 1  
                for index, (number, is_natural) in enumerate(decode_result):
                    #해당단어가 십,백,천에 속하는 단어이면
                    if is_natural:
                        if math.log10(number) > 3 and (math.log10(number) - 4) % 4 == 0:
                            result += temp_result * number
                            temp_result = 0
                        # 앞글자가 있다면
                        elif index - 1 >= 0:
                            #앞글자가 십, 백, 천이 아니면
                            if not decode_result[index - 1][1]:
                                # 앞글자 곱하기 (십,백,천)
                                temp_result += number * decode_result[index - 1][0]
                            #앞글자가 십, 백, 천이면 그냥 더하기
                            else:
                                temp_result += number
                        # 앞글자가 없는 경우라면 그냥 넘버를 더한다
                        else:
                            temp_result += number
                    #해당단어가 한자리수 단어이면
                    else:
                        # 마지막 자리에 있는 수라면 그냥 더하기
                        if index + 1 == len(decode_result):
                            temp_result += number
                        # 뒷 글자가 한자리 수라면 더하기
                        elif not decode_result[index + 1][1]:
                            temp_result += number
                        # 뒷글자가 10000이상일 경우
                        elif math.log10(decode_result[index + 1][0]) > 3 and (math.log10(decode_result[index + 1][0]) - 4) % 4 == 0:
                            temp_result += number
                result += temp_result
                
                ###### 한글 숫자로만 구성된 것과 규칙에 따른 것과의 구분
                if wow in korean_num:
                    return (str(result)+wow)
                else:
                    return (str(result))
                
    ## 만, 백, 십, 천이 없는, 숫자체계를 따르지 않을 경우 
    else:
        for rule in rule_word:
            ### 2가지 or 조건 -> 1. 한글 숫자가 포함되어있고 특정단어가 들어간 경우 or 2. 한글 숫자로만 구성된 단어
            if (len(rule) == 1 and rule in korean_num[-1]) or (len(rule) == 2 and rule in korean_num[-2:]) or count >= len(korean_num):
                for j in range(len(numbers2)):
                    if numbers2[j][0] in korean_num:
                        korean_num = korean_num.replace(numbers2[j][0],str(numbers2[j][1]))   
                return korean_num

