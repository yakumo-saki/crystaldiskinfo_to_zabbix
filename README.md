# NOT FINISHED YET

this is under heavy development

# smart to zabbix

smartctl を使用して取得したSMART情報をZABBIXに送信します。
WindowsとLinuxに対応しています。
外部コマンドとしてsmartctlに依存します。なお、zabbix_senderは使用しません。

## 使い方

### 設定

環境変数(TBD)

### 起動

`python3 smart_to_zabbix.py`

## 初回のみ

### 依存関係のインストール

`pip3 install -r requirements.txt`
（今の所依存関係はありません。スキップしてOK）

### Zabbixにテンプレートを登録する

Zabbixの設定 → テンプレート → インポート（右上） を押す
`zabbix_templates/zbx_export_templates.xml` を選択。

### ホストにテンプレートを紐付け

`smart_to_zabbix by yakumo-saki` テンプレートをホストに紐付け。
（テンプレート名がアレだと思う場合はリネームしてください。）

## 参考にしたサイト

LLDの応答
`zabbix_get -s 192.168.10.190 -k vfs.fs.discovery | jq`

zabbix公式の説明
https://www.zabbix.com/documentation/current/manual/appendix/items/trapper

py-zabbix （特に Sender.py）
https://github.com/adubkov/py-zabbix

https://www.slideshare.net/takeshiyamane9/lld-zabbix

http://blog.father.gedow.net/2015/12/08/aws-lambda-python-send-metric-value-to-zabbix/

ESP-WROOM-02からZabbixサーバーにZabbix senderプロトコルでデータを送信する
（データ送信時の形式について参考にさせていただきました）
https://qiita.com/mutz0623/items/2c7eae0f762d760875bb