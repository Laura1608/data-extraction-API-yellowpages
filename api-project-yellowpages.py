import requests
import csv
import os.path

# Connect to Yellow Pages API category page
url_categories = 'https://api.yellowpageskenya.com/categories'
payload_categories = {"searchParameters": {"LINGUA_ID": "2", "country": "CBV"}}

# Retrieve data and change format
response_categories = requests.post(url_categories, json=payload_categories)
data_categories = response_categories.json()
results_categories = data_categories.get('categories')

# Create empty list to append categories
categories = []

# Loop over dictionary (in list) with all categories
for dictionary in results_categories:
    category = dictionary['category']
    categories.append(category)

# Connect to Yellow Pages API business page
# Change API request depending on category name
for i in categories:
    url_business = 'https://api.yellowpageskenya.com/v1/search'
    payload_business = {"searchParameters": {"LINGUA_ID": "2", "PESQUISA_F": f'{i}', "LOCALITY_F": "", "country": "CBV"}}

    # Retrieve data and change format
    response_business = requests.post(url_business, json=payload_business)
    data_business = response_business.json()
    results_business = data_business.get('results')

    # Write code to see if file exists
    file_exists = os.path.isfile("Paginas_Amarelas_Output.csv")

    # Create new csv file to add data to
    with open("Paginas_Amarelas_Output.csv", "a", newline='') as file:
        headers = ["nome_loc_tit_id", "title", "bname", "descricao", "baddress", "locality", "region", "map_lat", "map_long", "bphone", "bmobile", "bemail", "burl", "logo"]

        writer = csv.DictWriter(file, delimiter=',', fieldnames=headers, extrasaction='ignore', dialect='unix')

        # Only add headers when the file is newly created
        if not file_exists:
            writer.writeheader()

        # Loop over every result on business page
        for item in results_business:
            writer.writerow(item)

print('Company information retrieved!')
