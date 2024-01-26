import streamlit as st
import pandas as pd

from datetime import date

from component.side_bar import aws_credentials_sidebar
from helper.ai_voice_helper import AIVoiceHelper
from helper.common_helper import convert_date_to_utc_datetime

st.set_page_config(
    page_title="AWS 사용량 조회",
    page_icon="🎤",
)

st.title("AWS 사용량 조회")

st.markdown(
    """
    AWS 사용량을 조회합니다.
    
    참고용 데이터이며, 정확한 데이터는 AWS 콘솔에서 확인하세요.
    
    </br>
    """,
    unsafe_allow_html=True
)

access_key_in_session, secret_access_key_in_session = aws_credentials_sidebar()

# 날짜 범위 입력 위젯을 추가합니다.
start_date = st.date_input("시작 날짜 선택", min_value=date(2023, 1, 1))
end_date = st.date_input("종료 날짜 선택", max_value=date(2030, 12, 31))

# 시작 날짜가 종료 날짜보다 클 경우 경고를 표시합니다.
if start_date > end_date:
    st.warning("시작 날짜는 종료 날짜보다 클 수 없습니다. 다시 선택하세요.")
else:
    # 선택된 날짜 범위를 출력합니다.
    st.write("선택한 날짜 범위:", start_date, "부터", end_date)


get_stat = st.button("사용량 조회")
if get_stat:
    start_datetime = convert_date_to_utc_datetime(start_date, date_type="start")
    end_datetime = convert_date_to_utc_datetime(end_date, date_type="end")

    chart_data_list, sum = AIVoiceHelper(
        service="cloudwatch",
        access_key=access_key_in_session,
        secret_access_key=secret_access_key_in_session,
    ).get_statistics(start_datetime=start_datetime, end_datetime=end_datetime)

    if chart_data_list:

        st.write(f"총 사용량: {int(sum)}")

        # 차트 데이터를 데이터프레임으로 변환합니다.
        df = pd.DataFrame(chart_data_list)
        st.bar_chart(df, x="날짜", y="요청 글자 수", color=["#FF0000"])

    else:
        st.write("조회할 데이터가 없습니다.")
