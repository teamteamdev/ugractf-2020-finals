import asyncio
import json
import logging

import cryptography.fernet as fernet
import pyppeteer

from adchecklib import Down


mainLogger = logging.getLogger(__name__)


SECRET_KEY = b"gno8p-srs5tko8rZRN3a7EtPhd0WObZqJlmeO-eq-kU="


async def check_advertisement(page, logger):
    integrity = await page.evaluate('''() => {
        return window.adhellIntegrity;
    }''')

    if not isinstance(integrity, str):
        raise Down("Please disable AdBlocker (no integrity)")

    cipher = fernet.Fernet(SECRET_KEY)
    try:
        data = cipher.decrypt(integrity.encode(), 60).decode()
        banner = json.loads(data)
    except (fernet.InvalidToken, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Down(f"Please disable AdBlocker ({type(exc)})")

    logger.info(data)

    tag_name = {
        'text': 'p',
        'image': 'img',
        'video': 'video'
    }[banner['format']]

    logger.info("Banner contents: %s", await page.evaluate('''() => {
        return document.querySelector('#adhellRealBanner').outerHTML;
    }'''))

    has_block = await page.evaluate(f'''() => {{
        const bl = document.querySelector("#adhellRealBanner #{banner['block']}");
        return bl && bl.tagName.toUpperCase() == '{tag_name.upper()}'
    }}''')

    if not has_block:
        raise Down("Please disable AdBlocker (no content block)")

    if banner['partner']:
        if banner['format'] == 'text':
            has_content = await page.evaluate(f'''() => {{
                const bl = document.querySelector("#adhellRealBanner #{banner['block']}");
                return bl && bl.innerHTML == "{banner['content']}";
            }}''')
        else:
            has_content = await page.evaluate(f'''() => {{
                const bl = document.querySelector("#adhellRealBanner #{banner['block']}");
                return bl && bl.src == "{banner['content']}";
            }}''')

        if not has_content:
            raise Down("Please disable AdBlocker (corrupted content)")


async def main():
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto('http://127.0.0.1:43250/sample.html')
    try:
        await check_advertisement(page, mainLogger)
    finally:
        await browser.close()


asyncio.get_event_loop().run_until_complete(main())
