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
Hello, this is a test message for AWS Polly.

"""

# Request speech synthesis
response = client_polly.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    VoiceId='Matthew'  # You can change the voice here
)

# Saving the audio
if "AudioStream" in response:
    with open("output.mp3", "wb") as file:
        file.write(response['AudioStream'].read())
    print("Audio file saved as output.mp3")
else:
    print("Could not stream audio")