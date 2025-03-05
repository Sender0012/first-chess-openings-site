import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from search_for_info import search
# URL strony z otwarciami szachowymi
url = "https://www.thechesswebsite.com/chess-openings/"

# Pobranie strony
response = requests.get(url)
if response.status_code != 200:
    print("Nie udało się pobrać strony")
    exit()

# Parsowanie HTML
soup = BeautifulSoup(response.text, "html.parser")

first_container = soup.find("div", class_="elementor-element elementor-element-7f0d9d87 elementor-widget elementor-widget-shortcode")

real_container = first_container.find("div", id="cb-container")

links = real_container.select("a")

# Znalezienie tabeli z otwarciami
openings = []

for link in links:
    href = link.get("href")  # Extracts the URL
    img_tag = link.find("img")  # Finds an image inside the <a>
    h5_tag = link.find("h5")  # Finds an <h5> title inside the <a>
    span_tag = link.find("span")  # Finds an optional <span> (e.g., "Members only")

    # Extract text and image source if available
    name = h5_tag.text.strip() if h5_tag else "Unknown"
    img_src = img_tag["src"] if img_tag else None  # Extract image src if available
    members_only =  True if span_tag else False  # Check if Members Only

    # Store in dictionary
    openings.append({
        "name": name,
        "link": href,
        "image": img_src,
        "members_only": members_only
    })

# Print extracted data
# for opening in openings:
#     print(opening)

# Create and write to a Markdown file
# Create the main Markdown file
with open("chess_openings.md", "w") as main_md:
    main_md.write("# List of Chess Openings\n\n")
    main_md.write("---\n\n")

    for opening in openings:
        # Create a unique file name for each opening
        opening_filename = f"openings/{opening['name'].replace(' ', '_').lower()}.md"

        # Create the individual Markdown file for each opening
        with open(opening_filename, "w") as opening_md:
            opening_md.write(f"---\n")
            opening_md.write(f"layout: page\n")
            opening_md.write(f"title: {opening['name']}\n")
            opening_md.write(f"permalink: /list_of_chess_openings/{opening['name'].replace(' ', '_')}/\n")  # Ensure spaces are replaced by underscores
            opening_md.write(f"---\n\n")
            
            if opening['image']:
                opening_md.write(f"![{opening['name']}]({opening['image']})\n\n")
            # opening_md.write(f"[Go to chess opening]({opening['link']})\n\n")
            # op  = opening['name'].replace("Gambit", "").strip()
            # opening_infos = DDGS().text(op, max_results=1)
            opening_infos = search(opening['name'])
            # opening_infos = search(f"{opening['name']}")
            # print(opening_infos)
            if opening_infos[0]['title'] != 'False' :
                for opening_info in opening_infos :
                    opening_md.write("---\n\n")
                    opening_md.write(f"## {opening_info['title']}\n\n")
                    opening_md.write(f"{opening_info['body']}\n\n")
                    opening_md.write(f"[More information in this page]({opening_info['href']})\n\n")




        # Link to the new file in the main markdown
        main_md.write(f"## [{opening['name']}](/list_of_chess_openings/{opening['name'].replace(' ', '_')})\n\n")
        
        if opening['members_only']:
            main_md.write(f"**🔒 Members only**\n\n")

        if opening['image']:
            main_md.write(f"![{opening['name']}]({opening['image']})\n\n")

        main_md.write("---\n\n")


print("Markdown file 'chess_openings.md' created successfully!")
