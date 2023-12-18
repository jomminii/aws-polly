import boto3
import os
from dotenv import load_dotenv

load_dotenv()

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
 <lang xml:lang="en-US">anyway,</lang> 창세기 5장은 아담에서 노아까지 선조들을 기록하며, 그들의 족보를 자세히 나열합니다. 이러한 기록은 인간의 초기 단계와 신성한 의도에 대한 이해를 제공합니다.
</prosody>

</speak>
"""

# Request speech synthesis
response = client_polly.synthesize_speech(
    Text=ssml_text,
    OutputFormat='mp3',
    TextType='ssml',
    VoiceId='Seoyeon'  # You can change the voice here
)


# Saving the audio
if "AudioStream" in response:
    with open("output.mp3", "wb") as file:
        file.write(response['AudioStream'].read())
    print("Audio file saved as output.mp3")
else:
    print("Could not stream audio")