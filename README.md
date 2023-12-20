streamlingファイルには、３つのファイルが入っています。

<h3>requirements.txt</h3>
以下のコードを実行するときに必要なモジュールが書いてあります。

ターミナル上でこのテキストファイルが置いてあるディレクトリで、<br><br>
pip install -r requirements.txt<br><br>
と実行すればまとめてインストールできます。<br><br><br>

<h3>audio.py</h3>
使用するaudioのindexを調べるためのコードです。<br><br><br>

<h3>streaming.py</h3>
google cloud speech-to-text APIを利用してリアルタイムなストリーミングができるコードです。<br><br>
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your/json/path'には、jsonファイルのパスを入れてください。<br>
input_device_indexは使用するaudioのインデックス番号を入れてください。インデックス番号はaudio.pyを実行すれば確認できると思います。<br>
話者識別機能があるため、話者の人数に合わせて数値を調整してください。<br><br><br>


jsonファイルは下のURLから取得してください<br>
https://console.cloud.google.com/iam-admin/serviceaccounts?hl=ja&project=engaged-wonder-390709
