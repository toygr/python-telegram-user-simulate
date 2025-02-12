from telethon import TelegramClient, events, functions, types
import time
import random
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
groupName = os.getenv("GROUP_NAME")

with open("env.json", "r") as f:
    env_json = json.load(f)
# PHONE_NUMBER = +1 828 374 3717
API_ID = "29030505"
API_HASH = "c72a1e40b4025bd304451442f11af39d"
SESSION_NAME = "session7"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

messages = [
    "I used to be addicted to soap, but I'm clean now.Why don't scientists trust atoms? Because they make up everything!",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "What do you call a fake noodle? An impasta!",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "I'd tell you a chemistry joke, but I know I wouldn't get a reaction.",
    "Why don't eggs tell jokes? They'd crack each other up.",
    "What do you call an alligator wearing a vest? An investigator.",
    "Why does a chicken coop always have two doors? Because if it had four doors it would be a chicken sedan!",
    "Who is the roundest knight at King Arthur's table? Sir Cumference.",
    "What time does Sean Connery arrive at Wimbledon? Tennish.",
    "I never wanted to believe that my dad was stealing from his job as a road worker. But when I got home, all the signs were there.",
    "How did the hipster burn his mouth? He ate his dinner before it was cool.",
    "What do you call a Frenchman wearing sandals? Philippe Philoppe.",
    "Two goldfish are in a tank. One turns to the other and says, Do you know how to drive this thing?",
    "What did the Buddhist monk say to the hot dog vendor? Make me one with everything.",
    "If you visit the National Air and Space Museum you might think the title is misleading, because it is actually full of stuff.",
    "Did you take a bath today? No. Is one missing?",
    "What do you get when you cross a cow and a duck? Milk and quackers.",
    "What's the difference between an egg and a skunk? If you don't know, remind me never to send you to buy eggs.",
    "What must you do before getting off a bus? Get on it.",
    "I'm on a seafood diet. I see food and I eat it.",
    "Why did the math book look so sad? Because it had too many problems.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "What do you call a bear with no teeth? A gummy bear.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call a parade of rabbits hopping backwards? A receding hare-line.",
    "Why don't scientists trust stairs? Because they're always up to something.",
    "What do you call a boomerang that doesn't come back? A stick.",
    "Why did the invisible man turn down the job offer? He couldn't see himself doing it.",
    "What do you call a can opener that doesn't work? A can't opener.",
    "Why did the gym close down? It just didn't work out.",
    "What do you call a fake stone in Ireland? A sham rock.",
    "Why don't eggs tell jokes? They'd crack each other up.",
    "What do you call a sleeping bull? A bulldozer.",
    "Why did the scarecrow become a successful motivational speaker? He was outstanding in his field.",
    "What do you call a fish wearing a bowtie? Sofishticated.",
    "Why don't scientists trust atoms? Because they make up everything.",
    "I told my computer I needed a break, and now it won't stop sending me Kit-Kats.",
    "I tried to organize a hide-and-seek tournament, but good players are so hard to find.",
    "My dog used to chase people on a bike. It got so bad, I had to take his bike away.",
    "I'm on a seafood diet. I see food, and I eat it.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "I'm reading a book on anti-gravity. It's impossible to put down.",
    "I used to be a baker, but I couldn't make enough dough.",
    "I told my friends I had a pun about ghosts, but it was too boo-ring.",
    "I'm friends with 25 letters of the alphabet. I don't know Y.",
    "I asked my gym trainer if I could do aerobics in the water. He said, “Deep water?” I said, “Yes.” He said, “How deep?” I said, “Water you talking about?”",
    "I told my boss I needed a raise because I was struggling to make ends meet. He said, “What ends?” I said, “The ones at the beginning of the month.”",
    "I tried to catch fog yesterday. Mist.",
    "I told my cat a joke. It was purr-fectly hilarious.",
    "I'm so good at sleeping, I can do it with my eyes closed.",
    "I told my plants a joke. They didn't laugh, but they did photosynthesize a little harder.",
    "I used to play piano by ear, but now I use my hands.",
    "I told my phone I needed space. Now it won't stop sending me pictures of the moon.",
    "I tried to write a joke about time travel, but no one got it.",
    "I told my math book I had problems. It said, “Don't worry, I've got plenty.”",
    "I'm writing a book on reverse psychology. Please don't buy it.",
    "I told my mirror I was the fairest of them all. It cracked. Fair enough.",
    "I tried to make a belt out of watches, but it was a waist of time.",
    "I told my shoes I needed a break. Now they're loafers.",
    "I'm so good at multitasking, I can waste time and procrastinate at the same time.",
    "I told my calendar I needed a date. It said, “Sorry, I'm all booked.”",
    "I tried to make a joke about a broken pencil, but it was pointless.",
    "I told my bed I was tired. It said, “Lie down, I've got you covered.”",
    "I'm so lazy, I put a stop sign at the end of my driveway so I don't have to leave.",
    "I told my car I needed a break. It said, “Brake? I thought you'd never ask.”",
    "I tried to make a joke about a clock, but it was too time-consuming.",
    "I told my fridge I was hungry. It said, “Cool story, bro.”",
    "I'm so indecisive, I can't even decide if I'm indecisive.",
    "I told my plants to grow up. Now they're acting all high and mighty.",
    "I tried to make a joke about a skeleton, but it didn't have the guts.",
    "I told my phone I needed a break. Now it's ghosting me.",
    "I'm so good at yoga, I can stretch the truth without breaking a sweat.",
    "I told my shoes to tie themselves. They said, “We're laced up, but we're not miracle workers.”",
    "I tried to make a joke about a calendar, but it was too dated.",
    "I told my dog to stop barking. He said, “I'm not barking, I'm just talking in dog language.”",
    "I'm so good at cooking, I can burn water without even trying.",
    "I told my plants to stop being so clingy. Now they're giving me the silent treatment.",
    "I tried to make a joke about a mirror, but it was too reflective.",
    "I told my bed I needed a hug. It said, “I've got you covered.”",
    "I'm so good at sleeping, I can do it in my dreams.",
    "I told my car to stop being so dramatic. It said, “I'm just tired of your backseat driving.”",
    "I tried to make a joke about a tree, but it was too sappy.",
    "I told my fridge to stop being so cold. It said, “Chill out.”",
    "I'm so good at procrastinating, I'll finish this list later.",
    "I told my plants to stop being so shady. They said, “We're just trying to photosynthesize.”",
    "I tried to make a joke about a pencil, but it was too sharp.",
    "I told my shoes to stop being so sneaky. They said, “We're just trying to walk a mile in your shoes.”",
    "I'm so good at multitasking, I can ignore you while scrolling through my phone.",
    "I told my bed to stop being so soft. It said, “I'm just trying to cushion your fall.”",
    "I tried to make a joke about a clock, but it was too tick-tock.",
    "I told my plants to stop being so green. They said, “We're just trying to leaf you alone.”",
    "I'm so good at cooking, I can make a microwave cry.",
    "I told my car to stop being so loud. It said, “I'm just trying to rev up your day.”",
    "I tried to make a joke about a mirror, but it was too vain.",
    "I told my fridge to stop being so cold. It said, “I'm just trying to keep my cool.”",
    "I'm so good at sleeping, I can do it with my eyes open.",
    "I told my plants to stop being so clingy. They said, “We're just trying to stick together.”",
    "I tried to make a joke about a tree, but it was too rooted in reality.",
    "I told my shoes to stop being so sneaky. They said, “We're just trying to step up our game.”",
    "I'm so good at procrastinating, I'll finish this sentence later.",
    "I told my bed to stop being so soft. It said, “I'm just trying to cushion your fall.”",
    "I tried to make a joke about a clock, but it was too time-sensitive.",
    "I told my plants to stop being so green. They said, “We're just trying to leaf you alone.”",
    "I'm so good at cooking, I can make a microwave cry.",
    "I told my car to stop being so loud. It said, “I'm just trying to rev up your day.”",
    "I tried to make a joke about a mirror, but it was too reflective.",
    "I told my fridge to stop being so cold. It said, “I'm just trying to keep my cool.”",
    "I'm so good at sleeping, I can do it with my eyes open.",
    "I told my plants to stop being so clingy. They said, “We're just trying to stick together.”",
    "I tried to make a joke about a tree, but it was too rooted in reality.",
    "I told my shoes to stop being so sneaky. They said, “We're just trying to step up our game.”",
    "I'm so good at procrastinating, I'll finish this sentence later.",
    "I told my bed to stop being so soft. It said, “I'm just trying to cushion your fall.”",
    "I tried to make a joke about a clock, but it was too time-sensitive.",
    "I told my plants to stop being so green. They said, “We're just trying to leaf you alone.”",
    "I'm so good at cooking, I can make a microwave cry.",
    "I told my car to stop being so loud. It said, “I'm just trying to rev up your day.”",
    "I tried to make a joke about a mirror, but it was too reflective.",
    "I told my fridge to stop being so cold. It said, “I'm just trying to keep my cool.”",
    "I'm so good at sleeping, I can do it with my eyes open.",
    "I told my plants to stop being so clingy. They said, “We're just trying to stick together.”",
    "I tried to make a joke about a tree, but it was too rooted in reality.",
    "I told my shoes to stop being so sneaky. They said, “We're just trying to step up our game.”",
    "I'm so good at procrastinating, I'll finish this sentence later.",
    "I told my bed to stop being so soft. It said, “I'm just trying to cushion your fall.”",
    "I tried to make a joke about a clock, but it was too time-sensitive.",
    "I told my plants to stop being so green. They said, “We're just trying to leaf you alone.”",
    "I'm so good at cooking, I can make a microwave cry.",
    "I told my car to stop being so loud. It said, “I'm just trying to rev up your day.”",
    "I tried to make a joke about a mirror, but it was too reflective.",
    "I told my fridge to stop being so cold. It said, “I'm just trying to keep my cool.”",
    "I'm so good at sleeping, I can do it with my eyes open.",
    "I told my plants to stop being so clingy. They said, “We're just trying to stick together.”",
    "I tried to make a joke about a tree, but it was too rooted in reality.",
    "I told my shoes to stop being so sneaky. They said, “We're just trying to step up our game.”",
    "I'm so good at procrastinating, I'll finish this list later.",
]


# @client.on(events.NewMessage(chats=groupName, pattern='/react'))
@client.on(events.NewMessage(incoming=True, chats=groupName))
async def handler(event):
    if event.message.text.startswith("/react"):
        print(f"React to: {event.message.text}")  # Print the message text for debugging
        try:
            await client(
                functions.messages.SendReactionRequest(
                    peer=event.chat_id,
                    msg_id=event.message.id,
                    reaction=[types.ReactionEmoji(emoticon="❤️")],  # '❤️' '👍'
                )
            )
            await event.reply("Reacted to the previous message!")
        except Exception as e:
            print(f"Error sending reaction: {e}")
            await event.reply("Failed to react to the message.")
    else:
        sender = await event.get_sender()
        print(f"New message from {sender.username}: {event.message.text}")
    replied_msg = await event.get_reply_message()
    if replied_msg:
        await replied_msg.reply("This is a reply to your message!")


# @client.on(events.NewMessage(pattern=r'(?i)hello.+'))
# list_words_to_exclude = ['word1', 'word2', 'word3']
# @client.on(events.NewMessage(incoming=True, pattern=lambda e: e.text not in list_words_to_exclude))


async def main():
    await client.start()

    group = await client.get_entity(groupName)
    while True:
        await client.send_message(group, messages[random.randint(0, len(messages) - 1)])
        time.sleep(random.randint(60, 80))


with client:
    client.loop.run_until_complete(main())