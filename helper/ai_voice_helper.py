import pytz
import boto3
import os
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
logging.basicConfig(level=logging.DEBUG)
load_dotenv()


class AIVoiceHelper:

    def __init__(self, service, access_key, secret_access_key):
        self.client_polly = boto3.client(
            service,  # cloudwatch / polly
            region_name='ap-northeast-2',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key
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

    def get_statistics(self, start_datetime, end_datetime):
        # AWS CloudWatch 클라이언트 생성

        client = self.client_polly

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
            StartTime=start_datetime,
            EndTime=end_datetime,
            Period=86400,  # 하루 단위로 데이터 집계
            Statistics=['Sum']  # 총 사용량을 확인하고자 할 때
        )

        request_character_sum = 0
        response['Datapoints'].sort(key=lambda x: x['Timestamp'])

        chart_data_list = []

        for i in response['Datapoints']:
            original_datetime = i['Timestamp']
            korea_timezone = pytz.timezone('Asia/Seoul')
            korea_datetime = original_datetime.astimezone(korea_timezone)
            formatted_date = korea_datetime.strftime('%Y-%m-%d')
            request_character_sum += i['Sum']

            chart_data_list.append({
                "날짜": formatted_date,
                "요청 글자 수": i['Sum'],
            })

        return chart_data_list, request_character_sum

