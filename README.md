# kor2num
한글 숫자 -> 아라비아 숫자로 변환해주는 함수입니다.
주소데이터에 맞게 커스터마이징 되어 있습니다.

## Usage

```python

import kor2num

print(kor2num("천오백이호"))
# >>> 1502호
print(kor2num("이만오천이백일"))
# >>> 25201
print(kor2num("둘둘이하나"))
# >>> 2221
print(kor2num("하나하나둘길"))
# >>> 112길

```

## 참고사항
해당 알고리즘은 [준성님의 Kor2num](https://github.com/codertimo/korean2num)알고리즘을 기반으로 기능 추가, 변형하여 커스터마이징하였습니다.
감사합니다.
