from pyppeteer import launch
import asyncio
import os
import requests
import pandas as pd

ZAP_USERNAME = os.environ["ZAP_USERNAME"]
ZAP_PASS = os.environ["ZAP_PASS"]
ZAP_DOMAIN = os.environ["ZAP_DOMAIN"]


async def main():
    browser = await launch()
    page = await browser.newPage()

    # Login
    await page.goto(ZAP_DOMAIN)
    await page.querySelector("input")
    await page.type("input", ZAP_USERNAME)
    await page.click('[value="Next"]')
    await page.waitForSelector("#passwordInput")
    await page.type("#passwordInput", ZAP_PASS)
    await page.click("#submitButton")
    await page.waitForSelector("#idBtn_Back")
    await page.click("#idBtn_Back")
    await page.waitForSelector("#marsIFrame")

    # Download all records
    skipTokenParams = requests.get(
        "https://zap-api-production.herokuapp.com/projects"
    ).json()["meta"]["skipTokenParams"]
    nextlink = f"{ZAP_DOMAIN}/api/data/v9.1/dcp_projects?{skipTokenParams}"
    counter = 0
    
    while nextlink != "":

        await page.goto(nextlink)
        await page.querySelector("pre")
        result = await page.evaluate("document.body.textContent", force_expr=True)
        result = json.loads(result)

        pd.DataFrame(result["value"]).to_csv(f"dump_{counter}.csv", index=False)

        counter += 1
        nextlink = result.get("@odata.nextLink", "")

    await browser.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
