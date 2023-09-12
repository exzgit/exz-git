import discord
from discord.ext import commands, tasks
import random
import sqlite3
import openai

# Inisialisasi bot
bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())


# API Tokenz openai
openai.api_key = "YOUR_OPENAI_API_KEY"

# Buat koneksi database SQLite
conn = sqlite3.connect('user_db.sqlite')
cursor = conn.cursor()

# Buat tabel untuk menyimpan pengguna yang terdaftar jika belum ada
cursor.execute('''
    CREATE TABLE IF NOT EXISTS registered_users (
        user_id TEXT PRIMARY KEY,
        username TEXT,
        level INTEGER
    )
''')
conn.commit()

# Fungsi untuk mendaftarkan pengguna
def register_user(user_id, username):
    cursor.execute('INSERT OR REPLACE INTO registered_users (user_id, username, level) VALUES (?, ?, ?)', (user_id, username, 1))
    conn.commit()

# Fungsi untuk memeriksa apakah seorang pengguna terdaftar
def is_registered(user_id):
    cursor.execute('SELECT * FROM registered_users WHERE user_id = ?', (user_id,))
    return cursor.fetchone() is not None

# Fungsi untuk mendapatkan level pengguna
def get_user_level(user_id):
    cursor.execute('SELECT level FROM registered_users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

# Fungsi untuk meningkatkan level pengguna
def increase_user_level(user_id):
    current_level = get_user_level(user_id)
    if current_level is not None:
        cursor.execute('UPDATE registered_users SET level = ? WHERE user_id = ?', (current_level + 1, user_id))
        conn.commit()

# Fungsi untuk menutup koneksi database
def close_database():
    cursor.close()
    conn.close()

# Inisialisasi variabel global
current_question = None
current_answer = None
user_answered = False

# Fungsi untuk menghasilkan pertanyaan matematika acak
def generate_random_math_question():
    operators = ['+', '-', '*', '/']
    operator = random.choice(operators)
    if operator == '+':
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        answer = num1 + num2
    elif operator == '-':
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        answer = num1 - num2
    elif operator == '*':
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        answer = num1 * num2
    else:
        num2 = random.randint(1, 20)
        answer = random.randint(1, 5)
        num1 = num2 * answer
    question = f"{num1} {operator} {num2}?"
    return question, str(answer)

# Penanganan peristiwa saat bot siap
@bot.event
async def on_ready():
    print(f'Bot siap dengan nama {bot.user.name}')

# Penanganan perintah untuk /regbot
@bot.command()
async def regbot(ctx):
    if is_registered(str(ctx.author.id)):
        await ctx.send("Anda sudah terdaftar.")
    else:
        register_user(str(ctx.author.id), ctx.author.name)
        await ctx.send("Anda telah terdaftar.")

# Penanganan perintah untuk /mtk
@bot.command()
async def mtk(ctx):
    global current_question, current_answer, user_answered
    if is_registered(str(ctx.author.id)):
        current_question, current_answer = generate_random_math_question()
        user_answered = False
        await ctx.send(f"Anda memiliki 1 menit untuk menjawab: ```{current_question}```")
    else:
        await ctx.send("Anda belum terdaftar. Gunakan ```/regbot``` untuk mendaftar.")

# Penanganan perintah untuk menjawab pertanyaan
@bot.command()
async def answer(ctx, user_answer: str):
    global user_answered
    if user_answered:
        await ctx.send("Anda telah menjawab pertanyaan ini sebelumnya.")
        return

    if user_answer is None or user_answer == "":
        await ctx.send("Silakan berikan jawaban.")
        return

    if user_answer == current_answer:
        user_answered = True
        increase_user_level(str(ctx.author.id))
        current_level = get_user_level(str(ctx.author.id))
        if current_level % 3 == 0:
            await ctx.send(f"Selamat! Anda sekarang berada di level ```{current_level}```. Anda telah menjawab 15 pertanyaan dengan benar secara beruntun!")
            await ctx.send("Jawaban Anda benar. Gunakan ```/exit``` untuk keluar atau ```/next``` untuk melanjutkan.")
        else:
            await ctx.send("Jawaban Anda benar. Gunakan ```/exit``` untuk keluar atau ```/next``` untuk melanjutkan.")
    else:
        await ctx.send("Jawaban Anda salah.")

# Penanganan perintah untuk /next
@bot.command()
async def next(ctx):
    global current_question, current_answer, user_answered
    if user_answered:
        current_question, current_answer = generate_random_math_question()
        user_answered = False
        await ctx.send(f"Anda memiliki 1 menit untuk menjawab: ```{current_question}```")
    else:
        await ctx.send("Anda harus menjawab pertanyaan saat ini terlebih dahulu.")

# Penanganan perintah untuk /exit
@bot.command()
async def exit(ctx):
    global user_answered
    if user_answered:
        await ctx.send("Terima kasih telah bermain!")
        user_answered = False
    else:
        await ctx.send("Anda harus menjawab pertanyaan saat ini terlebih dahulu.")

@bot.command()
async def checklv(ctx):
    user_id = str(ctx.author.id)
    user_level = get_user_level(user_id)
    if user_level is not None:
        await ctx.send(f"Level Anda saat ini adalah ```{user_level}```.")
    else:
        await ctx.send("Anda belum terdaftar. Gunakan ```/regbot``` untuk mendaftar.")

@tasks.loop(minutes=1)
async def check_question():
    global user_answered

    # Periksa apakah ada pengguna yang terdaftar
    if not is_registered(str(ctx.author.id)):
        return

    user_id = None
    for user in registered_users.keys():
        user_id = user

    if user_id:
        if current_answer is not None:
            user = await bot.fetch_user(int(user_id))
            await user.send("Waktu habis! Jawabannya adalah: " + current_answer)
            user_answered = True
            increase_user_level(str(user.id))  # Tingkatkan level pengguna saat menjawab dengan benar
            new_level = get_user_level(str(user.id))
            await user.send(f"Selamat! Anda sekarang berada di level ```{new_level}```.")
        else:
            user_answered = True

# perintah untuk ke openai
@bot.command()
async def gpt(ctx,*,msg):
    response = openai.Completion.create(
        model = "text-davinci-003",
        max_tokenz = 2000,
        prompt = msg,
        temperature = 0.6
    )

    await ctx.send(response.choice[0].text)
    return response.choice[0].text

# Token bot Discord Anda
DISCORD_BOT_TOKEN = "TOKEN_BOT_DISCORD"
bot.run(DISCORD_BOT_TOKEN)
