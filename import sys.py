import sys
import requests
import google.generativeai as genai
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget
import re

# 配置 Google Gemini AI
genai.configure(api_key="AIzaSyDidTvQ30-zFttUG4EbErxOf6hsaFSt-_U")
model = genai.GenerativeModel("gemini-1.5-flash")

class ZipcodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("今日の服装は？")
        self.resize(400, 400)

        # ウィジェットの作成
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("郵便番号または都市名を入力してください")
        self.search_button = QPushButton("検索")
        self.reset_button = QPushButton("リセット")
        self.result_label = QLabel("検索結果がここに表示されます", self)
        self.weather_label = QLabel("天気情報がここに表示されます", self)
        self.clothing_label = QLabel("服装提案がここに表示されます", self)

        # レイアウト
        layout = QVBoxLayout()
        layout.addWidget(QLabel("ご入力ください", self))
        layout.addWidget(self.input_field)
        layout.addWidget(self.search_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.weather_label)
        layout.addWidget(self.clothing_label)
        self.setLayout(layout)

        # 信号
        self.search_button.clicked.connect(self.search_weather_and_clothing)
        self.reset_button.clicked.connect(self.reset_fields)

        # OpenWeather API キー
        self.weather_api_key = "188b26bcf81ad0c453a2a0931bf4ad17"

    def validate_zipcode(self, input_text):
        """郵便番号が正しい形式か確認する"""
        return bool(re.fullmatch(r"\d{3}-?\d{4}", input_text))

    def search_weather_and_clothing(self):
        """検索ボタンのクリックイベント"""
        user_input = self.input_field.text().strip()
        if self.validate_zipcode(user_input):
            # 郵便番号の場合
            city_name = self.get_city_from_zipcode(user_input)
            if city_name:
                self.get_weather_and_clothing(city_name)
        else:
            # 直接都市名の場合
            self.result_label.setText(f"入力: {user_input}")
            self.get_weather_and_clothing(user_input)

    def get_city_from_zipcode(self, zipcode):
        """郵便番号から都市名を取得"""
        zipcloud_url = f"http://zipcloud.ibsnet.co.jp/api/search?zipcode={zipcode}"
        try:
            response = requests.get(zipcloud_url)
            response.raise_for_status()
            data = response.json()

            if data['results']:
                result = data['results'][0]
                city_name = result.get('address1', '')  # 都道府県名
                self.result_label.setText(f"住所: {city_name}")
                return city_name
            else:
                self.result_label.setText("該当する住所が見つかりませんでした。")
        except requests.exceptions.RequestException as e:
            self.result_label.setText("住所の取得に失敗しました。")
        return None

    def get_weather_and_clothing(self, city_name):
        """天気情報と服装提案を取得"""
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.weather_api_key}&lang=ja&units=metric"
        try:
            response = requests.get(weather_url)
            response.raise_for_status()
            data = response.json()
            if data:
                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                self.weather_label.setText(f"天気: {weather}, 気温: {temp}°C")
                self.get_clothing_recommendation_with_gemini(temp, weather)
            else:
                self.weather_label.setText("天気情報が取得できませんでした。")
        except requests.exceptions.RequestException as e:
            self.weather_label.setText("天気情報の取得に失敗しました。")

    def get_clothing_recommendation_with_gemini(self, temp, weather):
        """Google Gemini AI を使用して服装提案を生成"""
        prompt = f"現在の天気は {weather}、気温は {temp}°C です。この条件に最適な服装の提案をしてください。"
        try:
            response = model.generate_content(prompt)
            recommendation = response.text if response else "適切な服装の提案が見つかりませんでした。"
            self.clothing_label.setText(f"服装提案: {recommendation}")
        except Exception as e:
            self.clothing_label.setText("服装提案の生成に失敗しました。")

    def reset_fields(self):
        """フィールドをリセット"""
        self.input_field.clear()
        self.result_label.setText("検索結果がここに表示されます")
        self.weather_label.setText("天気情報がここに表示されます")
        self.clothing_label.setText("服装提案がここに表示されます")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ZipcodeApp()
    window.show()
    sys.exit(app.exec())
