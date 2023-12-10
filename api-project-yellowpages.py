import requests
import csv
import os.path

# Connect to Yellow Pages API category page
url = 'https://api.yellowpageskenya.com/categories'
payload = {"searchParameters": {"LINGUA_ID": "2", "country": "CBV"}}

# Retrieve data and change format
response = requests.post(url, json=payload)
data = response.json()
results = data.get('categories')

# Create empty list to append categories
categories = []

# Loop over dictionary (in list) with all categories
for dictionary in results:
    category = dictionary['category']
    categories.append(category)

# Connect to Yellow Pages API business page
# Change API request depending on category name
for i in categories:
    url = 'https://api.yellowpageskenya.com/v1/search'
    payload = {"searchParameters": {"LINGUA_ID": "2", "PESQUISA_F": f'{i}', "LOCALITY_F": "", "country": "CBV"}}

# Retrieve data and change format
    response = requests.post(url, json=payload)
    data = response.json()
    results = data.get('results')

# Write code to see if file exists
    file_exists = os.path.isfile("Paginas_Amarelas_Output.csv")

# Create new csv file to add data to
    with open("Paginas_Amarelas_Output.csv", "a", newline='') as file:
        headers = ["title", "bname", "locality", "region", "baddress", "bemail", "bphone", "bmobile", "burl"]
        writer = csv.DictWriter(file, delimiter=',', fieldnames=headers, extrasaction='ignore', dialect='unix')

# Only add headers when the file is newly created
        if not file_exists:
            writer.writeheader()

# Loop over every result on business page
        for item in results:
            writer.writerow(item)

print('Company information retrieved!')
