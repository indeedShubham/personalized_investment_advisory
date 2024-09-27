import requests
from bs4 import BeautifulSoup

#req = requests.get('https://www.amfiindia.com/')
req = requests.get('https://www.moneycontrol.com/mutualfundindia/')

soup = BeautifulSoup(req._content,"html.parser")

#print(soup.prettify())

# Scraping data from the table
 
table = soup.find("table", class_="mctable1")

# Extract table headers
headers = [header.text.strip() for header in table.find_all("th")]

# Extract table rows
rows = []
for row in table.find_all("tr"):
    cells = [cell.text.strip() for cell in row.find_all("td")]
    if cells:
        rows.append(cells)

# Print headers
print("\t".join(headers))

# Print rows
for row in rows:
    print("\t".join(row))
