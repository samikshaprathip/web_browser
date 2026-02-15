from network import request
from html_parser import extract_text

html = request("https://example.com")
text = extract_text(html)

print(text)
