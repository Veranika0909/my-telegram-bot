import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
# 1. Добавляем недостающий импорт CallbackQueryHandler
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

BOT_TOKEN = "8493906402:AAGBzNabL-eYzHn7_1flXpncunNUrOEym0I" 

# Состояния для ConversationHandler
FIRST, SECOND, THIRD, FINAL, PAYMENT = range(5) # 2. Добавляем новое состояние PAYMENT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['✅ Да', '❌ Нет']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "Привет! Я бот который поможет тебе прийти туда где тебе помогут вернуть радость к жизни. Ты готов?",
        reply_markup=reply_markup
    )
    return FIRST

async def handle_first_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка первого ответа"""
    user_text = update.message.text
    
    if user_text == '✅ Да':
        keyboard = [['✅ Да', '❌ Нет']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "Ну что, надо делать первые шаги! Давай начнём. Хочу показать тебе 3 бесплатных видео о том как вернуть радость к жизни. Ты готов?",
            reply_markup=reply_markup
        )
        return SECOND
        
    elif user_text == '❌ Нет':
        await update.message.reply_text(
            "Хорошо, как скажешь! Если передумаешь - просто напиши /start"
        )
        return ConversationHandler.END
        
    else:
        await update.message.reply_text("Пожалуйста, используй кнопки ниже 👇")
        return FIRST

async def handle_second_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if user_text == '✅ Да':
        # Создаем inline-кнопку для подписки
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/+VUZLC9qW_184ZjUy")],
            [InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Хорошо! Но перед этим тебе нужно подписаться на телеграм канал.\n\n"
            "Подпишись и нажми 'Я подписался'",
            reply_markup=reply_markup
        )
        return THIRD
        
    elif user_text == '❌ Нет':
        await update.message.reply_text(
            "Хорошо, как скажешь! Если передумаешь - просто напиши /start"
        )
        return ConversationHandler.END
        
    else:
        await update.message.reply_text("Пожалуйста, используй кнопки ниже 👇")
        return SECOND

async def handle_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатия на inline-кнопку"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_subscription":
        # Здесь должна быть настоящая проверка подписки (getChatMember)
        # Пока что просто доверяем пользователю
        await query.message.reply_text("Отлично! Ты подписался. Вот ссылка на первый ролик:")
        await query.message.reply_text("https://vkvideo.ru/video-174616704_456239261?list=61718cd62595af03ef")
        
        keyboard = [['✅ Да', '❌ Нет']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await query.message.reply_text(
            "Ты хочешь чтобы я скинул тебе 2 ролик?",
            reply_markup=reply_markup
        )
        # 2. Меняем состояние на FINAL, которое теперь только для видео
        return FINAL

async def handle_final_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка финальных ответов (отправка 2 и 3 видео)"""
    user_text = update.message.text
    
    if user_text == '✅ Да':
        await update.message.reply_text("Отлично! Я рад что тебе нужен этот ролик")
        await update.message.reply_text("Вот второй ролик:")
        await update.message.reply_text("https://vk.com/clip-174616704_456239315?c=1")
        
        await update.message.reply_text("Вот третий ролик:")
        await update.message.reply_text("https://vkvideo.ru/video-174616704_456239347?list=b0e54bd769e04259d4")
        
        keyboard = [['✅ Да', '❌ Нет']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "Вот и 3 видео! Я уверен что они тебе помогли. Хочу предложить тебе купить за 99 рублей 1 занятие которое тебе поможет. Ты согласен?",
            reply_markup=reply_markup
        )
        # 2. Переводим диалог в новое состояние PAYMENT для обработки оплаты
        return PAYMENT
        
    elif user_text == '❌ Нет':
        await update.message.reply_text(
            "Хорошо, как скажешь! Если передумаешь - просто напиши /start"
        )
        return ConversationHandler.END
        
    else:
        await update.message.reply_text("Пожалуйста, используй кнопки ниже 👇")
        return FINAL

# 2. Новая функция для обработки ответа про оплату
async def handle_payment_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа про оплату (новое состояние PAYMENT)"""
    user_text = update.message.text
    
    if user_text == '✅ Да':
        await update.message.reply_text(
            "Отлично! Тогда подробнее о плате ты увидишь в этом боте: @test_bot"
        )
    elif user_text == '❌ Нет':
        await update.message.reply_text(
            "Хорошо, как скажешь! Если передумаешь - просто напиши /start"
        )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена диалога"""
    await update.message.reply_text("Диалог завершен. Напиши /start чтобы начать заново.")
    return ConversationHandler.END

def main():
    """Основная функция"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Настройка ConversationHandler для управления диалогом
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_first_response)],
            SECOND: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_second_response)],
            THIRD: [CallbackQueryHandler(handle_subscription)],  # Исправлено: обработчик inline-кнопок
            FINAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_final_response)],
            # 2. Добавляем новое состояние в машину состояний
            PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment_response)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(conv_handler)
    
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()