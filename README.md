# CrystalDiskInfo to zabbix

CrystalDiskInfo (https://crystalmark.info/ 。以下CDI) の出力をzabbixに送信します。
なお、zabbix_senderは使用しません。

## 使い方

### 設定

設定可能項目は以下の通り。

| 変数名 | 設定例 | 用途 | 
| ZABBIX_SERVER | 192.168.1.123 | Zabbixサーバーのホスト名orIPアドレス。省略不可 |
| ZABBIX_PORT | 10051 | Zabbixサーバーのポート。省略時は10051 |
| ZABBIX_HOST | test | Zabbixホスト名。省略不可 |
| DISKINFO_TXT | C:\My Files\diskinfo.txt | CrystalDiskInfoの出力ファイルのパス |

#### 設定方法

以下の2つの方法があります。同時に行われた場合は、環境変数が優先されます。

##### exportで設定する 

```
set ZABBIX_SERVER=192.168.1.123
set ZABBIX_PORT=10051
set ZABBIX_HOST=test
```

##### .envファイルで設定する

.env.sample ファイルを .env にコピーして内容を編集してください。
注意） .envファイルは存在しなくても動作します。

### 起動

32bit版をお使いの場合は、`DiskInfo64.exe` を `DiskInfo32.exe` に読み替えてください。

```
taskkill /F /IM DiskInfo64.exe
DiskInfo64.exe /Copy
python3 crystaldiskinfo_to_zabbix.py
```

CrystalDiskInfo 8.12.7 の時点ではCDIが起動していると `/Copy` が無視されるため、一度強制終了させています。なお、`/Copy`オプションを使用した場合、出力ファイル名は `DiskInfo.txt` に固定されます。

GUIから操作するのであれば、CDIの `ファイル→保存（テキスト）` で保存されたファイルを入力にします。

## 初回のみ

### 依存関係のインストール

`pip3 install -r requirements.txt`

### Zabbixにテンプレートを登録する

Zabbixの設定 → テンプレート → インポート（右上） を押す
`zabbix_templates/zbx_export_templates.xml` を選択。

### ホストにテンプレートを紐付け

`CrystalDiskInfo to zabbix 20****** by yakumo-saki` テンプレートをホストに紐付け。
（テンプレート名がアレだと思う場合はリネームしてください。）

## FAQ

### Serial Number is hidden. It is not recommended.

* #16 CDIの設定で `機能→シリアルナンバーを隠す ` にチェックを入れているとシリアル番号がファイルにも出力されない。この状態でディスクを接続変更するなどして、CDIがディスクを検出する順番が変わると、zabbix側でデータの連続性が失われる。そのため
`Serial Number is hidden. It is not recommended. （略）` という警告が表示されます。

### 寿命(lifespan) が送信されてこない

* CDIの画面上で寿命が表示されているかご確認ください。正常。とだけ表示されている場合は送信されません。

### Unknown key {key}. Please notify author.

* 新しい項目がCDI側で追加されたようです。Issueにてお知らせください。その際、`DiskInfo.txt` を添付していただくと助かります。（見せたくない項目は削除して構いません）
* 念の為ですが、その項目が無視されるだけで処理は問題なく実行されます。

