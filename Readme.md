# 음성 종류
- [aws polly 목소리](https://docs.aws.amazon.com/ko_kr/polly/latest/dg/voicelist.html)
- ko-KR
  - Seoyeon
- en-US
  - FEMAIL
    - Danielle
    - Ivy(child)
    - Joanna
    - Kendra
    - Kimberly
    - Salli
    - Ruth
  - MALE
    - Gregory
    - Joey
    - Justin(child)
    - Kevin(child)
    - Matthew
    - Stephen

# 속도 조절
- rate 에 속도 명시
```
x-slow, slow, medium, fast,x-fast. Sets the pitch to a predefined value for the selected voice.

n%: A non-negative percentage change in the speaking rate. For example, a value of 100% means no change in speaking rate, a value of 200% means a speaking rate twice the default rate, and a value of 50% means a speaking rate of half the default rate. This value has a range of 20-200%.
```

```python

ssml_text = """
<speak>
  <prosody rate="105%">
        창세기 5장은 아담에서 노아까지 선조들을 기록하며, 그들의 족보를 자세히 나열합니다. 이러한 기록은 인간의 초기 단계와 신성한 의도에 대한 이해를 제공합니다.
  </prosody>

</speak>
"""

```

- 속도명시를 하지 않는다면 일반 텍스트로 전달해도 됨
```python
# Request speech synthesis
response = client_polly.synthesize_speech(
  Text=text,
  OutputFormat='mp3',
  VoiceId='Matthew'  # You can change the voice here
)


```

# 참고 사이트
- [AWS Cloudwatch get-metric-statistics](https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/get-metric-statistics.html)
- [Integrating CloudWatch with Amazon Polly](https://docs.aws.amazon.com/polly/latest/dg/cloud-watch.html)