import feedparser
import json
from datetime import datetime
import os

os.makedirs("public", exist_ok=True)

# ==========================
# CONFIG
# ==========================

RSS_FEEDS = {
    "Cybersecurity": "https://news.google.com/rss/search?q=cybersecurity&hl=en-US&gl=US&ceid=US:en",
    "Sports": "https://news.google.com/rss/search?q=sports&hl=en-US&gl=US&ceid=US:en",
    "Fashion": "https://news.google.com/rss/search?q=fashion&hl=en-US&gl=US&ceid=US:en",
    "NationalDevelopment": "https://news.google.com/rss/search?q=national+development&hl=en-US&gl=US&ceid=US:en",
    "Education": "https://news.google.com/rss/search?q=education&hl=en-US&gl=US&ceid=US:en"
}
OUTPUT_HTML = "public/index.html"   # rename blog_content.html → index.html
OUTPUT_JSON = "public/articles.json"


MAX_ARTICLES = 100

# ==========================
# FETCH RSS ARTICLES
# ==========================

def fetch_articles():
    categorized_articles = {}

    for category, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries[:20]:
            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "source": entry.get("source", {}).get("title", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")
            })

        categorized_articles[category] = articles
        print(f"[+] {category}: {len(articles)} articles")

    return categorized_articles

# ==========================
# SAVE JSON (OPTIONAL)
# ==========================

def save_to_json(articles):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[+] Saved {len(articles)} articles to {OUTPUT_JSON}")

# ==========================
# GENERATE STYLED HTML WITH ADS
# ==========================

def generate_html(categorized_articles):
    sections = []

    for category, articles in categorized_articles.items():
        section_id = category.lower()
        sections.append(f'<section id="{section_id}"><h2>{category}</h2>')

        for i, article in enumerate(articles):
            sections.append(f"""
            <article class="card">
                <h3>
                    <a href="{article['link']}" target="_blank">{article['title']}</a>
                </h3>
                <p class="meta">{article['source']} | {article['published']}</p>
                <p>{article['summary']}</p>
            </article>
            """)

            # Insert an ad every 5 articles
            if (i + 1) % 5 == 0:
                sections.append("""
                <div class="ad-banner">
                    <ins class="adsbygoogle"
                         style="display:block"
                         data-ad-client="ca-pub-5052053419736063"
                         data-ad-slot="YYYYYY"
                         data-ad-format="auto"></ins>
                    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
                </div>
                """)

        sections.append("</section>")

    return BASE_HTML.replace("{{CONTENT}}", "\n".join(sections))

# ==========================
# BASE HTML TEMPLATE
# ==========================

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Daily News Hub</title>
<style>
body { font-family: Arial, sans-serif; background: #f4f6f8; margin:0; padding:0; }
header { background: #0f172a; color: white; padding: 20px; }
header h1 { margin:0; }
nav { margin-top: 10px; }
nav a { color: #e5e7eb; margin-right: 15px; text-decoration: none; font-weight: bold; }
nav a:hover { text-decoration: underline; }
.container { padding: 25px; }
section { margin-bottom: 40px; }
section h2 { border-left: 5px solid #2563eb; padding-left: 10px; color: #111827; }
.card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
.card h3 { margin-top: 0; }
.card a { color: #2563eb; text-decoration: none; }
.card a:hover { text-decoration: underline; }
.meta { font-size: 0.9em; color: #6b7280; }
.ad-banner { margin: 20px 0; text-align: center; }
</style>
</head>

<body>

<header>
  <h1>📰 Daily News Hub</h1>
  <nav>
    <a href="#cybersecurity">Cybersecurity</a>
    <a href="#sports">Sports</a>
    <a href="#fashion">Fashion</a>
    <a href="#nationaldevelopment">National Development</a>
    <a href="#education">Education</a>
  </nav>
  <div class="ad-banner">
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-5052053419736063"
         data-ad-slot="YYYYYY"
         data-ad-format="auto"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>
</header>

<div class="container">
{{CONTENT}}
</div>

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5052053419736063"
     crossorigin="anonymous"></script>

</body>
</html>
"""

# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    articles = fetch_articles()
    save_to_json(articles)
    html_content = generate_html(articles)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] Multi-category blog generated successfully: {OUTPUT_HTML}")


