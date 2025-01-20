#Input - Url of file // www.aero.iitb.ac.in
#Outout - Directory created  // www.aero.iitb.ac.in 

import asyncio
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import hashlib

visited_urls = set() #set of all visited urls to avoid visiting same urls repeatedly
all_urls = set() #set of all urls that have not yet been visted 
visit_count = 0  #counter to keep track how many urls have been visted

def create_directory_structure(url):
    parsed_url = urlparse(url)
    file_name = unquote(parsed_url.path.lstrip("/")) #remove '/' to save to subdirectory 
    if len(file_name) > 100:  # Arbitrary length limit to prevent long file names
        file_name = hashlib.md5(file_name.encode()).hexdigest() + ".html" #shortened file name 

    # If the URL points to a directory or is empty, set it as index.html
    if not parsed_url.path or parsed_url.path.endswith("/"):
        path = Path(parsed_url.netloc) / file_name / "index.html"
    else:
        path = Path(parsed_url.netloc) / file_name

    os.makedirs(path.parent, exist_ok=True)
    return path

def rewrite_urls(html_content, base_url):
    parsed_url = urlparse(base_url)
    base_path = f"/{parsed_url.netloc}"
    return html_content.replace(f'src="/', f'src="{base_path}/').replace(f'href="/', f'href="{base_path}/')

async def get_all_urls_and_resources(page, base_url):
    urls = []
    resources = []

    # Get all links
    links = await page.query_selector_all("a")
    for link in links:
        url = await link.get_attribute("href")
        if url:
            # Resolve relative URLs
            full_url = urljoin(base_url, url)
            # Check if URL is within the same domain
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                urls.append(full_url)

    # Get all resources (images, CSS, JS)
    resources_elements = await page.query_selector_all("img, link[rel='stylesheet'], script[src]")
    for resource in resources_elements:
        url = await resource.get_attribute("src") or await resource.get_attribute("href")
        if url:
            full_url = urljoin(base_url, url)
            resources.append(full_url)

    return urls, resources

async def save_content(url, content):
    path = create_directory_structure(url)
    with open(path, "w", encoding='utf-8',errors='ignore') as file:
        file.write(content)
    print(f"Saved: {path}")

async def download_resource(context, url):
    path = create_directory_structure(url)
    if not path.exists():
        page = await context.new_page()
        try:
            response = await page.goto(url)
            content = await response.body()
            with open(path, "wb") as file:
                file.write(content)
            print(f"Downloaded resource: {path}")
        except Exception as e:
            print(f"Failed to download resource: {url} - {e}")
        await page.close()

async def scrape_page(context, url):
    global visit_count
    if url in visited_urls:
        return
    visited_urls.add(url)
    visit_count += 1
    print(f"Visiting: {url} - Total visited: {visit_count}")

    page = await context.new_page()
    try:
        await page.goto(url)
        # Increase the timeout value to 60 seconds
        await page.wait_for_load_state('networkidle', timeout=60000)
        try:
            await page.wait_for_selector('body', timeout=60000)  # Wait for the body to be available
        except PlaywrightTimeoutError as e:
            print(f"Failed to load body for URL: {url} - {e}")
            await page.close()
            return

        content = await page.content()
        rewritten_content = rewrite_urls(content, url)
        await save_content(url, rewritten_content)

        urls, resources = await get_all_urls_and_resources(page, url)
    except PlaywrightTimeoutError as e:
        print(f"Timeout while loading URL: {url} - {e}")
        await page.close()
        return
    finally:
        await page.close()

    for resource_url in resources:
        await download_resource(context, resource_url)

    for new_url in urls:
        if new_url not in visited_urls:
            all_urls.add(new_url)
            print(f"Found URL: {new_url}")
            await scrape_page(context, new_url)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        start_url = "https://www.aero.iitb.ac.in/"

        await scrape_page(context, start_url)

        await browser.close()

        print(f"\nTotal URLs visited: {visit_count}")
        print("\nAll extracted URLs:")
        for url in all_urls:
            print(url)

# Run the main function
asyncio.run(main())

