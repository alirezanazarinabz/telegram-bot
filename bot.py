import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# جایگزین کردن توکن ربات
TELEGRAM_BOT_TOKEN = "6747355749:AAFhQEXjVqe9FVABNa1w_3FvKBnMF3CQs2U"

def get_prices():
    url = "https://www.g-adwords.com/AdwordsPriceList/لیست-قیمت-شارژ-حساب-گوگل-ادوردز/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "❌ خطا در دریافت اطلاعات از سایت"

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if not table:
        return "❌ جدول قیمت‌ها پیدا نشد."

    prices = []
    for row in table.find_all("tr")[1:]:  
        cols = row.find_all("td")
        if len(cols) >= 2:
            plan = cols[0].text.strip()
            price = cols[1].text.strip().replace(",", "").replace("تومان", "")
            try:
                new_price = int(price) * 1.2
                prices.append(f"{plan}: {int(new_price):,} تومان")
            except ValueError:
                continue

    return "\n".join(prices) if prices else "❌ هیچ قیمت معتبری یافت نشد."

def send_prices(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    prices = get_prices()
    context.bot.send_message(chat_id=chat_id, text=f"📌 **لیست قیمت‌ها با ۲۰٪ افزایش:**\n\n{prices}", parse_mode="Markdown")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("prices", send_prices))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
