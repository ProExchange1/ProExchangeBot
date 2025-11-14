# bot.py
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from config import TOKEN, MONITORING_CHANNEL   # config.py dan ma'lumotlar

bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- /start buyrug‘i ---
@dp.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(
        "Assalomu alaykum! ProExchange botga xush kelibsiz.\n\n"
        "💱 Pul almashtirish uchun quyidagi ma'lumotlarni yuboring:\n\n"
        "🔢 *Miqdor:* 100000 so'm yoki 10 USDT\n"
        "💳 *Qabul qiluvchi karta/hamyon:* 8600 xxxx xxxx xxxx",
        parse_mode="Markdown"
    )


# --- Foydalanuvchi yuborgan arizani qabul qilish ---
@dp.message(F.text)
async def order_handler(msg: Message):
    user_text = msg.text

    # === Monitoring kanaliga yuboriladigan habar ===
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"ok_{msg.chat.id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"no_{msg.chat.id}")
        ]
    ])

    await bot.send_message(
        MONITORING_CHANNEL,
        f"📩 *Yangi ariza*\n"
        f"👤 User: {msg.from_user.id}\n"
        f"✉️ Xabar: {user_text}",
        reply_markup=kb,
        parse_mode="Markdown"
    )

    await msg.answer("🕓 Ariza qabul qilindi! Admin ko‘rib chiqadi.")


# --- Arizani Tasdiqlash ---
@dp.callback_query(F.data.startswith("ok_"))
async def approve_handler(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    await bot.send_message(user_id, "✅ Arizangiz tasdiqlandi! Tez orada to‘lov amalga oshiriladi.")
    await call.answer("Tasdiqlandi")


# --- Arizani Rad Etish ---
@dp.callback_query(F.data.startswith("no_"))
async def reject_handler(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    await bot.send_message(user_id, "❌ Ariza rad etildi. Iltimos qayta urinib ko‘ring.")
    await call.answer("Rad etildi")


# --- Botni ishga tushirish ---
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())