# ----------------------------------------------------------------------
# 1. IMPORTS (Should be at the very top)
# ----------------------------------------------------------------------
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime # Ensure this is imported if used

# ----------------------------------------------------------------------
# 2. PAGE CONFIGURATION (Immediately after imports)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="과학관 전시 정보",
    page_icon="🔬",
    layout="wide"
)

# ----------------------------------------------------------------------
# 3. GLOBAL DATA AND HELPER FUNCTION DEFINITIONS
# ----------------------------------------------------------------------
science_museums = {
    # ... your initial museum data ...
}

@st.cache_data(ttl=3600)
def load_additional_museums():
    # ... your function code ...
    # (Make sure any libraries used inside, like ssl, urllib3, are imported at the top)
    additional_museums = {} # Initialize
    try:
        import ssl # If used locally in function, ensure it's available
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # ... rest of the try block ...
        url = "https://smart.science.go.kr/scienceMuseum/subject/list.action?museum_med_cd=453&code=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        museum_items = soup.find_all('div', class_=['museum_item', 'item', 'list_item']) or soup.find_all('li')
        # ... (rest of your parsing logic) ...
    except Exception as e:
        st.info(f"외부 사이트 접속 제한으로 기본 과학관 목록을 사용합니다. 오류: {e}") # Log error for debugging

    if not additional_museums: # Fallback data
        additional_museums = {
            # ... your fallback museum data ...
        }
    return additional_museums


def get_estimated_coordinates(address):
    # ... your function code ...
    city_coords = {
        "서울": [37.5665, 126.9780], "부산": [35.1796, 129.0756], "대구": [35.8714, 128.6014],
        "인천": [37.4563, 126.7052], "광주": [35.1595, 126.8526], "대전": [36.3504, 127.3845],
        "울산": [35.5384, 129.3114], "경기": [37.4138, 127.5183], "강원": [37.8228, 128.1555],
        "충북": [36.6357, 127.4917], "충남": [36.5184, 126.8000], "전북": [35.7175, 127.1530],
        "전남": [34.8679, 126.9910], "경북": [36.4919, 128.8889], "경남": [35.4606, 128.2132],
        "제주": [33.4996, 126.5312]
    }
    for city, coords in city_coords.items():
        if city in address:
            return coords
    return None # Default return

@st.cache_data(ttl=1800) # Adding cache to exhibition info as it's also web-scraped
def get_exhibition_info():
    # ... your function code ...
    # (Make sure any libraries used inside, like urllib3, are imported at the top)
    exhibitions = [] # Initialize
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        url = "https://smart.science.go.kr/exhibitions/list.action?menuCd=DOM_000000101003001000&contentsSid=47"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # ... (rest of your parsing logic) ...
    except Exception as e:
        st.warning(f"전시 정보 크롤링 중 오류 발생: {e}. 기본 샘플 데이터를 사용합니다.") # Log error

    if not exhibitions: # Fallback data
        exhibitions = [
            # ... your sample exhibition data ...
        ]
    return exhibitions


def create_map():
    # ... your function code ...
    # (This function calls load_additional_museums)
    m = folium.Map(location=[36.5, 127.5], zoom_start=7, tiles='OpenStreetMap')
    additional_museums_map = load_additional_museums()
    all_museums_map = {**science_museums, **additional_museums_map}
    # ... (rest of your map creation logic) ...
    return m, all_museums_map


# ----------------------------------------------------------------------
# 4. MAIN APPLICATION LOGIC
# ----------------------------------------------------------------------
def main():
    st.title("🔬 전국 과학관 정보 및 전시 안내") # This is where the error was reported
    st.markdown("---")
    
    with st.spinner("과학관 목록을 불러오는 중..."):
        additional_museums = load_additional_museums()
        all_museums = {**science_museums, **additional_museums}
    
    with st.spinner("국립중앙과학관 포털 전시 정보를 불러오는 중..."):
        exhibitions_data_global = get_exhibition_info() 

    st.sidebar.title("🗺️ 과학관 선택")
    
    national_museums = {k: v for k, v in all_museums.items() if '국립' in k}
    local_museums = {k: v for k, v in all_museums.items() if '국립' not in k}
    
    museum_type = st.sidebar.radio(
        "과학관 종류:",
        ["전체", "국립과학관", "지역과학관"],
        key="museum_type_radio"
    )
    
    current_available_museums = all_museums # Default
    if museum_type == "국립과학관":
        current_available_museums = national_museums
    elif museum_type == "지역과학관":
        current_available_museums = local_museums
    
    # Ensure current_available_museums is not empty before trying to access its keys
    if not current_available_museums:
        st.sidebar.warning("선택한 종류의 과학관 정보가 없습니다.")
        # Potentially halt further execution or handle this case gracefully
        return 

    default_selection_index = 0
    museum_keys = list(current_available_museums.keys())

    if 'selected_museum_name' not in st.session_state or st.session_state.selected_museum_name not in museum_keys:
        st.session_state.selected_museum_name = museum_keys[0] if museum_keys else None
    
    if st.session_state.selected_museum_name: # Check if a valid museum is selected
        try:
            default_selection_index = museum_keys.index(st.session_state.selected_museum_name)
        except ValueError: # If somehow selected_museum_name is not in current keys, reset
            st.session_state.selected_museum_name = museum_keys[0] if museum_keys else None
            default_selection_index = 0


    selected_museum_sidebar = st.sidebar.selectbox(
        "과학관을 선택하세요:",
        museum_keys,
        index=default_selection_index,
        key="sidebar_selectbox"
    )

    if selected_museum_sidebar != st.session_state.selected_museum_name:
         st.session_state.selected_museum_name = selected_museum_sidebar
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 과학관 현황")
    st.sidebar.metric("전체 과학관", len(all_museums))
    st.sidebar.metric("국립과학관", len(national_museums))
    st.sidebar.metric("지역과학관", len(local_museums))
    
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.subheader("📍 과학관 위치")
        if not all_museums: # Check if all_museums is empty
            st.warning("표시할 과학관 데이터가 없습니다.")
        else:
            map_obj, all_museums_data_for_map = create_map()
            map_data = st_folium(
                map_obj,
                width=700,
                height=500,
                returned_objects=["last_object_clicked"],
                key="folium_map" 
            )
            
            st.markdown("""
            **지도 범례:**
            - 🔴 국립과학관 (빨간색 마커)
            - 🔵 지역과학관 (파란색 마커)
            """)
            
            if map_data.get('last_object_clicked'):
                clicked_lat = map_data['last_object_clicked']['lat']
                clicked_lng = map_data['last_object_clicked']['lng']
                
                closest_museum_name_map = None
                min_distance = float('inf')
                
                for name_map, info_map in all_museums_data_for_map.items(): # Use .items()
                    if 'lat' in info_map and 'lon' in info_map: # Ensure lat/lon exist
                        distance = ((info_map['lat'] - clicked_lat) ** 2 + (info_map['lon'] - clicked_lng) ** 2) ** 0.5
                        if distance < min_distance:
                            min_distance = distance
                            closest_museum_name_map = name_map # name_map is the key (name of museum)
                
                if closest_museum_name_map and min_distance < 0.01: 
                    if st.session_state.selected_museum_name != closest_museum_name_map:
                        st.session_state.selected_museum_name = closest_museum_name_map
                        st.experimental_rerun() 
                    st.info(f"🗺️ 지도에서 '{st.session_state.selected_museum_name}'이(가) 선택되었습니다!")
    
    with col2:
        st.subheader("🏛️ 과학관 정보")
        
        current_display_museum = st.session_state.selected_museum_name

        if current_display_museum and current_display_museum in all_museums:
            info = all_museums[current_display_museum]
            
            museum_category = "🏛️ 국립과학관" if '국립' in current_display_museum else "🏢 지역과학관"
            
            st.markdown(f"**{museum_category}**")
            st.markdown(f"### {current_display_museum}")
            st.markdown(f"📍 **주소:** {info.get('address', 'N/A')}") # Use .get for safety
            if info.get('phone'):
                st.markdown(f"📞 **전화번호:** {info['phone']}")
            if info.get('description'):
                st.markdown(f"📝 **설명:** {info['description']}")
            if info.get('website'):
                st.markdown(f'🌐 **홈페이지:** [방문하기]({info["website"]})')
            
            # Ensure lat/lon exist before creating map links
            if 'lat' in info and 'lon' in info:
                Maps_url = f"https://www.google.com/maps?q={info['lat']},{info['lon']}"
                st.markdown(f"🚗 [Google 지도로 길찾기]({Maps_url})")
                
                # URL Encode address for Naver Maps
                naver_maps_url = f"https://map.naver.com/v5/search/{requests.utils.quote(info.get('address', ''))}"
                st.markdown(f"🗺️ [Naver 지도로 보기]({naver_maps_url})")
            else:
                st.caption("위치 정보가 없어 지도 링크를 제공할 수 없습니다.")


            st.markdown("---")
            st.markdown(f"##### 🌟 '{current_display_museum}' 관련 가능성 있는 전시 (국립중앙과학관 포털 정보 기반)")
            
            relevant_exhibitions_found_for_museum = False
            if exhibitions_data_global: 
                for ex_item in exhibitions_data_global:
                    is_relevant = False
                    museum_name_lower = current_display_museum.lower()
                    museum_name_simplified = museum_name_lower.replace("국립", "").strip()

                    ex_title_lower = ex_item.get('title', "").lower()
                    ex_desc_lower = ex_item.get('description', "").lower()

                    if museum_name_lower in ex_title_lower or \
                       museum_name_lower in ex_desc_lower or \
                       (museum_name_simplified and (museum_name_simplified in ex_title_lower or museum_name_simplified in ex_desc_lower)):
                        is_relevant = True
                    
                    if is_relevant:
                        relevant_exhibitions_found_for_museum = True
                        with st.container():
                            st.markdown(f"**{ex_item.get('title', '제목 없음')}**")
                            if ex_item.get('date'):
                                st.markdown(f"<small>📅 기간: {ex_item['date']}</small>", unsafe_allow_html=True)
                            if ex_item.get('description'):
                                st.markdown(f"<small>📝 설명: {ex_item['description']}</small>", unsafe_allow_html=True)
                            if ex_item.get('link'):
                                st.markdown(f"<small>[자세히 보기]({ex_item['link']})</small>", unsafe_allow_html=True)
                            st.markdown("<br>", unsafe_allow_html=True) 
            
            if not relevant_exhibitions_found_for_museum:
                st.caption("현재 이 과학관의 이름이 언급된 전시를 국립중앙과학관 포털 목록에서 찾지 못했습니다.")
            st.markdown("---")
        elif not current_display_museum and museum_keys: # If no museum selected but list exists
             st.info("사이드바 또는 지도에서 과학관을 선택해주세요.")
        elif not museum_keys: # No museums available at all
            st.warning("표시할 과학관 정보가 없습니다.")


    st.markdown("---")
    
    st.subheader("🎨 국립중앙과학관 포털 제공 전체 전시 목록") 
    
    if st.button("🔄 모든 정보 새로고침 (캐시 지우기)", type="primary", key="refresh_all_data_button"):
        st.cache_data.clear() 
        st.experimental_rerun()
    
    if exhibitions_data_global:
        st.success(f"국립중앙과학관 포털에서 총 {len(exhibitions_data_global)}개의 전시 정보를 찾았습니다.")
        
        for i, exhibition_item_global in enumerate(exhibitions_data_global):
            with st.expander(f"📋 {exhibition_item_global.get('title', '제목 없음')}", expanded=(i < 2)):
                exp_col1, exp_col2 = st.columns([3,1])
                with exp_col1:
                    if exhibition_item_global.get('date'):
                        st.markdown(f"**📅 기간:** {exhibition_item_global['date']}")
                    if exhibition_item_global.get('description'):
                        st.markdown(f"**📝 설명:** {exhibition_item_global['description']}")
                with exp_col2:
                    if exhibition_item_global.get('link'):
                        st.markdown(f"🔗 [자세히 보기]({exhibition_item_global['link']})")
    else:
        st.warning("현재 국립중앙과학관 포털에서 전시 정보를 불러올 수 없습니다. 네트워크 상태를 확인하거나 나중에 다시 시도해주세요.")
            
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>🔬 전국 과학관 정보 서비스 | 
            <a href='https://smart.science.go.kr' target='_blank'>국립중앙과학관</a> 데이터 기반</p>
            <p>📡 정보는 주기적으로 캐시될 수 있습니다.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# ----------------------------------------------------------------------
# 5. SCRIPT EXECUTION GUARD (Call main function)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
