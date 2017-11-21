# このファイルは
#   * token.jsonの読み出し
#   * token.jsonへの書き込み
# を行う。

import json
def read_token():
    with open('token.json', 'r') as f:
        res = json.load(f)
    return res

def write_access_token(access_token):
    token = read_token()
    consumer_key = token['consumer_key']
    consumer_secret = token['consumer_secret']
    with open('token.json', 'w') as fh:
        fh.write(json.dumps({
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token['oauth_token'],
            "access_secret": access_token['oauth_token_secret']
        }))
