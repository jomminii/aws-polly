import streamlit.web.cli as stcli
import sys
import os

def get_home_path():
    if getattr(sys, 'frozen', False):
        # 실행 파일로 빌드된 경우
        application_path = sys._MEIPASS
    else:
        # 개발 중일 경우 (스크립트 직접 실행)
        application_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(application_path, 'Home.py')

if __name__ == "__main__":
    home_path = get_home_path()
    sys.argv = [
        "streamlit",
        "run",
        home_path,
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())