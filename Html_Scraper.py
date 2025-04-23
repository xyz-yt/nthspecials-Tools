import requests
from bs4 import BeautifulSoup
import os
import time

def title(t="HTML SCRAPER"):
    os.system("title html scraper - {}".format(t))

menu = r"""
██╗  ██╗████████╗███╗   ███╗██╗         ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██║  ██║╚══██╔══╝████╗ ████║██║         ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
███████║   ██║   ██╔████╔██║██║         ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██╔══██║   ██║   ██║╚██╔╝██║██║         ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██║  ██║   ██║   ██║ ╚═╝ ██║███████╗    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝"""

def extract_css(soup, url):
    css_code = ""
    for style in soup.find_all("style"):
        css_code += style.string + "\n"
    for link in soup.find_all("link", rel="stylesheet"):
        css_url = link.get("href")
        if css_url:
            if not css_url.startswith(('http:', 'https:')):
                css_url = requests.compat.urljoin(url, css_url)
            css_response = requests.get(css_url)
            if css_response.status_code == 200:
                css_code += css_response.text + "\n"
    return css_code

def extract_js(soup, url):
    js_code = ""
    for script in soup.find_all("script"):
        if script.get("src"):
            js_url = script.get("src")
            if not js_url.startswith(('http:', 'https:')):
                js_url = requests.compat.urljoin(url, js_url)
            js_response = requests.get(js_url)
            if js_response.status_code == 200:
                js_code += js_response.text + "\n"
        else:
            if script.string:
                js_code += script.string + "\n"
    return js_code

def get_unique_filename(base_name, directory, extension):
    counter = 1
    file_name = f"{base_name}.{extension}"
    while os.path.exists(os.path.join(directory, file_name)):
        file_name = f"{base_name}{counter}.{extension}"
        counter += 1
    return file_name

def main():
    print(menu)
    s = input("Desired Website: ")
    url = s
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    print(soup)

    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Generate unique filenames for all file types
    html_file_name = get_unique_filename("html_source", script_directory, "html")
    css_file_name = get_unique_filename("css_code", script_directory, "css")
    js_file_name = get_unique_filename("javascript", script_directory, "js")

    # Write the HTML source to file
    with open(os.path.join(script_directory, html_file_name), "w", encoding="utf-8") as file:
        file.write(str(soup))
    print(f"HTML source saved to {html_file_name}")

    # Extract and save CSS
    css_code = extract_css(soup, url)
    with open(os.path.join(script_directory, css_file_name), "w", encoding="utf-8") as file:
        file.write(css_code)
    print(f"CSS code saved to {css_file_name}")

    # Extract and save JavaScript
    js_code = extract_js(soup, url)
    with open(os.path.join(script_directory, js_file_name), "w", encoding="utf-8") as file:
        file.write(js_code)
    print(f"JavaScript code saved to {js_file_name}")

    time.sleep(2)
    os.system("cls")
    main()

if __name__ == "__main__":
    main()