import boto3
import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


class LangType(str, Enum):
    """
    KOR : 한국어
    ENG : 영어
    """

    KOR: str = 'ko'
    ENG: str = 'en'


# Initialize a boto3 client with the provided credentials
client_polly = boto3.client(
    'polly',
    region_name=os.environ.get('AWS_REGION_NAME'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)

# client_polly = boto3.Session().client(service_name='polly')

# Text to synthesize
text = """
Genesis chapter 5 records the genealogy of the ancestors from Adam to Noah, providing a detailed listing of their lineage. These records offer an understanding of the early stages of humanity and God's divine intentions.

Adam, the first ancestor of humanity, was created by God. He lived with Eve in the Garden of Eden but was expelled due to disobedience. However, Adam's life didn't end there. He lived for 930 years, and his descendants played a significant role in the early history of humanity. Their long lifespans signify God's special grace and His plan for humanity.

Another notable figure is Enoch. Enoch is remarkable for his unique experience. He didn't experience death but was taken up to heaven. This symbolizes the mystery of God's power and His plan.

The last part of this chapter relates to Noah. His story continues in Genesis chapter 6 and covers the significant turning point in human history, the Great Flood.

This chapter holds a significant place in the Bible as it deals with crucial aspects of the origin and early history of humanity, providing spiritual teachings and inspiration.

"""

ssml_text = """
<speak>
<prosody rate="105%">
Genesis chapter 6 begins with the story of Noah. The world was filled with wickedness, but Noah lived a different life. He found favor in the eyes of God. God instructed Noah to build a massive ark and to bring two of every animal on board.

Noah obediently started building the ark, even though many mocked him. He remained steadfast in his work. When the ark was finally completed, the great flood began, and Noah, along with his family and the animals, survived safely inside the ark.

After the floodwaters receded and the land dried up, God showed Noah a rainbow as a symbol of His promise. God vowed never to destroy the world by a flood again.

This story emphasizes the importance of faith and obedience. Noah's unwavering obedience to God's commands showcased his faith and ultimately saved the world. It continues to offer profound lessons for us today.
</prosody>

</speak>
"""
####################
# 언어 설정
####################
lang = LangType.ENG

voice_id = None

if lang == LangType.KOR:
    voice_id = 'Seoyeon'
elif lang == LangType.ENG:
    voice_id = 'Matthew'

# Request speech synthesis
response = client_polly.synthesize_speech(
    Text=ssml_text,
    OutputFormat='mp3',
    TextType='ssml',
    VoiceId=voice_id  # You can change the voice here
    # VoiceId='Matthew'  # You can change the voice here
)

# Saving the audio
if "AudioStream" in response:
    with open(f"음성_aws_{lang.value}.mp3", "wb") as file:
        file.write(response['AudioStream'].read())
    print("Audio file saved as output.mp3")
else:
    print("Could not stream audio")