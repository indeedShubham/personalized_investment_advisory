import requests
from bs4 import BeautifulSoup
from models import db, MutualFunds # replace 'your_flask_app' with the name of your Flask app module

def scrape_and_store():
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
            morningstar_rating = len(star_rating_cell.find_all('svg', class_='ks_icn ks_icn_star'))
            cell_texts.insert(2, morningstar_rating)
        
        # Check that the row has the expected number of cells
        if len(cell_texts) == 8:
            # Create a dictionary for the mutual fund
            fund = {
                'name': cell_texts[0],
                'category_rank': cell_texts[1],
                'morningstar_rating': cell_texts[2],
                'nav': cell_texts[3],
                'fund_return': cell_texts[4],
                'category_return': cell_texts[5],
                'risk': cell_texts[6],
                'fund_size': cell_texts[7]
            }

            # Check if the fund already exists in the database
            existing_fund = MutualFunds.query.filter_by(name=fund['name']).first()
            if existing_fund is None:
                # The fund does not exist in the database, so create a new record
                new_fund = MutualFunds(name=fund['name'], category_rank=fund['category_rank'], morningstar_rating=fund['morningstar_rating'], nav=fund['nav'], fund_return=fund['fund_return'], category_return=fund['category_return'], risk=fund['risk'], fund_size=fund['fund_size'])
                db.session.add(new_fund)
            else:
                # The fund exists in the database, so update the existing record
                existing_fund.category_rank = fund['category_rank']
                existing_fund.morningstar_rating = fund['morningstar_rating']
                existing_fund.nav = fund['nav']
                existing_fund.fund_return = fund['fund_return']
                existing_fund.category_return = fund['category_return']
                existing_fund.risk = fund['risk']
                existing_fund.fund_size = fund['fund_size']
    # Commit the changes
    db.session.commit()