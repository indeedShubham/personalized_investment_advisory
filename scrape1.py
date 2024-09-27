import requests
from bs4 import BeautifulSoup

url = 'https://www.businesstoday.in/mutual-funds/best-mf'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all rows in the table
rows = soup.find_all('div', class_='wdg_tbl_tr')

# Loop over each row
for row in rows:
    # Find all cells in the row
    cells = row.find_all('div', class_='wdg_tbl_td')

    # Extract text from each cell
    cell_texts = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True)!= '']

    # Find the cell with the star rating
    star_rating_cell = row.find('div', class_='wdg_tbl_td wdg_str_td')

    # Check if the cell was found and if it contains a star rating
    if star_rating_cell is not None and '--' not in star_rating_cell.get_text():
        # Count the number of 'ks_icn ks_icn_star' SVG elements
        morningstar_rating = len(star_rating_cell.find_all('svg', class_='ks_icn ks_icn_star'))
        # Insert the star rating at the correct position in the cell texts
        cell_texts.insert(2, morningstar_rating)
    
    print(cell_texts)