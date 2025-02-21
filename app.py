from telethon import TelegramClient, events, functions, types
from telethon.errors import FloodWaitError
import random
from calculate_sha256 import calculate_sha256
from custom_print import custom_print
import json
import asyncio
from dotenv import load_dotenv
import os
import time
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
import uvicorn
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
# app.debug = True
asgi_app = WsgiToAsgi(app)

load_dotenv()  # Load environment variables from .env file
# groupData = os.getenv("GROUP_NAME")
groupData = []

with open("env.json", "r") as f:
    env_json = json.load(f)

messageItemHashmap = {}
messages = []
emotions = [
    "👍",
    "❤️",
    "🔥",
    "🥰",
    "👏",
    "😁",
    "🤔",
    "🤯",
    "😱",
    "🤬",
    "😢",
    "🎉",
    "🤩",
    "🤮",
    "💩",
    "🙏",
]
FLAG_BOT_WORK = False


def sync_sheet_data():
    global messages, groupData
    url = "https://docs.google.com/spreadsheets/d/1O79bkFEgeWwPSBr3jT2GtoYnXzf4Db8sps-0NsBBGMI/export?format=csv"
    df = pd.read_csv(url)
    data = df.values
    messages = [
        {
            "gender": d[0],
            "message": d[1],
            "replies": [d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10], d[11], d[12]],
        }
        for d in data
    ]

    url = "https://docs.google.com/spreadsheets/d/1O79bkFEgeWwPSBr3jT2GtoYnXzf4Db8sps-0NsBBGMI/export?format=csv&gid=491177587"
    df = pd.read_csv(url)
    data = df.values
    groupData = [
        {
            "name": d[0],
            "timeout": int(d[1]),
            "reply_timeout": int(d[2]),
            "reply_limit": int(d[3]),
        }
        for d in data
    ]


sync_sheet_data()


def get_message_item(gender="Male"):
    messageItem = messages[random.randint(0, len(messages) - 1)]
    if messageItem["gender"].strip().lower() != gender.strip().lower():
        return get_message_item(gender)
    return messageItem


async def message_handler(client, event, session_name):
    # if event.message.text.startswith("/react"):
    if not FLAG_BOT_WORK:
        return
    try:
        id = str(event.sender_id)
        message = event.message.text
        try:
            chat_name = (
                f"@{event.chat.username}"
                if hasattr(event.chat, "username") and event.chat.username
                else "No username"
            )
        except Exception as e:
            chat_name = "Unknown"
        hash = calculate_sha256(id + message)
        if hash in messageItemHashmap:
            messageItem = messageItemHashmap[hash]
            if session_name in messageItem["replying_session_names"]:
                index = messageItem["replying_session_names"].index(session_name)
                timeout = messageItem["reply_timeout"] * (index + 1)
                reply_msg = str(messageItem["messageItem"]["replies"][index])
                origin_session_name = messageItem["session_name"]
                if not reply_msg == "nan":
                    custom_print(f"Waiting for replying message: {session_name}")
                    await asyncio.sleep(timeout)
                    await event.reply(reply_msg)
                    custom_print(
                        f"Client {session_name} replied in group: {chat_name}, id: {id}, {origin_session_name}'s msg ==>: {message} ==> with this reply_msg: {reply_msg}"
                    )
                # if index == messageItem["reply_limit"] - 1:
                #     del messageItemHashmap[hash]
    except Exception as e:
        custom_print(f"Error when replying: {e}")
    # if random.randint(0, 100) < 5:
    #     await asyncio.sleep(random.randint(8, 20))
    #     custom_print(f"React to: {event.message.text}")  # Print the message text for debugging
    #     try:
    #         await client(
    #             functions.messages.SendReactionRequest(
    #                 peer=event.chat_id,
    #                 msg_id=event.message.id,
    #                 reaction=[
    #                     types.ReactionEmoji(
    #                         emoticon=emotions[random.randint(0, len(emotions) - 1)]
    #                     )
    #                 ],
    #             )
    #         )
    #         await event.reply(get_message())
    #     except Exception as e:
    #         custom_print(f"Error sending reaction: {e}")
    # else:
    #     sender = await event.get_sender()
    #     custom_print(f"New message from {sender.username}: {event.message.text}")
    # replied_msg = await event.get_reply_message()
    # if replied_msg:
    #     await replied_msg.reply("This is a reply to your message!")


async def main():
    clients = []
    for client_item in env_json:
        custom_print(f"Starting: {client_item["phone_number"]}")
        clients.append(
            {
                "session_name": client_item["session_name"],
                "gender": client_item["gender"],
                "client": TelegramClient(
                    client_item["session_name"],
                    client_item["api_id"],
                    client_item["api_hash"],
                ),
            }
        )

    # Define a function to attach the event handler to a client
    def attach_handler(client, session_name):
        @client.on(
            events.NewMessage(
                incoming=True, chats=[group["name"] for group in groupData]
            )
        )
        async def handler(event):
            await message_handler(client, event, session_name)

    # # Attach the handler to each client
    for client in clients:
        attach_handler(client["client"], client["session_name"])

    # Run all clients
    async def run_client(client, gender, session_name, client_index):
        try:
            async with client:
                await asyncio.sleep(
                    client_index * 1800 + random.randint(0, 60)
                )  # TODO: uncomment this in production
                me = await client.get_me()
                id = str(me.id)
                custom_print(
                    f"Client {client.session.filename} is started, working as {me.first_name}, id: {id}"
                )
                # await asyncio.Future()  # Keep the client
                # group = await client.get_entity(groupNames)
                # groups = [await client.get_entity(groupName) for groupName in groupNames]
                groups = [
                    {
                        "name": group["name"],
                        "group": await client.get_entity(group["name"]),
                        "timeout": group["timeout"],
                        "reply_timeout": group["reply_timeout"],
                        "reply_limit": group["reply_limit"],
                        "prev_timestamp": 0,
                    }
                    for group in groupData
                ]
                while True:
                    await asyncio.sleep(5)
                    for i in range(len(groups)):
                        groups[i]["timeout"] = groupData[i]["timeout"]
                        groups[i]["reply_timeout"] = groupData[i]["reply_timeout"]
                        groups[i]["reply_limit"] = groupData[i]["reply_limit"]
                    custom_print(
                        f"{client.session.filename} is looping... read from synced data..."
                    )
                    for group_item in groups:
                        try:
                            await asyncio.sleep(5)
                            if not FLAG_BOT_WORK:
                                continue
                            current_time = int(time.time())
                            prev_timestamp = group_item["prev_timestamp"]
                            timeout = group_item["timeout"] + random.randint(0, 300)

                            if (
                                prev_timestamp != 0
                                and (current_time - prev_timestamp) < timeout
                            ):
                                continue

                            custom_print(
                                f"group name: {group_item['name']}, prev_timestamp: {prev_timestamp}, current_time: {current_time}, timeout: {timeout}"
                            )

                            async with client.action(group_item["group"].id, "typing"):
                                await asyncio.sleep(random.randint(3, 10))
                                messageItem = get_message_item(gender)
                                message = messageItem["message"]

                                replying_session_names = set()
                                for i in range(group_item["reply_limit"]):
                                    if str(messageItem["replies"][i]) == "nan":
                                        break
                                    len_clients = len(clients)
                                    while True:
                                        index = random.randint(0, len_clients - 1)
                                        choosen_client = clients[index]
                                        if (
                                            choosen_client["gender"]
                                            == messageItem["gender"]
                                            and session_name
                                            != choosen_client["session_name"]
                                        ):
                                            replying_session_names.add(
                                                choosen_client["session_name"]
                                            )
                                            break

                                messageItemHashmap[calculate_sha256(id + message)] = {
                                    "session_name": session_name,
                                    "messageItem": messageItem,
                                    "reply_timeout": group_item["reply_timeout"],
                                    "reply_limit": group_item["reply_limit"],
                                    "replying_session_names": list(
                                        replying_session_names
                                    ),
                                }

                                await client.send_message(group_item["group"], message)
                                custom_print(
                                    f"Client {client.session.filename} sent message into group: {group_item["name"]}: {message}, replying_session_names: {replying_session_names}"
                                )
                            group_item["prev_timestamp"] = int(time.time())
                            await asyncio.sleep(10)  # Non-blocking sleep
                        except Exception as e:
                            custom_print(
                                f"Error sending message from {client.session.filename}: {e}"
                            )
                            group_item["prev_timestamp"] = int(time.time())
                            await asyncio.sleep(30)  # Wait longer if there is an error.

        except FloodWaitError as e:
            custom_print(f"Client {client.session.filename} FloodWaitError: {e}")
            await asyncio.sleep(e.seconds)  # Wait for the specified time
        except Exception as e:
            custom_print(f"Client {client.session.filename} encountered an error: {e}")

    tasks = [
        run_client(client["client"], client["gender"], client["session_name"], index)
        for index, client in enumerate(clients)
    ]
    await asyncio.gather(*tasks)


@app.route("/")
def index():
    return render_template("index.html", FLAG_BOT_WORK=FLAG_BOT_WORK)


@app.route("/start")
def start():
    global FLAG_BOT_WORK
    FLAG_BOT_WORK = True
    return redirect("/")


@app.route("/stop")
def stop():
    global FLAG_BOT_WORK
    FLAG_BOT_WORK = False
    return redirect("/")


@app.route("/sync")
def sync():
    sync_sheet_data()
    return redirect("/")


async def run_server():
    config = uvicorn.Config(asgi_app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()


async def start_main():
    await asyncio.gather(main(), run_server())


if __name__ == "__main__":
    asyncio.run(start_main())
