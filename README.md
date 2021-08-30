## smart to zabbix

smartctl を使用して取得したSMART情報をZABBIXに送信します。
WindowsとLinuxに対応しています。
外部コマンドとしてsmartctlに依存します。なお、zabbix_senderは使用しません。

## 使い方

`python3 smart_to_zabbix.py`

## （初回のみ）依存関係のインストール

`pip3 install -r requirements.txt`

## 設定方法


## 参考にしたサイト

LLDの応答
`zabbix_get -s 192.168.10.190 -k vfs.fs.discovery | jq`

zabbix公式の説明
https://www.zabbix.com/documentation/current/manual/appendix/items/trapper

py-zabbix （特に Sender.py）
https://github.com/adubkov/py-zabbix

https://www.slideshare.net/takeshiyamane9/lld-zabbix

http://blog.father.gedow.net/2015/12/08/aws-lambda-python-send-metric-value-to-zabbix/

