# -*- coding=utf-8 -*-
# @Time:7/4/2025 下午 9:04
# @Author:席灏铖
# @File:run_with_ngrok.PY
# @Software:PyCharm

from flask import Flask
from pyngrok import ngrok

# 你的 Flask 应用文件名
from app import app


def main():
    # 开启 ngrok 隧道
    public_url = ngrok.connect(5000)
    print(" * The ngrok tunnel is enabled, and the public IP address：", public_url)

    # Flask 用本地方式运行，ngrok 会自动转发
    app.run(debug=True, use_reloader=False)  # 不要传 port 参数


if __name__ == '__main__':
    main()
