import tkinter as tk
from tkinter import scrolledtext
from scrapy.crawler import CrawlerProcess
import scrapy
import requests
from fuzzywuzzy import fuzz
from selenium import webdriver

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = []
    def parse(self, response):
   
        text_content = response.xpath('//body//text()[not(parent::script)]').getall()
    # Extracting image URLs
        image_urls = response.xpath('//img/@src').getall()
        item = {
        'url': response.url,
        'text_content': text_content,
        'image_urls': image_urls
        }
  
        crawled_data.append(item)
        yield item

crawled_data = []

def start_crawler(url):
    MySpider.start_urls.append(url)
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_ENABLED': False
    })
    process.crawl(MySpider)
    process.start()

def start_crawling():
    url = url_entry.get()
    if not url:
        output_area.insert(tk.END, "Please enter a URL.\n")
        return
    start_crawler(url)
    output_area.delete(1.0, tk.END)
    output_area.insert(tk.END, "Crawling completed successfully.\n")
    fetch_network_info(url)

def fetch_network_info(url):
    output_area.insert(tk.END, f"\nFetching network info for {url}...\n")
    try:
        domain_info = requests.get(url).url
        output_area.insert(tk.END, f"Domain: {domain_info}\n")
        ip_address = requests.get(url).headers.get('X-Forwarded-For')
        if ip_address:
            output_area.insert(tk.END, f"IP Address: {ip_address}\n")
        else:
            output_area.insert(tk.END, "IP Address: Not available\n")
        output_area.insert(tk.END, f"Response Time: {requests.get(url).elapsed.total_seconds()} seconds\n")
    except Exception as e:
        output_area.insert(tk.END, f"Error fetching network info: {str(e)}\n")

from selenium import webdriver

# def capture_screenshot(url, keyword):
#     # Configure Selenium WebDriver
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without opening GUI)
#     chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
#     chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resources problem in Docker

#     # Create Chrome WebDriver instance
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get(url)

#     # Find elements containing the keyword
#     elements = driver.find_elements_by_xpath(f"//*[contains(text(), '{keyword}')]")
    
#     # Capture screenshots of each element containing the keyword
#     screenshots = []
#     for index, element in enumerate(elements):
#         screenshot_path = f"screenshot_{index}.png"
#         element.screenshot(screenshot_path)
#         screenshots.append(screenshot_path)
    
#     # Close the WebDriver
#     driver.quit()
    
#     return screenshots




def search_data():
    keyword = keyword_entry.get().lower()
    if not keyword:
        output_area.insert(tk.END, "Please enter a keyword.\n")
        return

    found_items = []
    for item in crawled_data:
        found = False
        for text in item['text_content']:
            if keyword in text.lower():
                found = True
                break
        if found:
            found_items.append(item)

    output_area.delete(1.0, tk.END)
    if found_items:
        output_area.insert(tk.END, f"Found {len(found_items)} item(s) containing the keyword '{keyword}':\n\n")
        for item in found_items:
            output_area.insert(tk.END, f"URL: {item['url']}\n")
            output_area.insert(tk.END, "Text Content:\n")
            for text in item['text_content']:
                if keyword in text.lower():
                    output_area.insert(tk.END, f"- {text.strip()}\n")
            output_area.insert(tk.END, "Image URLs:\n")
            for image_url in item['image_urls']:
                output_area.insert(tk.END, f"- {image_url}\n")
            output_area.insert(tk.END, "\n")
    else:
        output_area.insert(tk.END, f"No items found containing the keyword '{keyword}'.\n")






def display_crawled_data():
    output_area.insert(tk.END, "\nCrawled Data:\n")
    for item in crawled_data:
        output_area.insert(tk.END, f"URL: {item['url']}\n")
        output_area.insert(tk.END, "Text Content:\n")
        for text in item['text_content']:
            output_area.insert(tk.END, f"  - {text.strip()}\n")
        output_area.insert(tk.END, "Image URLs:\n")
        for image_url in item['image_urls']:
            output_area.insert(tk.END, f"  - {image_url}\n")
        output_area.insert(tk.END, "\n")


# Tkinter GUI
root = tk.Tk()
root.title("Web Crawler")

# GUI components
tk.Label(root, text="Web Crawler", font=("Helvetica", 16)).pack(pady=10)

# URL Entry
url_frame = tk.Frame(root)
url_frame.pack(pady=5)
url_label = tk.Label(url_frame, text="Enter starting URL:")
url_label.pack(side=tk.LEFT)
url_entry = tk.Entry(url_frame, width=40)
url_entry.pack(side=tk.LEFT)

# Expected URL Format
expected_url_label = tk.Label(root, text="Expected URL format: http(s)://www.example.com")
expected_url_label.pack()

start_button = tk.Button(root, text="Start Crawling", command=start_crawling)
start_button.pack(pady=5)

# Keyword Entry
keyword_frame = tk.Frame(root)
keyword_frame.pack(pady=5)
keyword_label = tk.Label(keyword_frame, text="Enter keyword:")
keyword_label.pack(side=tk.LEFT)
keyword_entry = tk.Entry(keyword_frame, width=20)
keyword_entry.pack(side=tk.LEFT)

# Search Button
search_button = tk.Button(root, text="Search", command=search_data)
search_button.pack(pady=5)


# Display Crawled Data Button
display_button = tk.Button(root, text="Display Crawled Data", command=display_crawled_data)
display_button.pack(pady=5)

# Expanded Text Widget
output_area = scrolledtext.ScrolledText(root, width=150, height=50)
output_area.pack(pady=10)

# Set dark theme colors
bg_color = '#2b2b2b'  # Background color
fg_color = '#dcdcdc'  # Foreground (text) color

# Configure root window
root.configure(bg=bg_color)

# Configure input label
url_label.config(bg=bg_color, fg=fg_color)
keyword_label.config(bg=bg_color, fg=fg_color)

# Configure input entry
url_entry.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
keyword_entry.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

# Configure search button
search_button.config(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)

# Configure output text area
output_area.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

# Define font for labels and buttons
font_style = ('Helvetica', 10, 'bold')

# Configure input label
url_label.config(font=font_style)
keyword_label.config(font=font_style)

# Configure input entry
url_entry.config(font=font_style)
keyword_entry.config(font=font_style)

# Configure search button
search_button.config(font=font_style)

# Configure output text area
output_area.config(font=('Helvetica', 10))



root.mainloop()
