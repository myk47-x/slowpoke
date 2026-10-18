import re
from bs4 import BeautifulSoup

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "img"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    text = text.replace("\xa0", " ")

    text = re.sub(r"\[([^\]]+)\]\(https?://[^)]+\)", r"\1", text)

    return text

