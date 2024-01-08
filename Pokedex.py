import requests
import sqlite3

# Function to get Pokémon details
def get_pokemon_details(pokemon_name):
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        pokemon_details = response.json()
        return pokemon_details
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to extract Pokémon information
def extract_pokemon_info(pokemon_details):
    if not pokemon_details:
        return None
    
    pokemon_info = {
        'Name': pokemon_details['name'],
        'Height': pokemon_details['height'],
        'Weight': pokemon_details['weight'],
        'Types': [type_data['type']['name'] for type_data in pokemon_details['types']],
    }
    
    return pokemon_info

# Create a SQLite database
conn = sqlite3.connect('pokemon_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table for Pokémon data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        height REAL,
        weight REAL,
        types TEXT
    )
''')

# Commit changes to the database
conn.commit()

# Initialize pokemon_info outside the conditional block
pokemon_info = None

def insert_pokemon_data(pokemon_info):
    if not pokemon_info:
        return None
    # Insert Pokémon data into the database
    cursor.execute('''
        INSERT INTO pokemon (name, height, weight, types)
        VALUES (?, ?, ?, ?)
    ''', (pokemon_info['Name'], pokemon_info['Height'], pokemon_info['Weight'], ', '.join(pokemon_info['Types'])))
    
    # Commit changes to the database
    conn.commit()

# Prompt the user to choose a Pokémon
chosen_pokemon = input("Enter the name of a Pokémon: ")

# Get details of the chosen Pokémon
pokemon_details = get_pokemon_details(chosen_pokemon)

# Extract basic information
pokemon_info = extract_pokemon_info(pokemon_details)

if pokemon_info:
    print("\nBasic Information:")
    for key, value in pokemon_info.items():
        print(f"{key}: {value}")
else:
    print(f"Could not retrieve details for {chosen_pokemon}. Please check the Pokémon name.")

# Insert Pokémon data into the database (if available)
insert_pokemon_data(pokemon_info)

# Close the connection to the database
conn.close()

def preprocess_data(pokemon_info):
    # Add preprocessing logic here
    # Example: Convert weight from kg to pounds
    pokemon_info['Weight_pounds'] = pokemon_info['Weight'] * 2.20462
    return pokemon_info