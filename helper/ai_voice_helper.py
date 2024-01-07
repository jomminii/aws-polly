import boto3
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()


class AIVoiceHelper:

    def __init__(self):
        self.client_polly = boto3.client(
            'polly',
            region_name=os.environ.get('AWS_REGION_NAME'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )

    def synthesize_voice(
        self,
        text,
        voice_id,
        rate=100,
        engine="neural"
    ):

        ssml_text = f"""
        <speak>
            <prosody rate="{rate}%">
                {text}
            </prosody>
        </speak>
        """
        try:
            # Request speech synthesis
            response = self.client_polly.synthesize_speech(
                Text=ssml_text,
                OutputFormat='mp3',
                TextType='ssml',
                VoiceId=voice_id,  # You can change the voice here
                Engine=engine,
            )

            # audio stream 으로 전달
            if "AudioStream" in response:
                return response['AudioStream'].read()
            else:
                print("AudioStream not found in the response")
                return None

        except Exception as e:
            raise e


    def get_statistics(self):
        # AWS CloudWatch 클라이언트 생성
        client = boto3.client('cloudwatch', region_name='ap-northeast-2')

        # 시작 및 종료 시간 설정
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=30)  # 예: 지난 30일간의 데이터

        # AWS Polly 관련 메트릭 가져오기
        response = client.get_metric_statistics(
            Namespace='AWS/Polly',
            MetricName='RequestCharacters',  # AWS Polly에서 문자 수를 나타내는 메트릭
            Dimensions=[
                {
                    'Name': 'Operation',
                    'Value': 'SynthesizeSpeech'  # 'SynthesizeSpeech' 작업에 대한 메트릭
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,  # 하루 단위로 데이터 집계
            Statistics=['Sum']  # 총 사용량을 확인하고자 할 때
        )
        import pytz

        # 주어진 datetime 값을 생성합니다.
        # original_datetime = datetime(2023, 12, 29, 13, 15, tzinfo=pytz.utc)

        # 한국 시간대로 변환합니다.

        sum = 0
        for i in response['Datapoints']:
            original_datetime = i['Timestamp']
            print(original_datetime)
            korea_timezone = pytz.timezone('Asia/Seoul')
            korea_datetime = original_datetime.astimezone(korea_timezone)
            formatted_date = korea_datetime.strftime('%Y-%m-%d')
            sum += i['Sum']
            print(f"날짜 : {formatted_date} \n 요청 글자 수 : {i['Sum']}")
        print(f"총 요청 글자 수 : {sum}")
        return response

