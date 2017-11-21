# 参考にした記事: https://qiita.com/kosystem/items/7728e57c70fa2fbfe47c
# このファイルは
#   1. Request Tokenを発行
#   2. Access Tokenを取得
#   3. 取得したトークンをtoken.jsonに保存
# という処理を行う。

from urllib.parse import parse_qsl
from requests import post
from requests_oauthlib import OAuth1
from access_token import read_token, write_access_token
# import webbrowser

consumer_key = read_token()['consumer_key']
consumer_secret = read_token()['consumer_secret']

def oauth_requests():
    # Get request token
    params = {"scope": "read_private,write_private"}
    auth = OAuth1(consumer_key, consumer_secret, callback_uri='oob')
    r = post('https://www.hatena.com/oauth/initiate', data=params, auth=auth)
    request_token = dict(parse_qsl(r.text))

    # サーバー上にプログラムを上げていた関係で、ブラウザで直接開けなかったのでURLを表示する形式とした
    print('%s?oauth_token=%s&perms=delete' % ('https://www.hatena.com/oauth/authorize', request_token['oauth_token']))
    # webbrowser.open('%s?oauth_token=%s&perms=delete' % ('https://www.hatena.com/oauth/authorize', request_token['oauth_token']))  # ブラウザを開きOAuth認証確認画面を表示 ユーザーが許可するとPINコードが表示される

    oauth_verifier = input("Please input PIN code:")
    auth = OAuth1(
        consumer_key,
        consumer_secret,
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        verifier=oauth_verifier)
    r = post('https://www.hatena.com/oauth/token', auth=auth)

    write_access_token(dict(parse_qsl(r.text)))

if __name__ == '__main__':
    oauth_requests()

