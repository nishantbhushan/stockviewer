import requests
from bs4 import BeautifulSoup
import string
import re
import pickle

letters=string.ascii_lowercase
letters_list=list(letters)
letters_list.append('number')
print(letters_list)

columns_list = {
    'company':str,
    'ticker':str,
    'url':str
}
stock_list = []
for letter in letters_list:
    # if(letter =='c'):
        # break
    formed_url = 'https://www.dogsofthedow.com/stock/stock-symbols-list-'+letter+'.htm'
    # Send a GET request to the URL
    response = requests.get(formed_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table element
    table = soup.find('table')
    # print(type(table))

    company=''
    ticker = ''
    url = ''
    # Find all the rows of the table
    rows = table.find_all('tr')
    r=0
    # Iterate over the rows
    for row in rows:
        if r!=0:
            # Find all the cells in the row
            cells = list(row.find_all('td'))
            c=0
            for cell in cells:
                
                cell = str(cell)
                cell = re.sub(r'<[^>]*>','',cell)
                if c==0:
                    company = None if cell=='' else cell
                elif c==1:
                    ticker = None if cell=='' else cell
                elif c==2:
                    url = None if cell=='' else cell
                    
                # print(cell)
                c=c+1
                # print(f"cell {c}")
            
            new_row = {
                'company':company,
                'ticker':ticker,
                'url':url
            }
            print(r)
            print(f"{new_row}") 
            print(type(new_row))
            stock_list.append(new_row)
        r=r+1
        # print(f"row {r}")
            
        # df = pandas.concat([df,newRowDf], ignore_index = True)
        # if r==10:
        #     break
        # Print the contents of the cells
        # print([cell.text for cell in cells])
# df=df[company.notnull()]
with open('stock_list.pkl','wb') as f:
    pickle.dump(stock_list,f)