import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার তথ্য এখানে দিন
API_TOKEN = '8643041834:AAG7Az9IFM62360ubqqpkJi8ByffZr39W2A'
ADMIN_ID = 8534308595  # আপনার টেলিগ্রাম ইউজার আইডি
BIKASH_NO = "01741374715"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# --- কীবোর্ড বাটন ---
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("💎 সাবস্ক্রিপশন প্ল্যান", callback_data="plans"),
        InlineKeyboardButton("📞 সাপোর্ট", url="https://t.me/your_username")
    )
    return keyboard

def plan_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("৩ দিন - ৩০ টাকা", callback_data="buy_3_50"),
        InlineKeyboardButton("৭ দিন - ৪০ টাকা", callback_data="buy_7_100"),
        InlineKeyboardButton("৩০ দিন - ৬০ টাকা", callback_data="buy_30_300"),
        InlineKeyboardButton("🔙 ফিরে যান", callback_data="back_main")
    )
    return keyboard

# --- হ্যান্ডলারসমূহ ---
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("স্বাগতম! আমাদের প্রিমিয়াম গ্রুপে যুক্ত হতে নিচের বাটনটি চাপুন।", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == 'plans')
async def show_plans(callback_query: types.CallbackQuery):
    await bot.edit_message_text("আমাদের প্ল্যানগুলো নিচে দেওয়া হলো। আপনার পছন্দমতো বেছে নিন:",
                                callback_query.from_user.id,
                                callback_query.message.message_id,
                                reply_markup=plan_menu())

@dp.callback_query_handler(lambda c: c.data.startswith('buy_'))
async def payment_instruction(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    days, price = data[1], data[2]
    
    msg = (f"✅ আপনি {days} দিনের প্ল্যান বেছে নিয়েছেন।\n\n"
           f"💰 মূল্য: {price} টাকা\n"
           f"📱 বিকাশ (Personal): {BIKASH_NO}\n\n"
           "টাকা পাঠানোর পর ট্রানজেকশন আইডি (TrxID) লিখে এখানে মেসেজ দিন।")
    
    await bot.send_message(callback_query.from_user.id, msg)

# ইউজার TrxID পাঠালে অ্যাডমিনের কাছে যাবে
@dp.message_handler()
async def handle_payment(message: types.Message):
    # ইউজার যদি অ্যাডমিন না হয়, তবে মেসেজটি পেমেন্ট রিকোয়েস্ট হিসেবে ধরা হবে
    if message.from_user.id != ADMIN_ID:
        approve_kb = InlineKeyboardMarkup()
        approve_kb.add(InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.from_user.id}"))
        
        await bot.send_message(ADMIN_ID, f"📩 নতুন পেমেন্ট রিকোয়েস্ট!\nইউজার: {message.from_user.full_name}\nমেসেজ: {message.text}", reply_markup=approve_kb)
        await message.answer("ধন্যবাদ! আপনার পেমেন্ট রিকোয়েস্ট অ্যাডমিনের কাছে পাঠানো হয়েছে। যাচাই করে আপনাকে গ্রুপ লিংক দেওয়া হবে।")

@dp.callback_query_handler(lambda c: c.data.startswith('approve_'))
async def approve_user(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[1]
    group_link = "https://t.me/+eiFGZcO3yRk5MjVl" # আপনার গ্রুপের ইনভাইট লিংক
    
    await bot.send_message(user_id, f"🎉 আপনার পেমেন্ট অ্যাপ্রুভ হয়েছে!\nনিচের লিংকে ক্লিক করে গ্রুপে জয়েন করুন:\n{group_link}")
    await bot.answer_callback_query(callback_query.id, "ইউজারকে লিংক পাঠানো হয়েছে!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
