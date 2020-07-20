from src.classes import AnkiBot

bot = AnkiBot("text", "frases.txt", "db_cards", "cards")

bot.start("login.txt")
