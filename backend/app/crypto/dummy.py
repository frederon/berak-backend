from bs4 import BeautifulSoup

html_text = "<body>\"&a4NB\\e/J#{\\).oIn\u000ezKQ\u0002bt\u0006\"L\n\"S=qj]\bR\u001bN\u000f-.A0lT;kTgC=<t0\u00071{b\u0003r\u0019yB</body>"

start_index = html_text.find("<body>") + len("<body>")
end_index = html_text.find("</body>")

body_text = html_text[start_index:end_index]

print(html_text)

print("=" * 20)
print("---- BODY TEXT ----")
print(body_text)
print("=" * 20)   