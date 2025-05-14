'''
from random import sample
import random
from datetime import datetime
from collections import Counter

#랜덤한 광물 무게 5개
weights=sample(range(1,10),2)+sample(range(11,21),2)+[10]
#순서 섞음
random.shuffle(weights)
name=['빨강','노랑','초록','파랑','보라']
dictionary = dict(zip(name, weights))
Tdictionary = dict(zip(weights, name))

#저울
mainleft=dict(빨강=0,노랑=0,초록=0,파랑=0,보라=0)
mainright=dict(빨강=0,노랑=0,초록=0,파랑=0,보라=0)
assisleft=dict(빨강=0,노랑=0,초록=0,파랑=0,보라=0)
assisright=dict(빨강=0,노랑=0,초록=0,파랑=0,보라=0)

#플레이어수
players=7
playerlist = list(range(1, players + 1))
#각플레이어 보유 광물
mineral={}
for player in range(1,players+1):
    mineral[player]=dict(빨강=2,노랑=2,초록=2,파랑=2,보라=2)

# ===================================================================
print("오늘의 상금매치는 양팔저울입니다")
print("양팔저울은 무게가 다른 광물들을 양팔저울에 올려 균형을 맞추고")
print("각 광물의 무게를 모두 알아내야하는 게임입니다")
print("플레이어들에게는 빨강 노랑 초록 파랑 보라 다섯가지 색깔의 광물이 각각 두개씩 총 열개가 지급됩니다")
print("각 광물의 무게는 1g이상 20g이하이며 자연수입니다")
print('게임시작시 이 중 하나의 색깔의 광물에 대한 정보가 주어집니다')
print("플레이어들은 보유한 광물들을 저울에 올려 그 결과를 단서로 저울에 균형을 맞추고 각 광물의 무게도 정확히 유추해내야 합니다")
print("양팔저울은 메인저울과 보조저울이 준비되어 있습니다")
print("메인저울은 플레이어들이 광물을 올려 최종적으로 균형을 맞춰야하는 저울입니다")
print("보조저울은 추가적으로 계산에 활용할 수 있는 저울로 보조저울의 균형은 맞추지 않아도 됩니다")
print("자신의 차례에 최소 2개의 광물을 제한시간 5분안에 저울에 올려야 합니다")
print("동시에 두개의 저울을 모두 사용할수있으며 하나의 저울만 사용해도 됩니다")
print("이때 광물을 올린 결과 메인저울의 양쪽 광물 구성이 같아서는 안됩니다")
print("한번 올린 광물은 다시 회수할 수 없으며 저울에 계속 누적됩니다")
print("메인저울에 균형이 맞춰지면 자신의 피스 한개를 내고 각 광물의 무게를 맞힐 수 있습니다")
print("정답을 모두 맞혔다면 상금매치에 성공하고 정답을 맞힌 플레이어는 보상으로 피스 2개를 획득합니다.")
print("광물을 모두 소진하거나 한개만 남은 플레이어는 더 이상 광물을 저울에 올릴 수 없으며 정답을 맞힐 기회도 없습니다")
print("모든 플레이어가 더 이상 광물을 저울에 올릴 수 없다면 게임은 그즉시 종료됩니다")
print(f'{Tdictionary[10]}는 3번째로 무겁고 의 무게는 10g 입니다')

flag=0
while flag<players:
    serviveplayerlist=playerlist.copy()
    for player in serviveplayerlist:
        print('')
        print(f'{player}번플레이어 제한시간 5분안에 최소 2개의 광물을 저울에 올려주십시오')
        now=datetime.now().strftime('%H:%M:%S')
        print(f'현재시간은 {now} 입니다')
        while True:
            count=0
            print(f'현재보유광물 {mineral[player]}')
            print("입력예시 : 빨강,노랑  해당저울에 올리지 않을 경우 엔터")
            ml=input("메인저울왼쪽 입력 : ").split(',')
            mr=input("메인저울오른쪽 입력 : ").split(',')
            al=input("보조저울왼쪽 입력 : ").split(',')
            ar=input("보조저울오른쪽 입력 : ").split(',')
            uselist=[]
            for i in [ml,mr,al,ar]:
                if i!=['']:
                    count+=len(i)
                    uselist+=i
            if count>=2:
                use_dict = dict(Counter(uselist))
                invalid_colors = [key for key in list(use_dict.keys()) if key not in name]
                if len(invalid_colors)==0:
                    remain_mineral=mineral[player].copy()
                    for key in remain_mineral:
                        if key in use_dict:
                            remain_mineral[key] -= use_dict[key]
                            
                    if any(value < 0 for value in remain_mineral.values()):
                        print("")
                        print("사용가능한 광물의 숫자를 초과하였습니다")
                    else :
                        templeft=mainleft.copy()
                        tempright=mainright.copy()
                        if ml!=['']:
                            for color in ml:
                                templeft[color]+=1
                        if mr!=['']:
                            for color in mr:
                                tempright[color]+=1
                        if templeft!=tempright:
                            break
                        else :
                            print("")
                            print('메인저울 양쪽의 광물구성이 같습니다')
                else :
                    print("")
                    print("잘못된 광물을 입력하셨습니다")
            else :
                print("")
                print(f'{count}개의 광물을 올리셨습니다 최소 2개의 광물을 저울에 올려야 합니다')
        mainleft=templeft.copy()
        mainright=tempright.copy()
        if al!=['']:
            for color in al:
                assisleft[color]+=1
        if ar!=['']:
            for color in ar:
                assisright[color]+=1
        mainleftweight=mainleft['빨강']*dictionary['빨강']+mainleft['노랑']*dictionary['노랑']+mainleft['초록']*dictionary['초록']+mainleft['파랑']*dictionary['파랑']+mainleft['보라']*dictionary['보라']
        mainrightweight=mainright['빨강']*dictionary['빨강']+mainright['노랑']*dictionary['노랑']+mainright['초록']*dictionary['초록']+mainright['파랑']*dictionary['파랑']+mainright['보라']*dictionary['보라']
        assisleftweight=assisleft['빨강']*dictionary['빨강']+assisleft['노랑']*dictionary['노랑']+assisleft['초록']*dictionary['초록']+assisleft['파랑']*dictionary['파랑']+assisleft['보라']*dictionary['보라']
        assisrightweight=assisright['빨강']*dictionary['빨강']+assisright['노랑']*dictionary['노랑']+assisright['초록']*dictionary['초록']+assisright['파랑']*dictionary['파랑']+assisright['보라']*dictionary['보라']
        print(f'{player}번플레이어 종료되었습니다')
        print("저울의 결과가 공개되었습니다")
        if mainleftweight==mainrightweight:
            print("메인저울이 균형이 되었습니다")
            answer=list(map(int,input("빨강,노랑,초록,파랑,보라 광물의 무게를 순서대로 맞히십시오 : ").split(',')))
            if weights==answer:
                print("상금매치에 성공했습니다")
                flag=players+1
                break
                
        elif mainleftweight>mainrightweight:
            print("메인저울의 왼쪽이 더 무겁습니다")
        else :
            print("메인저울의 오른쪽이 더 무겁습니다")
        if assisleftweight==assisrightweight:
            print("보조저울이 균형이 되었습니다")
        elif assisleftweight>assisrightweight:
            print("보조저울의 왼쪽이 더 무겁습니다")
        else :
            print("보조저울의 오른쪽이 더 무겁습니다")
        mineral[player]=remain_mineral.copy()
        if sum(mineral[player].values())<=1:
            print(f'{player}번플레이어는 더 이상 광물을 올릴 수 없으므로 게임에서 제외됩니다')
            playerlist.remove(player)
            flag+=1
        if flag==players:
            print("모든 플레이어가 더 이상 광물을 저울에 올릴 수 없으므로 종료됩니다 ")
'''
import streamlit as st
from random import sample
import random
from collections import Counter

# 초기 상태 설정
if 'weights' not in st.session_state:
    weights = sample(range(1,10), 2) + sample(range(11,21), 2) + [10]
    random.shuffle(weights)
    st.session_state.weights = weights
    name = ['빨강','노랑','초록','파랑','보라']
    st.session_state.dictionary = dict(zip(name, weights))
    st.session_state.Tdictionary = dict(zip(weights, name))
    st.session_state.mineral = dict(빨강=2,노랑=2,초록=2,파랑=2,보라=2)
    st.session_state.mainleft = dict(빨강=0,노랑=0,초록=0,파랑=0,보라=0)
    st.session_state.mainright = dict(빨강=0,노랑=0,초록=0,파랑=0,보라=0)
    st.session_state.assisleft = dict(빨강=0,노랑=0,초록=0,파랑=0,보라=0)
    st.session_state.assisright = dict(빨강=0,노랑=0,초록=0,파랑=0,보라=0)

st.title("🎮 양팔 저울 추리 게임")

st.markdown(f"🟡 `{st.session_state.Tdictionary[10]}`는 3번째로 무겁고, 무게는 10g입니다.")
st.write("🎒 현재 보유 광물:", st.session_state.mineral)

# 저울에 올릴 광물 선택
st.subheader("1️⃣ 저울에 올릴 광물 선택")

ml = st.multiselect("메인저울 왼쪽", options=name, key="ml")
mr = st.multiselect("메인저울 오른쪽", options=name, key="mr")
al = st.multiselect("보조저울 왼쪽", options=name, key="al")
ar = st.multiselect("보조저울 오른쪽", options=name, key="ar")

if st.button("🔍 측정하기"):
    # 사용 광물 계산
    use_list = ml + mr + al + ar
    use_dict = dict(Counter(use_list))

    remain_mineral = st.session_state.mineral.copy()
    for k in use_dict:
        remain_mineral[k] -= use_dict[k]

    if any(v < 0 for v in remain_mineral.values()):
        st.error("❌ 광물 수를 초과해서 사용할 수 없습니다.")
    elif Counter(ml) == Counter(mr):
        st.warning("⚠️ 메인저울 양쪽 광물 구성이 같습니다.")
    elif len(use_list) < 2:
        st.warning("⚠️ 최소 2개의 광물을 사용해야 합니다.")
    else:
        # 상태 업데이트
        for color in ml:
            st.session_state.mainleft[color] += 1
        for color in mr:
            st.session_state.mainright[color] += 1
        for color in al:
            st.session_state.assisleft[color] += 1
        for color in ar:
            st.session_state.assisright[color] += 1
        st.session_state.mineral = remain_mineral

        # 결과 계산
        d = st.session_state.dictionary
        mlw = sum(st.session_state.mainleft[c] * d[c] for c in name)
        mrw = sum(st.session_state.mainright[c] * d[c] for c in name)
        alw = sum(st.session_state.assisleft[c] * d[c] for c in name)
        arw = sum(st.session_state.assisright[c] * d[c] for c in name)

        st.subheader("📊 저울 결과")
        st.write(f"⚖️ 메인저울 왼쪽: {mlw}g / 오른쪽: {mrw}g")
        st.write(f"⚖️ 보조저울 왼쪽: {alw}g / 오른쪽: {arw}g")
        if mlw == mrw:
            st.success("✅ 메인저울 균형")
            guess = st.text_input("무게를 추측해보세요 (예: 5,10,13,2,9)")
            if st.button("✅ 정답 제출"):
                try:
                    answer = list(map(int, guess.split(',')))
                    if answer == st.session_state.weights:
                        st.success("🎉 정답입니다! 상금 획득!")
                    else:
                        st.error("❌ 정답이 아닙니다.")
                except:
                    st.error("입력이 올바르지 않습니다.")
        elif mlw > mrw:
            st.info("메인저울 왼쪽이 더 무겁습니다.")
        else:
            st.info("메인저울 오른쪽이 더 무겁습니다.")

---

### 📌 다음 단계 제안
- 1인용 외에도 **여러 플레이어 지원** 가능 (각 세션마다 다르게)
- 광물 이미지 + 저울 시각화도 Streamlit + HTML/CSS로 추가 가능
- 게임 종료 조건 추가

---

이걸 기반으로 Streamlit 앱 구조를 더 확장할 수 있습니다. 원하시면 전체 프로젝트 템플릿도 만들어 드릴게요. 계속해서 개발 원하시나요?
