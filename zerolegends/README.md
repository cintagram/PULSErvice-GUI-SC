# 제로레전드 클리어코드
BCSFE 2.7.2.3 패치방식에서 사용하는 제로레전드 스테이지 컨트롤 코드.

# 코드 설명
## count_chapters
현재 **세이브**에 세팅되어있는 챕터 수의 수를 가져온다.

쉽게말해서 세이브데이터에 전체 제로레전드 챕터 수가 몇개로 되있는지 가져온다.

버전에 따라서 수가 달라서 충돌이 날 수 있기때문에 쓴다.

## count_stages
위의 count_chapters에서 가져온 장 각각의 스테이지 수를 가져온다.

## edit_zl
coutn_chapters 함수를 사용하여 챕터 수를 가져와 사용자로부터 클리어할 스테이지의 범위를 입력 받는다.

그 후 set_zl 함수에 입력과 데이터를 패스한다.

## set_zl
제로레전드 스테이지의 클리어를 설정한다.

for 문을 사용하여 각 장에 대하여 설정하고, 각 장안에서 for문을 사용하여 스테이지를 클리어한다.

스테이지 클리어 횟수도 설정할 수 있는데, 필자는 고정값 1로 사용하였다. 원하면 바꿔보시길.

```stage_data[chapter_index]["stars"][0]["stages"][i] = 1```

*i는 for문 상수.


