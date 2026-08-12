from aiogram import Bot
import httpx

CHANNEL_ID = ""

async def publish_news_item(bot: Bot, api_client: httpx.AsyncClient, item: dict):

    text = (
        f"<b>📰 {item['title']}</b>\n\n"
        f"{item['description'][:300]}...\n\n"
        f"🔗 <a href='{item['link']}'>Читати повністю на {item['source_name']}</a>"
    )

    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            disable_web_page_preview=False
        )
        await api_client.post(
            "/processed_news",
            params={
                "source_id": item["source_id"],
                "news_hash": item["hash"],
                "title": item["title"],
                "link": item['link']
            }
        )
    except Exception as e:
        print(f"❌ Помилка публікації новини '{item['title']}': {e}")