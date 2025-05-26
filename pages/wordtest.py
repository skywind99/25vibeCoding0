import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="과학관 전시 정보",
    page_icon="🔬",
    layout="wide"
)

# 과학관 데이터
science_museums = {
    "국립중앙과학관": {
        "lat": 36.3724,
        "lon": 127.3755,
        "address": "대전광역시 유성구 대덕대로 481",
        "phone": "042-601-7894",
        "website": "https://www.science.go.kr"
    },
    "국립과천과학관": {
        "lat": 37.4341,
        "lon": 126.9964,
        "address": "경기도 과천시 상하벌로 110",
        "phone": "02-3677-1500",
        "website": "https://www.sciencecenter.go.kr"
    },
    "국립부산과학관": {
        "lat": 35.2273,
        "lon": 128.9242,
        "address": "부산광역시 기장군 기장읍 동부산관광로 59",
        "phone": "051-750-2300",
        "website": "https://www.sciport.or.kr"
    },
    "국립광주과학관": {
        "lat": 35.2291,
        "lon": 126.8438,
        "address": "광주광역시 북구 첨단과기로 235",
        "phone": "062-960-6114",
        "website": "https://www.gsc.go.kr"
    }
}

def get_exhibition_info():
    """국립중앙과학관 전시 정보 크롤링"""
    try:
        url = "https://smart.science.go.kr/exhibitions/list.action?menuCd=DOM_000000101003001000&contentsSid=47"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        exhibitions = []
        
        # ul.bbslist에서 전시 정보 추출
        bbs_list = soup.find('ul', class_='bbslist')
        if bbs_list:
            items = bbs_list.find_all('li')
            for item in items:
                try:
                    # 제목 추출
                    title_elem = item.find('strong') or item.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else "제목 없음"
                    
                    # 날짜/기간 추출
                    date_elem = item.find('span', class_='date') or item.find('em')
                    date = date_elem.get_text(strip=True) if date_elem else ""
                    
                    # 설명 추출
                    desc_elem = item.find('p') or item.find('div', class_='desc')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # 링크 추출
                    link_elem = item.find('a')
                    link = link_elem.get('href') if link_elem else ""
                    if link and not link.startswith('http'):
                        link = "https://smart.science.go.kr" + link
                    
                    if title and title != "제목 없음":
                        exhibitions.append({
                            'title': title,
                            'date': date,
                            'description': description[:100] + "..." if len(description) > 100 else description,
                            'link': link
                        })
                except Exception as e:
                    continue
        
        # 샘플 데이터 (크롤링이 실패할 경우 대비)
        if not exhibitions:
            exhibitions = [
                {
                    'title': '상설전시관 - 자연사관',
                    'date': '상시 운영',
                    'description': '지구의 역사와 생명의 진화 과정을 다양한 화석과 표본으로 만나보세요.',
                    'link': 'https://www.science.go.kr'
                },
                {
                    'title': '상설전시관 - 과학기술관',
                    'date': '상시 운영',
                    'description': '과학기술의 발전사와 첨단 과학기술을 체험할 수 있습니다.',
                    'link': 'https://www.science.go.kr'
                },
                {
                    'title': '천체관측소',
                    'date': '야간 운영',
                    'description': '망원경을 통해 별자리와 행성을 관측하는 프로그램입니다.',
                    'link': 'https://www.science.go.kr'
                }
            ]
        
        return exhibitions
        
    except Exception as e:
        st.error(f"전시 정보를 불러오는 중 오류가 발생했습니다: {str(e)}")
        return []

def create_map():
    """과학관 위치가 표시된 지도 생성"""
    # 대한민국 중심으로 지도 생성
    m = folium.Map(
        location=[36.5, 127.5],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # 각 과학관 마커 추가
    for name, info in science_museums.items():
        popup_html = f"""
        <div style="width: 200px;">
            <h4>{name}</h4>
            <p><strong>주소:</strong> {info['address']}</p>
            <p><strong>전화:</strong> {info['phone']}</p>
            <p><a href="{info['website']}" target="_blank">홈페이지 방문</a></p>
        </div>
        """
        
        folium.Marker(
            location=[info['lat'], info['lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=name,
            icon=folium.Icon(color='blue', icon='flask', prefix='fa')
        ).add_to(m)
    
    return m

def main():
    st.title("🔬 전국 과학관 정보 및 전시 안내")
    st.markdown("---")
    
    # 사이드바
    st.sidebar.title("🗺️ 과학관 선택")
    selected_museum = st.sidebar.selectbox(
        "과학관을 선택하세요:",
        list(science_museums.keys())
    )
    
    # 메인 컨텐츠를 두 개 컬럼으로 나누기
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.subheader("📍 과학관 위치")
        
        # 지도 생성 및 표시
        map_obj = create_map()
        map_data = st_folium(
            map_obj,
            width=700,
            height=400,
            returned_objects=["last_object_clicked"]
        )
        
        # 지도에서 클릭한 마커 정보 표시
        if map_data['last_object_clicked']:
            clicked_lat = map_data['last_object_clicked']['lat']
            clicked_lng = map_data['last_object_clicked']['lng']
            
            # 클릭한 위치와 가장 가까운 과학관 찾기
            closest_museum = None
            min_distance = float('inf')
            
            for name, info in science_museums.items():
                distance = ((info['lat'] - clicked_lat) ** 2 + (info['lon'] - clicked_lng) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_museum = name
            
            if closest_museum and min_distance < 0.1:  # 충분히 가까운 경우
                selected_museum = closest_museum
                st.info(f"📍 {selected_museum}이(가) 선택되었습니다!")
    
    with col2:
        st.subheader("🏛️ 과학관 정보")
        
        if selected_museum:
            info = science_museums[selected_museum]
            
            st.markdown(f"""
            **🏛️ {selected_museum}**
            
            📍 **주소:** {info['address']}
            
            📞 **전화번호:** {info['phone']}
            
            🌐 **홈페이지:** [방문하기]({info['website']})
            """)
            
            # 길찾기 링크
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={info['lat']},{info['lon']}"
            st.markdown(f"🚗 [구글 지도로 길찾기]({google_maps_url})")
    
    st.markdown("---")
    
    # 전시 정보 섹션
    st.subheader("🎨 현재 전시 정보")
    
    if st.button("🔄 전시 정보 새로고침", type="primary"):
        st.cache_data.clear()
    
    # 전시 정보 로딩
    with st.spinner("전시 정보를 불러오는 중..."):
        exhibitions = get_exhibition_info()
    
    if exhibitions:
        st.success(f"총 {len(exhibitions)}개의 전시 정보를 찾았습니다.")
        
        # 전시 정보를 카드 형태로 표시
        for i, exhibition in enumerate(exhibitions):
            with st.expander(f"📋 {exhibition['title']}", expanded=(i < 3)):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if exhibition['date']:
                        st.markdown(f"**📅 기간:** {exhibition['date']}")
                    
                    if exhibition['description']:
                        st.markdown(f"**📝 설명:** {exhibition['description']}")
                
                with col2:
                    if exhibition['link']:
                        st.markdown(f"[자세히 보기]({exhibition['link']})")
                
                st.markdown("---")
    else:
        st.warning("현재 전시 정보를 불러올 수 없습니다. 나중에 다시 시도해주세요.")
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>🔬 전국 과학관 정보 서비스 | 
            <a href='https://smart.science.go.kr' target='_blank'>국립중앙과학관</a> 데이터 기반</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
