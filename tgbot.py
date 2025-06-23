from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

YOUR_CHAT_ID = 736034861  # ← сюда вставь свой chat_id

# Категории и продукты
product_categories = {
    "🍳 Главное блюдо": ["Яйца", "Овсянка"],
    "🍞 Углеводики": ["Булочки", "Хлеб", "Булки с корицей свежие", "Булки с корицей маленькие", "Просто печенье"],
    "🍗Мяско": ["Сосиски тонкие куринные", "Сосиски маленькие"],
    "🥦 Овощи и Фрукты": ["Огурец", "Помидор", "Морковка", "Яблоки", "Нектарин", "Виноград", "Груша", "Банан"],
}

# Выбранные продукты
selected_items = []

# Главное меню
def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["🍳 Главное блюдо", "🍞 Углеводики"],
            ["🥦 Овощи и Фрукты", "🍗Мяско"],
            ["🧺 Мой выбор", "🗑 Очистить выбор"],
            ["Завершить выбор"]
        ],
        resize_keyboard=True
    )

# Меню с продуктами
def category_menu(category):
    options = [[item] for item in product_categories.get(category, [])]
    options.append(["↩️ Назад"])
    return ReplyKeyboardMarkup(options, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_items.clear()
    await update.message.reply_text(
        "Привет! Выбирай продукты для завтрака:",
        reply_markup=main_menu()
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Назад в меню категорий
    if text == "↩️ Назад":
        await update.message.reply_text("Выбери категорию:", reply_markup=main_menu())
        return

    # Показать текущий выбор
    if text == "🧺 Мой выбор":
        if selected_items:
            message = "Ты выбрала:\n• " + "\n• ".join(selected_items)
        else:
            message = "Ты пока ничего не выбрала 😊"
        await update.message.reply_text(message, reply_markup=main_menu())
        return

    # Очистить выбор
    if text == "🗑 Очистить выбор":
        selected_items.clear()
        await update.message.reply_text("Выбор очищен 🧼", reply_markup=main_menu())
        return

    # Завершить выбор
    if text == "Завершить выбор":
        if selected_items:
            message = "Ты выбрала следующие продукты:\n• " + "\n• ".join(selected_items)
            await update.message.reply_text(message)
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=f"Она завершила выбор:\n{message}")
            selected_items.clear()
        else:
            await update.message.reply_text("Ты ничего не выбрала 😢")
        await update.message.reply_text("Если хочешь выбрать снова — нажми /start")
        return

    # Выбор категории
    if text in product_categories:
        await update.message.reply_text(
            f"Выбрана категория: {text}\nТеперь выбери продукт:",
            reply_markup=category_menu(text)
        )
        return

    # Выбор продукта
    for category, products in product_categories.items():
        if text in products:
            selected_items.append(text)
            await update.message.reply_text(f"Ты выбрала: {text} ✅", reply_markup=main_menu())
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=f"Она выбрала продукт: {text}")
            return

    await update.message.reply_text("Пожалуйста, выбери вариант из меню.", reply_markup=main_menu())

# Запуск
def main():
    app = ApplicationBuilder().token("8052772143:AAHe0NPp286mTLVhTjTCURmm0wLwGCWb76o").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()

