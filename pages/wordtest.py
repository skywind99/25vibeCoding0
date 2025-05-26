import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from bs4 import BeautifulSoup

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

# 전시 정보 파싱 함수
def get_exhibition_info():
    """국립중앙과학관 전시 정보 크롤링"""
    try:
        url = "https://smart.science.go.kr/exhibitions/list.action?menuCd=DOM_000000101003001000&contentsSid=47"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
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
        
        return exhibitions
        
    except Exception as e:
        return []

def create_map():
    """과학관 위치가 표시된 지도 생성"""
    # 대한민국 중심으로 지도 생성
    m = folium.Map(
        location=[36.5, 127.5],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # 과학관 마커 추가
    for name, info in science_museums.items():
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
    
    return m

def main():
    st.title("🔬 과학관 전시 정보")
    st.markdown("---")
    
    # 과학관 지도 생성
    map_obj = create_map()
    
    # 과학관 마커 클릭 시 전시 정보 표시
    st_folium(map_obj, width=700, height=500)
    
    # 전시 정보 로딩
    exhibitions = get_exhibition_info()
    
    st.subheader("🎨 현재 전시 정보")
    if exhibitions:
        st.success(f"총 {len(exhibitions)}개의 전시 정보를 찾았습니다.")
        for exhibition in exhibitions:
            st.expander(f"📋 {exhibition['title']}", expanded=True):
                st.markdown(f"**📅 기간:** {exhibition['date']}")
                st.markdown(f"**📝 설명:** {exhibition['description']}")
                if exhibition['link']:
                    st.markdown(f"[자세히 보기]({exhibition['link']})")
    else:
        st.warning("현재 전시 정보를 불러올 수 없습니다. 나중에 다시 시도해주세요.")

if __name__ == "__main__":
    main()
