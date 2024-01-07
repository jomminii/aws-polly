import streamlit as st

from datetime import date

from helper.ai_voice_helper import AIVoiceHelper
from helper.voices_dictionary import voices_dict
voice_dict = voices_dict.copy()

language_list = voice_dict.keys()


st.set_page_config(
    page_title="AI 음성 만들기 with AWS Polly",
    page_icon="🎤",
)

st.title("AI 음성 만들기")

st.markdown(
    """
    AI 음성을 만들어 보세요.
    
    ### 사용법
    1. 언어를 선택 합니다.
    2. 엔진을 선택 합니다.
       - neural 엔진 : 표준 음성보다 더 높은 품질의 음성을 생성할 수 있습니다. NTTS 시스템은 가능한 가장 자연스럽고 인간과 유사한 텍스트 음성 변환을 제공합니다.
       - standard 엔진 : 표준 TTS 음성은 연결합성(concatenative synthesis)을 사용합니다. 이 방법은 녹음된 음성의 음운을 연결하여 매우 자연스러운 합성 음성을 생성합니다. 그러나 불가피한 음성 변화와 음파를 분할하는 기술적인 한계로 인해 음성의 품질이 제한됩니다.
    3. 목소리를 선택 합니다.
    4. 속도를 선택 합니다.
    </br>
    """,
    unsafe_allow_html=True
)

selected_language = st.selectbox("언어 선택", language_list)

selected_engine = st.selectbox("엔진 선택", voice_dict[selected_language].keys())
select_data_list = [item['select_data'] for item in voice_dict[selected_language][selected_engine]]
selected_data = st.selectbox("목소리 선택", select_data_list)

selected_person_name = selected_data.split(" / ")[0]  # "Lupe / Female / Bilingual" -> "Lupe"

st.markdown(
    """
    ### 속도 선택
    - 20% : 매우 느림
    - 50% : 느림
    - 100% : 표준
    - 150% : 빠름
    - 200% : 매우 빠름
    """,
    unsafe_allow_html=True
)
speed_rate = st.slider(
    label="속도 선택",
    min_value=20, max_value=200, value=100,
    help="전체적으로 적용할 속도를 선택합니다. ssml 태그를 사용하면 부분적으로 속도를 따로 적용할 수 있습니다.",
)

text = st.text_area(
    label="내용 입력",
    help='음성으로 변환할 내용을 입력해주세요.',
    placeholder='음성으로 변환할 내용을 입력해주세요.',
)

create = st.button(
    label="음성 만들기",
)

if create:
    if selected_person_name and text:
        try:
            audio_stream = AIVoiceHelper().synthesize_voice(
                text=text,
                voice_id=selected_person_name,
                rate=speed_rate,
                engine=selected_engine,
            )

        except Exception as e:
            st.error(f"음성 변환에 실패했습니다. {e}")
            audio_stream = None
            print(e)

        if audio_stream:
            selected_language_name = selected_language.split("/")[0]  # Swedish/sv-SE -> Swedish

            st.download_button(
                label="Download MP3",
                data=audio_stream,
                file_name=f"ai_voice_{selected_language_name}_{selected_engine}_{selected_person_name}.mp3",
                mime="audio/mpeg",
                disabled=False if audio_stream else True,
            )
            st.audio(audio_stream, format="audio/mp3")

    else:
        st.warning("내용을 입력해주세요.")
        print("no")


# 날짜 범위 입력 위젯을 추가합니다.
start_date = st.date_input("시작 날짜 선택", min_value=date(2023, 1, 1))
end_date = st.date_input("종료 날짜 선택", max_value=date(2024, 12, 31))

print(start_date, end_date)

# 시작 날짜가 종료 날짜보다 클 경우 경고를 표시합니다.
if start_date > end_date:
    st.warning("시작 날짜는 종료 날짜보다 클 수 없습니다. 다시 선택하세요.")
else:
    # 선택된 날짜 범위를 출력합니다.
    st.write("선택한 날짜 범위:", start_date, "부터", end_date)

get_stat = st.button("test")
if get_stat:
    AIVoiceHelper().get_statistics()

st.markdown(
    """
    ### FAQ
    1. 음성 변환 실패 사례 (voice id 에러)
        - [AWS Polly 음성 목록](https://docs.aws.amazon.com/ko_kr/polly/latest/dg/voicelist.html) 에서 사용 가능한 목소리를 확인해주세요.
        - 만약 목소리가 없다면, helper/voice_dictionary.py 에서 해당 목소리를 삭제 해주세요. (aws 에서 지원 종료 했을 경우)
    """
)