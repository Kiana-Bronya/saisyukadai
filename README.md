# saisyukadai
取扱説明書

概要:
このツールは、郵便番号または都市名を入力することで、該当する地域の天気情報と、気温や天候に基づいた服装の提案を表示します。また、リセットボタンを使って、入力と結果を初期化できます。

必要環境:
Python 3.8以上
必須ライブラリ：
PyQt5
requests
google-generativeai
OpenWeather APIキー
Google Gemini APIキー

機能:
郵便番号または都市名で天気と服装提案を取得
郵便番号を入力して該当する地域を検索。
都市名を直接入力して検索。
結果のリセット
リセットボタンを押すと、入力フィールドとすべての結果がクリアされます。

使用方法:
1. ツールを起動

2. 天気と服装提案を取得
郵便番号を入力

入力例：100-0001
「検索」ボタンを押すと、該当する地域の天気と服装提案が表示されます。
都市名を入力

入力例：東京
「検索」ボタンを押すと、入力した都市の天気と服装提案が表示されます。
3. リセット機能
「リセット」ボタンを押すと、以下のフィールドが初期化されます：
郵便番号/都市名入力欄
住所表示
天気情報
服装提案
