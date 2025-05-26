def main():
    st.title("🔬 전국 과학관 정보 및 전시 안내")
    st.markdown("---")
    
    # 1. Load museum and exhibition data early
    with st.spinner("과학관 목록을 불러오는 중..."): # Changed spinner message for clarity
        additional_museums = load_additional_museums()
        all_museums = {**science_museums, **additional_museums}
    
    # Load exhibition data ONCE and early
    # This data is assumed to be primarily from/for the National Science Museum portal
    with st.spinner("국립중앙과학관 포털 전시 정보를 불러오는 중..."):
        exhibitions_data_global = get_exhibition_info() 

    # 사이드바
    st.sidebar.title("🗺️ 과학관 선택")
    
    national_museums = {k: v for k, v in all_museums.items() if '국립' in k}
    local_museums = {k: v for k, v in all_museums.items() if '국립' not in k}
    
    museum_type = st.sidebar.radio(
        "과학관 종류:",
        ["전체", "국립과학관", "지역과학관"],
        key="museum_type_radio" # Added key for potential state issues
    )
    
    if museum_type == "국립과학관":
        available_museums = national_museums
    elif museum_type == "지역과학관":
        available_museums = local_museums
    else:
        available_museums = all_museums
    
    # Initialize selected_museum. It can be updated by sidebar or map.
    # If nothing is selected yet, and available_museums is not empty, pick the first one.
    default_selection = list(available_museums.keys())[0] if available_museums else None
    
    # Use session state to keep track of selected_museum to handle updates from map
    if 'selected_museum_name' not in st.session_state:
        st.session_state.selected_museum_name = default_selection

    # Update selected_museum from sidebar
    # The selectbox itself will hold the state for the current selection from sidebar
    selected_museum_sidebar = st.sidebar.selectbox(
        "과학관을 선택하세요:",
        list(available_museums.keys()),
        index=list(available_museums.keys()).index(st.session_state.selected_museum_name) if st.session_state.selected_museum_name in available_museums else 0
    )
    # Prioritize sidebar selection if it changes
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
        map_obj, all_museums_data_for_map = create_map() # Use a different variable name
        map_data = st_folium(
            map_obj,
            width=700,
            height=500,
            returned_objects=["last_object_clicked"],
            key="folium_map" # Added key
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
            
            for name, info_map in all_museums_data_for_map.items():
                distance = ((info_map['lat'] - clicked_lat) ** 2 + (info_map['lon'] - clicked_lng) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_museum_name_map = name
            
            if closest_museum_name_map and min_distance < 0.01: # Threshold for clicking near a marker
                if st.session_state.selected_museum_name != closest_museum_name_map:
                    st.session_state.selected_museum_name = closest_museum_name_map
                    st.experimental_rerun() # Rerun to update sidebar and details panel
                st.info(f"🗺️ 지도에서 '{st.session_state.selected_museum_name}'이(가) 선택되었습니다!")
    
    with col2:
        st.subheader("🏛️ 과학관 정보")
        
        current_display_museum = st.session_state.selected_museum_name # Use the state variable

        if current_display_museum and current_display_museum in all_museums:
            info = all_museums[current_display_museum]
            
            museum_category = "🏛️ 국립과학관" if '국립' in current_display_museum else "🏢 지역과학관"
            
            st.markdown(f"**{museum_category}**")
            st.markdown(f"### {current_display_museum}")
            st.markdown(f"📍 **주소:** {info['address']}")
            if info['phone']:
                st.markdown(f"📞 **전화번호:** {info['phone']}")
            if info.get('description'):
                st.markdown(f"📝 **설명:** {info['description']}")
            if info['website']:
                st.markdown(f'🌐 **홈페이지:** [방문하기]({info["website"]})')
            
            Maps_url = f"https://maps.google.com/?q={info['lat']},{info['lon']}" # Corrected Google Maps URL
            st.markdown(f"🚗 [Google 지도로 길찾기]({Maps_url})")
            
            naver_maps_url = f"https://map.naver.com/v5/search/{requests.utils.quote(info['address'])}" # URL Encode address for Naver Maps
            st.markdown(f"🗺️ [Naver 지도로 보기]({naver_maps_url})")

            # 2. Display relevant exhibitions for the selected museum
            st.markdown("---")
            st.markdown(f"##### 🌟 '{current_display_museum}' 관련 가능성 있는 전시 (국립중앙과학관 포털 정보 기반)")
            
            relevant_exhibitions_found_for_museum = False
            if exhibitions_data_global: # Use the globally loaded exhibition data
                for ex_item in exhibitions_data_global:
                    is_relevant = False
                    museum_name_lower = current_display_museum.lower()
                    # Handle cases like "국립중앙과학관" vs "중앙과학관" for matching
                    museum_name_simplified = museum_name_lower.replace("국립", "").strip()


                    ex_title_lower = ex_item.get('title', "").lower()
                    ex_desc_lower = ex_item.get('description', "").lower()

                    if museum_name_lower in ex_title_lower or \
                       museum_name_lower in ex_desc_lower or \
                       (museum_name_simplified and (museum_name_simplified in ex_title_lower or museum_name_simplified in ex_desc_lower)):
                        is_relevant = True
                    
                    # Special handling for 국립중앙과학관 itself, as most exhibitions are from there
                    if current_display_museum == "국립중앙과학관" and not is_relevant:
                         # If no specific mention but selected museum is the source, assume relevance (or list all)
                         # For now, strict matching. This could be relaxed if desired.
                         pass


                    if is_relevant:
                        relevant_exhibitions_found_for_museum = True
                        with st.container():
                            st.markdown(f"**{ex_item['title']}**")
                            if ex_item.get('date'):
                                st.markdown(f"<small>📅 기간: {ex_item['date']}</small>", unsafe_allow_html=True)
                            if ex_item.get('description'):
                                st.markdown(f"<small>📝 설명: {ex_item['description']}</small>", unsafe_allow_html=True)
                            if ex_item.get('link'):
                                st.markdown(f"<small>[자세히 보기]({ex_item['link']})</small>", unsafe_allow_html=True)
                            st.markdown("<br>", unsafe_allow_html=True) # Add a little space
            
            if not relevant_exhibitions_found_for_museum:
                st.caption("현재 이 과학관의 이름이 언급된 전시를 국립중앙과학관 포털 목록에서 찾지 못했습니다.")
            st.markdown("---")
        else:
            st.info("사이드바 또는 지도에서 과학관을 선택해주세요.")

    st.markdown("---")
    
    # 3. General Exhibition Information Section (from National Science Museum Portal)
    st.subheader("🎨 국립중앙과학관 포털 제공 전체 전시 목록") 
    
    # Button to refresh all cached data (including museums and exhibitions)
    if st.button("🔄 모든 정보 새로고침 (캐시 지우기)", type="primary", key="refresh_all_data_button"):
        st.cache_data.clear() # Clears all @st.cache_data functions
        st.experimental_rerun()
    
    if exhibitions_data_global:
        st.success(f"국립중앙과학관 포털에서 총 {len(exhibitions_data_global)}개의 전시 정보를 찾았습니다.")
        
        for i, exhibition_item_global in enumerate(exhibitions_data_global):
            with st.expander(f"📋 {exhibition_item_global['title']}", expanded=(i < 2)): # Expand first 2
                exp_col1, exp_col2 = st.columns([3,1])
                with exp_col1:
                    if exhibition_item_global.get('date'):
                        st.markdown(f"**📅 기간:** {exhibition_item_global['date']}")
                    if exhibition_item_global.get('description'):
                        st.markdown(f"**📝 설명:** {exhibition_item_global['description']}")
                with exp_col2:
                    if exhibition_item_global.get('link'):
                        st.markdown(f"🔗 [자세히 보기]({exhibition_item_global['link']})")
                # st.markdown("---") # Optional separator inside expander
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

if __name__ == "__main__":
    main()
