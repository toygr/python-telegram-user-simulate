from telethon import TelegramClient, events, functions, types
from telethon.errors import FloodWaitError
import random
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
    # data = np.delete(data, 0, axis=0)
    data = [d[1] for d in data]
    messages = data

    url = "https://docs.google.com/spreadsheets/d/1O79bkFEgeWwPSBr3jT2GtoYnXzf4Db8sps-0NsBBGMI/export?format=csv&gid=491177587"
    df = pd.read_csv(url)
    data = df.values
    # data = np.delete(data, 0, axis=0)
    groupData = [{"name": d[0], "timeout": d[1]} for d in data]


sync_sheet_data()


def get_message():
    return messages[random.randint(0, len(messages) - 1)]


async def message_handler(client, event):
    # if event.message.text.startswith("/react"):
    if not FLAG_BOT_WORK:
        return
    if random.randint(0, 100) < 5:
        await asyncio.sleep(random.randint(8, 20))
        print(f"React to: {event.message.text}")  # Print the message text for debugging
        try:
            await client(
                functions.messages.SendReactionRequest(
                    peer=event.chat_id,
                    msg_id=event.message.id,
                    reaction=[
                        types.ReactionEmoji(
                            emoticon=emotions[random.randint(0, len(emotions) - 1)]
                        )
                    ],
                )
            )
            # await event.reply(get_message())
        except Exception as e:
            print(f"Error sending reaction: {e}")
    # else:
    #     sender = await event.get_sender()
    #     print(f"New message from {sender.username}: {event.message.text}")
    # replied_msg = await event.get_reply_message()
    # if replied_msg:
    #     await replied_msg.reply("This is a reply to your message!")


async def main():
    clients = []
    for client_item in env_json:
        print(f"Starting: {client_item["phone_number"]}")
        clients.append(
            TelegramClient(
                client_item["session_name"],
                client_item["api_id"],
                client_item["api_hash"],
            )
        )

    # Define a function to attach the event handler to a client
    def attach_handler(client):
        @client.on(
            events.NewMessage(
                incoming=True, chats=[group["name"] for group in groupData]
            )
        )
        async def handler(event):
            await message_handler(client, event)

    # Attach the handler to each client
    for client in clients:
        attach_handler(client)

    # Run all clients
    async def run_client(client):
        await asyncio.sleep(random.randint(0, 60)) # TODO: uncomment this in production
        # groups = await asyncio.gather(
        #     *[
        #         {
        #             "group": await client.get_entity(group["name"]),
        #             "timeout": group["timeout"],
        #             "prev_timestamp": 0,
        #         }
        #         for group in groupData
        #     ],
        #     return_exceptions=True,
        # )
        try:
            async with client:
                me = await client.get_me()
                print(
                    f"Client {client.session.filename} is started, working as {me.first_name}"
                )
                # await asyncio.Future()  # Keep the client
                # group = await client.get_entity(groupNames)
                # groups = [await client.get_entity(groupName) for groupName in groupNames]
                groups = [
                    {
                        "group": await client.get_entity(group["name"]),
                        "timeout": group["timeout"],
                        "prev_timestamp": 0,
                    }
                    for group in groupData
                ]
                while True:
                    try:
                        for group_item in groups:
                            if not FLAG_BOT_WORK:
                                await asyncio.sleep(30)
                                continue
                            current_time = int(time.time())
                            prev_timestamp = group_item["prev_timestamp"]
                            timeout = group_item["timeout"] + random.randint(0, 300)

                            if (
                                prev_timestamp != 0
                                and (current_time - prev_timestamp) < timeout
                            ):
                                await asyncio.sleep(5)
                                continue
                            async with client.action(group_item["group"].id, "typing"):
                                await asyncio.sleep(random.randint(3, 10))
                                message = get_message()
                                await client.send_message(
                                    group_item["group"], get_message()
                                )
                                print(
                                    f"Client {client.session.filename} sent message: {message}"
                                )
                                group_item["prev_timestamp"] = int(time.time())
                            await asyncio.sleep(10)  # Non-blocking sleep
                    except Exception as e:
                        print(
                            f"Error sending message from {client.session.filename}: {e}"
                        )
                        await asyncio.sleep(60)  # Wait longer if there is an error.

        except FloodWaitError as e:
            print(f"Client {client.session.filename} FloodWaitError: {e}")
            await asyncio.sleep(e.seconds)  # Wait for the specified time
        except Exception as e:
            print(f"Client {client.session.filename} encountered an error: {e}")

    tasks = [run_client(client) for client in clients]
    await asyncio.gather(*tasks)

@app.route('/')
def index():
    return render_template('index.html', FLAG_BOT_WORK = FLAG_BOT_WORK)

@app.route('/start')
def start():
    global FLAG_BOT_WORK
    FLAG_BOT_WORK = True
    return redirect('/')

@app.route('/stop')
def stop():
    global FLAG_BOT_WORK
    FLAG_BOT_WORK = False
    return redirect('/')

@app.route('/sync')
def sync():
    sync_sheet_data()
    return redirect('/')


async def run_server():
    config = uvicorn.Config(asgi_app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()
    

async def start_main():
    await asyncio.gather(main(), run_server())

if __name__ == "__main__":
    asyncio.run(start_main())