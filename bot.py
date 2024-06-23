import discord
import re
import os
import time

client = discord.Client(intents=discord.Intents.all())

############################################################

# settings

file_path = "./www"
website_url = "https://totallynotfake.news"
discord_token = "TOKEN"

############################################################

def convert_text(text):
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'(?<!\n)\n(?!\n)(.+?)(?=\n\n|\Z)', r'<p>\1</p>', text, flags=re.DOTALL)
    text = text.replace('\n', '<br/>')
    
    return text

def generate_news_path():
    return f"news/{str(int(time.time()))}"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(f'<@{str(client.user.id)}>'):
        news_path = generate_news_path()
        command = message.content.split(' ')[1].split('\n')[0]
        print(command)
        if command == "upload":
            first_title = re.search(r'^# (.+)$', message.content, flags=re.MULTILINE)
            first_title = first_title.group(1) if first_title else "新聞"
            meta_title = first_title
            content = convert_text(re.sub(f"<@{str(client.user.id)}> upload\n","",message.content))

            meta_desc = re.sub(meta_title, "", content)[:50] + "..."
            
            html_1 = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="title" content="{meta_title}" />
                    <meta name="description" content="{meta_desc}" />
                    <title>絕對不是假新聞網</title>
                '''

            if not os.path.exists(file_path):
                os.makedirs(file_path)
            os.makedirs(f"{file_path}/{news_path}")
            with open(f"{file_path}/{news_path}/index.html", "w", encoding="utf-8") as f:
                f.write(html_1 + html_2 + content + html_3)
            await message.reply(f"網站已經上傳，請前往 {website_url}/{news_path} 查看")



html_2 = '''
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
        }
        header {
            background: #35424a;
            color: white;
            padding-top: 30px;
            min-height: 70px;
            border-bottom: #e8491d 3px solid;
        }
        header a {
            color: #ffffff;
            text-decoration: none;
            text-transform: uppercase;
            font-size: 16px;
        }
        header li {
            float: left;
            display: inline;
            padding: 0 20px 0 20px;
        }
        header #branding {
            float: left;
        }
        header #branding h1 {
            margin: 0;
        }
        header nav {
            float: right;
            margin-top: 10px;
        }
        header .highlight, header .current a {
            color: #e8491d;
            font-weight: bold;
        }
        #showcase {
            min-height: 400px;
            text-align: center;
            color: #ffffff;
        }
        #showcase h1 {
            margin-top: 100px;
            font-size: 55px;
            margin-bottom: 10px;
            color: #000000;
        }
        #showcase p {
            font-size: 20px;
            color: #000000;
        }
        #main h1 {
            font-size: 45px;
        }
        #main {
            margin-bottom: 20px;
            font-size: 20px;
        }
        aside#sidebar {
            float: right;
            width: 30%;
            margin-top: 10px;
        }
        article#main-col {
            float: left;
            width: 65%;
        }
        footer {
            padding: 20px;
            margin-top: 20px;
            color: #ffffff;
            background-color: #e8491d;
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div id="branding">
                <h1><span class="highlight">不是</span> 假新聞網</h1>
            </div>
            <nav>
                <ul>
                    <li class="current"><a href="#">熱門</a></li>
                    <li><a href="#">不熱門</a></li>
                    <li><a href="#">很熱門</a></li>
                    <li><a href="https://github.com/nelsonGX/totallynotfake.news-bot">GitHub</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <section id="showcase">
        <div class="container">
            <h1>Breaking News</h1>
            <p>這裡正在報導史詩級的新聞。</p>
        </div>
    </section>

    <section id="main">
        <div class="container">
            <article id="main-col">
'''

html_3 = '''
            </article>
            <aside id="sidebar">
                <h3>今日頭條</h3>
                <ul>
                    <li><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">驚爆! 路邊看見「一男子」，專家這樣說...</a></li>
                    <li><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">獨家 / 天上太陽紅呀紅彤彤耶</a></li>
                    <li><a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">你媽死了? 你沒事了!</a></li>
                </ul>
            </aside>
        </div>
    </section>

    <footer>
        <p>不是假新聞網，沒有版權 &copy; 2024</p>
    </footer>
</body>
</html>
'''


client.run(discord_token)