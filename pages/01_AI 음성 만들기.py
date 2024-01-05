import streamlit as st



############
language_data_list_dict = [
    {
        "language": "English (US)",
        "language_code": "en-US",
    },
    {
        "language": "Korean",
        "language_code": "ko-KR",
    }
]

voice_dict = {
    "en-US": [
        {
            "이름": "Matthew",
            "성별": "Male",
            "특징": "news style",
        },
        {
            "이름": "Danielle",
            "성별": "Female",
            "특징": "only NTTS",
        }
    ],
    "ko-KR": [
        {
            "이름": "Seoyeon",
            "성별": "Female",
            "특징": "normal",
        },
    ]
}

# # Your list of dictionaries
# a = [
#     {"id": 1, "name": "apple"},
#     {"id": 2, "name": "banana"}
# ]
#
# # Extracting names for the selectbox
# names = [item['name'] for item in a]
#
# # Creating the selectbox
# selected_name = st.selectbox("Select a fruit", names)
#
# # Finding the corresponding id
# selected_id = next(item['id'] for item in a if item['name'] == selected_name)
#
# # You can use selected_id in your business logic
# st.write("Selected Fruit ID:", selected_id)


############


st.set_page_config(
    page_title="AI 음성 만들기",
    page_icon="🎤",
)

st.title("AI 음성 만들기")

st.markdown(
    """
    Welcome to my **AI 음성 만들기**.
    
    This is a demo of aws polly.
    
    """
)

language_list = [item['language'] for item in language_data_list_dict]

selected_language = st.selectbox("언어 선택", language_list)
selected_language_code = next(item['language_code'] for item in language_data_list_dict if item['language'] == selected_language)

st.write(selected_language_code)

persona_name_list = [item['이름'] for item in voice_dict[selected_language_code]]
if selected_language_code:
    selected_persona = st.selectbox("목소리 선택", persona_name_list)
    selected_voice = next(item['이름'] for item in voice_dict[selected_language_code] if item['이름'] == selected_persona)

    st.write(selected_voice)




st.slider("속도 선택", 20, 200, 100)
st.button("음성 만들기")

st.download_button("음성 다운로드", "음성파일")