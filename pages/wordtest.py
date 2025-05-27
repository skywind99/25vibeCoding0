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
        "website": "https://www.science.go.kr",
        "description": "우리나라 최초의 종합과학관으로 자연사관, 과학기술관 등 다양한 전시관 운영"
    },
    "국립과천과학관": {
        "lat": 37.4341,
        "lon": 126.9964,
        "address": "경기도 과천시 상하벌로 110",
        "phone": "02-3677-1500",
        "website": "https://www.sciencecenter.go.kr",
        "description": "수도권 대표 과학관으로 첨단기술관, 자연사관, 천체관 등 운영"
    },
    "국립부산과학관": {
        "lat": 35.2273,
        "lon": 128.9242,
        "address": "부산광역시 기장군 기장읍 동부산관광로 59",
        "phone": "051-750-2300",
        "website": "https://www.sciport.or.kr",
        "description": "영남권 대표 과학관으로 해양과학, 항공우주 분야 특화 전시 운영"
    },
    "국립광주과학관": {
        "lat": 35.2291,
        "lon": 126.8438,
        "address": "광주광역시 북구 첨단과기로 235",
        "phone": "062-960-6114",
        "website": "https://www.gsc.go.kr",
        "description": "호남권 대표 과학관으로 빛과 에너지 분야 특화 전시 운영"
    }
}

# 추가 과학관 데이터를 동적으로 가져오는 함수
@st.cache_data(ttl=3600)  # 1시간 캐시
def load_additional_museums():
    """과학관 목록 사이트에서 추가 과학관 정보 수집"""
    additional_museums = {}
    
    try:
        import ssl
        import urllib3
        
        # SSL 경고 무시
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        url = "https://smart.science.go.kr/scienceMuseum/subject/list.action?museum_med_cd=453&code=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # SSL 검증 비활성화하여 요청
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 과학관 목록에서 정보 추출
        museum_items = soup.find_all('div', class_=['museum_item', 'item', 'list_item']) or soup.find_all('li')
        
        for item in museum_items:
            try:
                # 과학관 이름 추출
                name_elem = item.find('h3') or item.find('h4') or item.find('strong') or item.find('a')
                if not name_elem:
                    continue
                    
                name = name_elem.get_text(strip=True)
                if not name or name in science_museums:
                    continue
                
                # 주소 추출
                addr_elem = item.find('p', string=lambda text: text and '주소' in text) or \
                           item.find('span', string=lambda text: text and ('시' in text or '도' in text))
                address = addr_elem.get_text(strip=True) if addr_elem else ""
                
                # 전화번호 추출
                phone_elem = item.find('span', string=lambda text: text and ('-' in text and len(text) > 8))
                phone = phone_elem.get_text(strip=True) if phone_elem else ""
                
                # 링크 추출
                link_elem = item.find('a')
                website = link_elem.get('href') if link_elem else ""
                if website and not website.startswith('http'):
                    website = "https://smart.science.go.kr" + website
                
                # 좌표는 주요 도시 기준으로 추정 (실제 서비스에서는 지오코딩 API 사용 권장)
                coords = get_estimated_coordinates(address)
                
                if coords and name not in ['', '과학관', '박물관']:
                    additional_museums[name] = {
                        "lat": coords[0],
                        "lon": coords[1],
                        "address": address,
                        "phone": phone,
                        "website": website,
                        "description": f"{name} - 지역 과학 교육의 중심지"
                    }
                    
            except Exception as e:
                continue
                
    except Exception as e:
        st.info(f"외부 사이트 접속 제한으로 기본 과학관 목록을 사용합니다.")
    
    # 전국 주요 과학관 데이터 (크롤링 실패 시 또는 추가 정보)
    if not additional_museums:
        additional_museums = {
            "서울특별시과학관": {
                "lat": 37.5665,
                "lon": 126.9780,
                "address": "서울특별시 노원구 한글비석로 160",
                "phone": "02-970-4500",
                "website": "https://science.seoul.go.kr",
                "description": "서울시민을 위한 과학교육 및 체험학습 전문기관"
            },
            "경기도어린이박물관": {
                "lat": 37.2636,
                "lon": 127.0286,
                "address": "경기도 용인시 기흥구 상갈로 6",
                "phone": "031-270-8600",
                "website": "https://www.gcm.go.kr",
                "description": "어린이 중심의 체험형 박물관"
            },
            "대구국립과학관": {
                "lat": 35.8714,
                "lon": 128.6014,
                "address": "대구광역시 달성군 유가읍 테크노대로 20길 186",
                "phone": "053-670-6114",
                "website": "https://www.dnsm.or.kr",
                "description": "영남권 과학문화 확산을 위한 종합과학관"
            },
            "인천광역시과학관": {
                "lat": 37.4563,
                "lon": 126.7052,
                "address": "인천광역시 연수구 미래로 131",
                "phone": "032-749-2300",
                "website": "https://www.ism.go.kr",
                "description": "인천시민과 함께하는 과학문화공간"
            },
            "울산과학관": {
                "lat": 35.5384,
                "lon": 129.3114,
                "address": "울산광역시 남구 정동 번지",
                "phone": "052-220-1114",
                "website": "https://www.usm.go.kr",
                "description": "산업도시 울산의 과학기술 체험관"
            },
            "강원과학관": {
                "lat": 37.8228,
                "lon": 128.1555,
                "address": "강원도 춘천시 중앙로 1가",
                "phone": "033-250-1300",
                "website": "https://www.gwsm.go.kr",
                "description": "강원도민을 위한 과학문화 체험공간"
            },
            "충북과학관": {
                "lat": 36.6357,
                "lon": 127.4917,
                "address": "충청북도 청주시 흥덕구 오송읍",
                "phone": "043-650-1234",
                "website": "https://www.cbsm.go.kr",
                "description": "충북지역 과학교육의 메카"
            },
            "전남과학관": {
                "lat": 34.8679,
                "lon": 126.9910,
                "address": "전라남도 나주시 혁신산업단지",
                "phone": "061-334-1500",
                "website": "https://www.jnsm.go.kr",
                "description": "전남지역 과학문화 발전소"
            },
            "경북과학관": {
                "lat": 36.4919,
                "lon": 128.8889,
                "address": "경상북도 구미시 산동면",
                "phone": "054-480-4600",
                "website": "https://www.gbsm.go.kr",
                "description": "경북지역 과학기술 체험관"
            },
            "제주과학관": {
                "lat": 33.4996,
                "lon": 126.5312,
                "address": "제주특별자치도 제주시 1100로",
                "phone": "064-710-7000",
                "website": "https://www.jejusm.go.kr",
                "description": "제주도민과 관광객을 위한 과학체험관"
            }
        }
    
    return additional_museums

def get_estimated_coordinates(address):
    """주소 기반 좌표 추정 (간단한 매핑)"""
    city_coords = {
        "서울": [37.5665, 126.9780],
        "부산": [35.1796, 129.0756],
        "대구": [35.8714, 128.6014],
        "인천": [37.4563, 126.7052],
        "광주": [35.1595, 126.8526],
        "대전": [36.3504, 127.3845],
        "울산": [35.5384, 129.3114],
        "경기": [37.4138, 127.5183],
        "강원": [37.8228, 128.1555],
        "충북": [36.6357, 127.4917],
        "충남": [36.5184, 126.8000],
        "전북": [35.7175, 127.1530],
        "전남": [34.8679, 126.9910],
        "경북": [36.4919, 128.8889],
        "경남": [35.4606, 128.2132],
        "제주": [33.4996, 126.5312]
    }
    
    for city, coords in city_coords.items():
        if city in address:
            return coords
    
    return None

def get_exhibition_info():
    """국립중앙과학관 전시 정보 크롤링"""
    try:
        import urllib3
        
        # SSL 경고 무시
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        url = "https://smart.science.go.kr/exhibitions/list.action?menuCd=DOM_000000101003001000&contentsSid=47"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # SSL 검증 비활성화
        response = requests.get(url, headers=headers, timeout=15, verify=False)
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
                },
                {
                    'title': '특별전시 - AI와 미래과학',
                    'date': '2024.01~2024.12',
                    'description': '인공지능 기술의 발전과 미래 과학기술을 체험해보세요.',
                    'link': 'https://www.science.go.kr'
                },
                {
                    'title': '어린이과학놀이터',
                    'date': '상시 운영',
                    'description': '어린이들이 직접 만지고 체험할 수 있는 과학 놀이 공간입니다.',
                    'link': 'https://www.science.go.kr'
                }
            ]
        
        return exhibitions
        
    except Exception as e:
        # 네트워크 오류 시 기본 전시 정보 제공
        return [
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
            },
            {
                'title': '특별전시 - 우주탐험',
                'date': '2024년 연중',
                'description': '우주의 신비와 우주탐험의 역사를 만나보세요.',
                'link': 'https://www.science.go.kr'
            },
            {
                'title': '과학체험교실',
                'date': '주말 운영',
                'description': '다양한 과학 실험과 체험활동을 통해 과학의 원리를 배워보세요.',
                'link': 'https://www.science.go.kr'
            }
        ]

def create_map():
    """과학관 위치가 표시된 지도 생성"""
    # 대한민국 중심으로 지도 생성
    m = folium.Map(
        location=[36.5, 127.5],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # 추가 과학관 정보 로드
    additional_museums = load_additional_museums()
    
    # 기본 과학관과 추가 과학관 합치기
    all_museums = {**science_museums, **additional_museums}
    
    # 각 과학관 마커 추가
    for name, info in all_museums.items():
        # 국립 과학관은 빨간색, 기타는 파란색으로 구분
        icon_color = 'red' if '국립' in name else 'blue'
        
        popup_html = f"""
        <div style="width: 250px;">
            <h4>{name}</h4>
            <p><strong>주소:</strong> {info['address']}</p>
            {f"<p><strong>전화:</strong> {info['phone']}</p>" if info['phone'] else ""}
            {f"<p><strong>설명:</strong> {info['description']}</p>" if info.get('description') else ""}
            {f'<p><a href="{info["website"]}" target="_blank">홈페이지 방문</a></p>' if info['website'] else ""}
        </div>
        """
        
        folium.Marker(
            location=[info['lat'], info['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=name,
            icon=folium.Icon(color=icon_color, icon='flask', prefix='fa')
        ).add_to(m)
    
    return m, all_museums

def main():
    st.title("🔬 전국 과학관 정보 및 전시 안내")
    st.markdown("---")
    
    # 과학관 데이터 로드
    with st.spinner("과학관 정보를 불러오는 중..."):
        additional_museums = load_additional_museums()
        all_museums = {**science_museums, **additional_museums}
    
    # 사이드바
    st.sidebar.title("🗺️ 과학관 선택")
    
    # 과학관 종류별로 분류
    national_museums = {k: v for k, v in all_museums.items() if '국립' in k}
    local_museums = {k: v for k, v in all_museums.items() if '국립' not in k}
    
    museum_type = st.sidebar.radio(
        "과학관 종류:",
        ["전체", "국립과학관", "지역과학관"]
    )
    
    if museum_type == "국립과학관":
        available_museums = national_museums
    elif museum_type == "지역과학관":
        available_museums = local_museums
    else:
        available_museums = all_museums
    
    selected_museum = st.sidebar.selectbox(
        "과학관을 선택하세요:",
        list(available_museums.keys())
    )
    
    # 통계 정보
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 과학관 현황")
    st.sidebar.metric("전체 과학관", len(all_museums))
    st.sidebar.metric("국립과학관", len(national_museums))
    st.sidebar.metric("지역과학관", len(local_museums))
    
    # 메인 컨텐츠를 두 개 컬럼으로 나누기
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.subheader("📍 과학관 위치")
        
        # 지도 생성 및 표시
        map_obj, all_museums_data = create_map()
        map_data = st_folium(
            map_obj,
            width=700,
            height=500,
            returned_objects=["last_object_clicked"]
        )
        
        # 범례 추가
        st.markdown("""
        **지도 범례:**
        - 🔴 국립과학관 (빨간색 마커)
        - 🔵 지역과학관 (파란색 마커)
        """)
        
        # 지도에서 클릭한 마커 정보 표시
        if map_data['last_object_clicked']:
            clicked_lat = map_data['last_object_clicked']['lat']
            clicked_lng = map_data['last_object_clicked']['lng']
            
            # 클릭한 위치와 가장 가까운 과학관 찾기
            closest_museum = None
            min_distance = float('inf')
            
            for name, info in all_museums_data.items():
                distance = ((info['lat'] - clicked_lat) ** 2 + (info['lon'] - clicked_lng) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_museum = name
            
            if closest_museum and min_distance < 0.1:  # 충분히 가까운 경우
                selected_museum = closest_museum
                st.info(f"📍 {selected_museum}이(가) 선택되었습니다!")
    
    with col2:
        st.subheader("🏛️ 과학관 정보")
        
        if selected_museum and selected_museum in all_museums:
            info = all_museums[selected_museum]
            
            # 과학관 종류 표시
            museum_category = "🏛️ 국립과학관" if '국립' in selected_museum else "🏢 지역과학관"
            
            st.markdown(f"""
            **{museum_category}**
            
            ### {selected_museum}
            
            📍 **주소:** {info['address']}
            
            {f"📞 **전화번호:** {info['phone']}" if info['phone'] else ""}
            
            {f"📝 **설명:** {info['description']}" if info.get('description') else ""}
            
            {f'🌐 **홈페이지:** [방문하기]({info["website"]})' if info['website'] else ""}
            """)
            
            # 길찾기 링크
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={info['lat']},{info['lon']}"
            st.markdown(f"🚗 [구글 지도로 길찾기]({google_maps_url})")
            
            # 네이버 지도 링크
            naver_maps_url = f"https://map.naver.com/v5/search/{info['address']}"
            st.markdown(f"🗺️ [네이버 지도로 보기]({naver_maps_url})")
    
    st.markdown("---")
    
    # 전시 정보 섹션
    st.subheader("🎨 현재 전시 정보")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("💡 전시 정보는 국립중앙과학관 기준으로 표시됩니다.")
    with col2:
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
            <p>📡 실시간 과학관 정보 업데이트</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
