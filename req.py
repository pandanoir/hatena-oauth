# このファイルが記事一覧の取得のメインとなるファイル
from urllib.parse import parse_qs, urlparse
import xml.etree.ElementTree as ET
import json
from access_token import *

from requests_oauthlib import OAuth1Session

# XML用の名前空間
ns = {
    'ns': 'http://www.w3.org/2005/Atom',
    'app': 'http://www.w3.org/2007/app'
}

def get_next_page(root):
    # 次のページの番号をXMLの中から検索して返す
    return parse_qs(
            urlparse(
                root.find('.//ns:link[@rel="next"]', namespaces=ns).attrib['href']
            ).query
        )['page'][0]


def get_article_list(page=''):
    token = read_token()
    CK = token['consumer_key']
    CS = token['consumer_secret']
    AT = token['access_token']
    AS = token['access_secret']
    auth = OAuth1Session(CK, CS, AT, AS)

    # 結果はXML形式なのでパースして木構造にする
    # (9) アクセストークンを使って記事一覧を取得
    root = ET.fromstring(
            # auth.get('https://blog.hatena.ne.jp/panda_noir/panda-noir.hatenablog.jp/atom/entry', params={'page': page})
            auth.get('https://blog.hatena.ne.jp/{userid}/{blogid}/atom/entry', params={'page': page})
                ._content.decode('utf-8')
        )

    isnt_draft = lambda entry:entry.find('.//app:draft', namespaces=ns).text=='no'

    res = []
    # 下書きも一緒に取得されるので、下書きを取り除く
    for entry in filter(isnt_draft, root.findall('.//ns:entry', namespaces=ns)):
        res.append({
            'title': entry.find('.//ns:title', namespaces=ns).text,
            'href': entry.find('.//ns:link[@rel="alternate"]', namespaces=ns).attrib['href'],
            'category': list(map(lambda x:x.attrib['term'], entry.findall('.//ns:category', namespaces=ns)))
        })

    # 次の一覧ページへのリンクが存在する場合はそのリンクを返す
    if (root.find('.//ns:link[@rel="next"]', namespaces=ns) != None):
        return res, get_next_page(root)
    return res, None

if __name__ == '__main__':
    res, next = get_article_list()
    while next is not None:
        # 最後のページになるまで再帰的に記事一覧を取得する
        _res, next = get_article_list(next)
        res.extend(_res)

    print(json.dumps(res, ensure_ascii=False))

