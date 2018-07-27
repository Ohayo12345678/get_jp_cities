# Get-JP-cities library

English document is in the file.


## RESAS-APIを利用して市区町村マスタを作るための支援モジュールです。

    [["01101", "札幌市中央区", "北海道", "北海道・東北"], ["01102", "札幌市北区", "北海道", "北海道・東北"], ..., ["47382", "与那国町", "沖縄県", "九州・沖縄"]]

というようなネストのリストを取得できます。



#### 使い方

取得方法は３つ用意しました。


##### コマンドラインから実行してjsonファイルを作る
    python get_jp_cities Your_api_key
ファイル名は'jp_cities.json'です。
Pythonでプログラミングしない方でもインタプリタとRequestsパッケージが入っていれば、
jsonファイルが取得可能です。


##### 他のモジュールでインポートして、jsonファイルを作る
    import get_jp_cities
    get_jp_cities.get_json(file_name='name_as_you_like.json', api_key='Your_api_key')


##### 他のモジュールでインポートして、tupleを変数で受ける
    import get_jp_cities
    jp = get_jp_cities.get_tuple(api_key='Your_api_key')



#### RESAS-APIについて：
    RESAS-APIは内閣府が提供しているサービスです。
    利用には登録が必要です（簡単でした）。
    https://opendata.resas-portal.go.jp/docs/api/v1/index.html


#### Note：
    RESAS-APIのアクセス制限を回避するためのウェイトが仕込んであるので
    実行には数秒かかることをご承知おきください。


#### 依存パッケージ：
    Requests HTTP Library (c) 2017 by Kenneth Reitz.

#### ライセンス：
    Apache 2.0です。

