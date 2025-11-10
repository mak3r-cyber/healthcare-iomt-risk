import os
import requests
import re

# Fonction pour vérifier si un lien est valide
def is_valid_link(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Chemin vers le fichier contenant les liens à valider
file_path = "docs/compliance/iso27002-iomt-mapping.md"

# Vérifier si le fichier existe
if not os.path.exists(file_path):
    print(f"Le fichier {file_path} n'existe pas.")
    exit(1)

# Lire le fichier et valider les liens
with open(file_path, 'r') as file:
    lines = file.readlines()

# Variables pour suivre les liens valides et invalides
valid_links = []
invalid_links = []

# Expression régulière pour détecter un lien URL valide
url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

# Analyser chaque ligne du fichier à la recherche de liens
for line in lines:
    # Rechercher tous les liens dans la ligne en utilisant l'expression régulière
    links_in_line = re.findall(url_pattern, line)
    
    for link in links_in_line:
        if is_valid_link(link):
            valid_links.append(link)
        else:
            invalid_links.append(link)

# Afficher les résultats
print(f"Nombre de liens valides : {len(valid_links)}")
for link in valid_links:
    print(f"Valid: {link}")

print(f"\nNombre de liens invalides : {len(invalid_links)}")
for link in invalid_links:
    print(f"Invalid: {link}")
