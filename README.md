streamlingファイルには、３つのファイルが入っています。

<h3>requirements.txt</h3>
以下のコードを実行するときに必要なモジュールが書いてあります。

ターミナル上でこのテキストファイルが置いてあるディレクトリで、<br><br>
pip install -r requirements.txt<br><br>
と実行すればまとめてインストールできます。

<h3>audio.py</h3>
使用するaudioのindexを調べるためのコードです。

<h3>streaming.py</h3>
google cloud speech-to-text APIを利用してリアルタイムなストリーミングができるコードです。<br>
話者識別機能があるため、話者の人数に合わせて数値を調整してください。<br>
input_device_indexは、使用するaudioのインデックス番号を入れてください。インデックス番号はaudio.pyを実行すれば確認できると思います。

jsonファイルは下のURLから取得してください<br>
https://console.cloud.google.com/iam-admin/serviceaccounts?hl=ja&project=engaged-wonder-390709
