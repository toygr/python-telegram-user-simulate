from datetime import datetime


def custom_print(data):
    print(data)
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {data}\n")
