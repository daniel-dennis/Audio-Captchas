import os
import random
import time
import argparse
import boto3
from google.cloud import texttospeech

import aws_creds # Credentials for AWS
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_key.json' # Credentials for GCP

aws_voices = ['Nicole', 'Russell', 'Amy', 'Emma', 'Brian', 'Raveena', 'Aditi', 'Salli', 'Joanna', 'Ivy', 'Kendra', 'Kimberly', 'Matthew', 'Justin', 'Joey', 'Geraint']
gcp_voices = ['en-AU-Wavenet-A', 'en-AU-Wavenet-B', 'en-AU-Wavenet-C', 'en-AU-Wavenet-D', 'en-GB-Wavenet-A', 'en-GB-Wavenet-B', 'en-GB-Wavenet-C', 'en-GB-Wavenet-D', 'en-IN-Wavenet-A', 'en-IN-Wavenet-B', 'en-IN-Wavenet-C', 'en-US-Wavenet-A', 'en-US-Wavenet-B', 'en-US-Wavenet-C', 'en-US-Wavenet-D', 'en-US-Wavenet-E', 'en-US-Wavenet-F']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', default='charset.txt', type=str)
    parser.add_argument('--length', help='Length of the captcha', default=8, type=int)
    parser.add_argument('--count', help='Amount of captchas to generate', default=10, type=int)
    parser.add_argument('--test_dir', help='Test data directory', default='test', type=str)
    parser.add_argument('--train_dir', help='Train data directory', default='train', type=str)
    args = parser.parse_args()

    if args.symbols is None:
        print('Please specify --symbols to generate')
        exit(1)
    if args.length is None:
        print('Please specify --length to generate')
        exit(1)
    if args.count is None:
        print('Please specify --count to generate')
        exit(1)
    if args.test_dir is None:
        print('Please specify --test_dir to generate')
        exit(1)
    if args.train_dir is None:
        print('Please specify --train_dir to generate')
        exit(1)

    with open(args.symbols, 'r') as symbols_file:
        captcha_symbols = symbols_file.readline().strip()

    polly_client = boto3.Session(
        aws_access_key_id=aws_creds.aws_access_key_id,
        aws_secret_access_key=aws_creds.aws_secret_access_key,
        region_name=aws_creds.region_name
    ).client('polly')

    gcp_client = texttospeech.TextToSpeechClient()

    print('Generating captchas with symbol set {' + captcha_symbols + '}')
    start = time.time()

    for i in range(args.count):
        captcha_text = '›'.join([random.choice(captcha_symbols) for j in range(args.length)])

        if random.randint(1, 5) == 1:
            output_dir = args.test_dir
        else:
            output_dir = args.train_dir 
        
        # Approximately the same amount of voices in each, so keep it simple
        if random.randint(0, 1) == 1:
            tts_aws(polly_client, captcha_text, output_dir)
        else:
            tts_gcp(gcp_client, captcha_text, output_dir)
        
    end = time.time()
    print('Time: %fs, %fs/item' % (end - start, (end - start) / args.length))

def tts_gcp(gcp_client, captcha_text, output_dir):
    if captcha_text[0] == 'A':
        input_text = texttospeech.types.SynthesisInput(text='.' + captcha_text)
    else:
        input_text = texttospeech.types.SynthesisInput(text=captcha_text)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name=gcp_voices[random.randint(0, len(gcp_voices) - 1)],
    )

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3
    )

    response = gcp_client.synthesize_speech(input_text, voice, audio_config)

    with open(os.path.join(output_dir, captcha_text.replace('›', '') + '.mp3'), 'wb') as out:
        out.write(response.audio_content)

def tts_aws(polly_client, captcha_text, output_dir):
    response = polly_client.synthesize_speech(
        VoiceId=aws_voices[random.randint(0, len(aws_voices) - 1)],
        OutputFormat='mp3', 
        Text = captcha_text
    )
    with open(os.path.join(output_dir, captcha_text.replace('›', '') + '.mp3'), 'wb') as out:
        out.write(response['AudioStream'].read())

if __name__ == '__main__':
    main()
