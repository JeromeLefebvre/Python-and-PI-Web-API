
import json
import getpass

import requests as r
# PI Web APIのリクエストはHTTPSが必要ですが、
# テストの環境では、PI Web APIのサーバーに自己署名証明書しかないことが多いです。
# この場合、HTTPSのリクエストをするとrequestsのパッケージか警告またはエラーが発生します。
# 下記の行は警告を無視するためです。
r.packages.urllib3.disable_warnings()

# PI Web APIのサーバー名を記入してください。
piwebapi_server = ''
base_url = 'https://' + piwebapi_server + '/piwebapi/'

# PI Web APIにて認証は三種類ありますが、このポストではKerberosについては言及しません。
# Basic認識を使う場合はユーザー名とパスワードを送る必要があります。
# Anonymousを使う場合は下記のように空白でよいです。
user = ''
_password = ''


def password():
    global _password
    if _password == '':
        _password = getpass.getpass('please type in your password: ')
    return _password


def pi_request(request, action, parameters={}, debug=False):
    # pi_requestsの関数は変数として：
    # requestにrequests.get、requests.updateなどの関数
    # actionにelement、assetdatabasessetなどのController（Method)名か
    # controler名/webidのリソース名
    # parametersに"Url Parameters"を設定する

    # verify=Falseのパラメーターは自己署名証明書しかない環境では
    # エラーを発生させないためのパラメーターです。
    response = request(url=base_url + action,
                       params=parameters,
                       verify=False,
                       auth=(user, password()))
    # エラーが発生すると、レスポンスのヘッダーなどを見て何かあったと分かるケースが多いので、
    # pi_get_requests(action, parameters={}, debug=True)と実行するとレスポンスの情報を出力します。
    if debug:
        # レスポンスなどを出力する
        print('デバッグのための情報です')
        print('{0: <10} {1}'.format('url:', response.url))
        print('{0: <10} {1}'.format('status:', response.status_code))
        print('{0: <10} {1}'.format('reason:   ', response.reason))
        print('{0: <10} '.format('headers:'))
        for key in response.headers:
            print('     {0: <17} {1}'.format(key + ':', response.headers[key]))
        #
        # print('{0: <10} {1}'.format('text:'), response.text)
    # Deleteの様なrequestsから空白の時列しかもられないので、
    # この場合はloadsの関数にエラーが発生する。
    try:
        return json.loads(response.text)
    except json.decoder.JSONDecodeError:
        # 内容がない場合は
        return ''


def pprint(response):
    # pi_get_requestsを綺麗に出力するため
    print(json.dumps(response, indent=4, sort_keys=True))


# piwebapi/help/controllers/assetdatabase/actions/getelementsによると
# あるデータベースのエレメントを収集したい場合は下記の様に収集できます。
# GET assetdatabases/{webId}/elements
af_server = ''
af_database = 'DB'
parameters = {'path': r'\\' + af_server + '\\' + af_database}
pump_db_web_Id = pi_request(r.get, 'assetdatabases', parameters, debug=True)['WebId']

# 以上のデータベースを削除する
pi_request(r.delete, 'assetdatabases/' + str(pump_db_web_Id), debug=True)
