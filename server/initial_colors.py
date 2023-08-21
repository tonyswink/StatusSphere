import requests

BASE_URL = "http://localhost:5000/api/colours/"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY_HERE"
}

color_options = [
    {"display": "Maroon", "value": "#800000"},
    {"display": "Red", "value": "#FF0000"},
    {"display": "Orange", "value": "#FFA500"},
    {"display": "Yellow", "value": "#FFFF00"},
    {"display": "Olive", "value": "#808000"},
    {"display": "Green", "value": "#008000"},
    {"display": "Lime", "value": "#00FF00"},
    {"display": "Cyan", "value": "#00FFFF"},
    {"display": "Light Blue", "value": "#ADD8E6"},
    {"display": "Blue", "value": "#0000FF"},
    {"display": "Dark Blue", "value": "#0000A0"},
    {"display": "Purple", "value": "#800080"},
    {"display": "Magenta", "value": "#FF00FF"},
    {"display": "White", "value": "#FFFFFF"},
    {"display": "Silver", "value": "#C0C0C0"},
    {"display": "Gray", "value": "#808080"},
    {"display": "Brown", "value": "#A52A2A"},
]

def create_color(color):
    payload = {
        "name": color["display"],
        "value": color["value"]
    }
    
    response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    
    if response.status_code == 201:
        print(f"Successfully created color: {color['display']}")
    else:
        print(f"Failed to create color: {color['display']}. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    for color in color_options:
        create_color(color)
