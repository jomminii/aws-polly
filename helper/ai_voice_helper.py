import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class AIVoiceHelper:

    def __init__(self):
        self.client_polly = boto3.client(
            'polly',
            region_name=os.environ.get('AWS_REGION_NAME'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )

    def synthesize_voice(self, text,
                         # language_code,
                         voice_id, rate=100, engine="neural"):

        ssml_text = f"""
        <speak>
            <prosody rate="{rate}%">
                {text}
            </prosody>
        </speak>
        """
        print("$$", ssml_text)
        try:
            # Request speech synthesis
            response = self.client_polly.synthesize_speech(
                Text=ssml_text,
                OutputFormat='mp3',
                TextType='ssml',
                VoiceId=voice_id,  # You can change the voice here
                Engine=engine,
                # VoiceId='Matthew'  # You can change the voice here
            )

            # # Saving the audio
            # if "AudioStream" in response:
            #     with open(f"voice_{language_code}_{voice_id}.mp3", "wb") as file:
            #         file.write(response['AudioStream'].read())
            #     print("Audio file saved as output.mp3")
            # else:
            #     print("Could not stream audio")

            # audio stream 으로 전달
            if "AudioStream" in response:
                return response['AudioStream'].read()
            else:
                print("AudioStream not found in the response")
                return None

        except Exception as e:
            print(f"Error in synthesizing voice: {e}")
            return None
