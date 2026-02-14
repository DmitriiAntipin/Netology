import os
import requests
from flask import Flask, render_template_string
# Установить flask перед запуском


UPLOAD_FOLDER = "uploads"
YANDEX_API_URL = "https://cloud-api.yandex.net/v1/disk/resources"
app = Flask(__name__)


def get_local_files():
    if not os.path.exists(UPLOAD_FOLDER):
        return []
    return [
        f for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]


def get_uploaded_files(token, path="/"):
    headers = {
        "Authorization": f"OAuth {token}"
    }
    uploaded_files = set()
    offset = 0
    limit = 100
    while True:
        params = {
            "path": path,
            "limit": limit,
            "offset": offset
        }
        response = requests.get(
            YANDEX_API_URL,
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
        items = data["_embedded"]["items"]
        if not items:
            break
        for item in items:
            if item["type"] == "file":
                uploaded_files.add(item["name"])
        offset += limit
    return uploaded_files

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Яндекс Диск</title>
</head>
<body>

<h2>Файлы на сервере</h2>

<ul>
{% for file in local_files %}
    <li
        {% if file in uploaded_files %}
            style="background-color: rgba(0, 200, 0, 0.25);"
        {% endif %}
    >
        {{ file }}
    </li>
{% endfor %}
</ul>

</body>
</html>
"""

if __name__ == "__main__":
    token = input("Введите API-ключ Яндекс.Диска: ").strip()
    uploaded_files = get_uploaded_files(token)
    @app.route("/")
    def index():
        local_files = get_local_files()
        return render_template_string(
            HTML_TEMPLATE,
            local_files=local_files,
            uploaded_files=uploaded_files
        )
    app.run(debug=True)
