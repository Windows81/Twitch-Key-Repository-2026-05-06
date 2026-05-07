import functools
import subprocess
import requests
import json
import re

CLIENT_IDEN = '71vq0git2hubkomm7jm6cyyjs4r603'
CLIENT_SECRET = '6ebtp63bm8o0jpfc9xy0ytygukrnhw'


@functools.cache
def fetch_auth() -> str:
    '''
    https://stackoverflow.com/a/75800617/6879778
    '''

    url = 'https://id.twitch.tv/oauth2/token'
    payload = {
        'client_id': CLIENT_IDEN,
        'client_secret': CLIENT_SECRET,
        'grant_type':  'client_credentials',
    }
    response = requests.post(url, json=payload)
    return json.loads(response.text)['access_token']


def get_follower_count(iden: int) -> int:
    headers = {
        'Authorization': f'Bearer {fetch_auth()}',
        'Client-Id': CLIENT_IDEN,
    }
    url = f'https://api.twitch.tv/helix/channels/followers?broadcaster_id={iden}'

    response = requests.get(url, headers=headers)
    return json.loads(response.text).get('total', 0)


def get_username(iden: int) -> str:
    headers = {
        'Authorization': f'Bearer {fetch_auth()}',
        'Client-Id': CLIENT_IDEN,
    }
    url = f'https://api.twitch.tv/helix/channels?broadcaster_id={iden}'

    response = requests.get(url, headers=headers)
    return json.loads(response.text)['data'][0]['broadcaster_name']


tokens = set()
while True:
    text = input()
    if not text:
        break
    match = re.search(r'live_[0-9]{7,10}_[a-zA-Z0-9]{20,}', text)
    if not match:
        continue
    tokens.add(match.group(0))

for token in tokens:
    split = token.split('_')
    if len(split) != 3:
        continue

    output = subprocess.run(
        f'ffmpeg -f lavfi -i color=black -c copy -f flv rtmp://live.twitch.tv/app/{token}',
        stderr=subprocess.PIPE,
    ).stderr

    if b'Function not implemented' not in output:
        continue

    iden = int(split[1])
    followers = get_follower_count(iden)
    print()
    print(f'{token:50s} - followed by {followers}')
    username = get_username(iden)
    print(f'{token:50s} - username is {username}')
