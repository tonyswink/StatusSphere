"""
Applet: StatusSphere
Summary: Real-time office status display and update.
Description: StatusSphere is a Tidbyt app that allows users to easily display and update their current workplace status.
Author: Tony Swink
"""

load("animation.star", "animation")
load("encoding/base64.star", "base64")
load("encoding/json.star", "json")
load("http.star", "http")
load("cache.star", "cache")
load("render.star", "render")
load("schema.star", "schema")

API_URL = "http://127.0.0.1:5000/api/"
API_KEY = "YOUR_API_KEY_HERE"

API_HEADERS = {
    "Authorization": "Bearer "+API_KEY,
}

DEFAULT_NAME = "null"
DEFAULT_STATUS = "null"
DEFAULT_COLOR = "#000000"
DEFAULT_ICON = """
iVBORw0KGgoAAAANSUhEUgAAAAoAAAAICAYAAADA+m62AAAACXBIWXMAAC4jAAAuIwF4
pT92AAAAb0lEQVQYlYXOsQnCUBAG4C8khQMIGccJsoCNSFrLLCPWlklhJ7hDLDNIOovY
XOAhD3PNcT8fP8f2XDFtoQ4LHv/QJdBtDWoUP6gNdE/DD8bkPgYaUlRixgn7aO7xRJP7
5xwtC145UMZ+Y4cKhxz8Al5ZEuTs2wZwAAAAAElFTkSuQmCC
"""
DEFAULT_MESSAGE = ""

def current_status():
    # Attempt to retrieve the status from cache
    cached_status = cache.get("current_status_key")
    
    # If the status is found in cache, return it
    if cached_status:
        return json.decode(cached_status)  # Convert the cached string back to a dictionary

    # If not in cache, fetch from the API
    response = http.get(url=API_URL + "statuses/current", headers=API_HEADERS)
    
    # If the request was successful, cache and return the response
    if response and response.status_code == 200:
        status_data = response.json()
        # Store the result in cache as a string
        cache.set("current_status_key", json.encode(status_data), ttl_seconds=60)
        return status_data

    # Handle any error scenarios as needed (like returning a default status or an empty dict)
    return {}

def retrieve_color_options():
    cached_colors = cache.get("color_options_key")
    if cached_colors:
        decoded_colors = json.decode(cached_colors)
        return [schema.Option(display=color['display'], value=color['value']) for color in decoded_colors]
    
    response = http.get(url = API_URL + "colours", headers=API_HEADERS)
    
    # Check if the response was successful and contains data
    if response and response.status_code == 200:
        data = response.json()
        color_options = [schema.Option(display=color['name'], value=color['value']) for color in data]
        cache.set("color_options_key", json.encode(color_options), ttl_seconds=30)  # Cache for an hour
        return color_options
    
    # Return a default or empty list if there's an error
    return []


def retrieve_icon_options():
    cached_icons = cache.get("icon_options_key")
    if cached_icons:
        decoded_icons = json.decode(cached_icons)
        return [schema.Option(display=icon['display'], value=icon['value']) for icon in decoded_icons]
    
    response = http.get(url = API_URL + "icons", headers=API_HEADERS)

    # Check if the response was successful and contains data
    if response and response.status_code == 200:
        data = response.json()
        icon_options = [schema.Option(display=icon['name'], value=icon['value']) for icon in data]
        cache.set("icon_options_key", json.encode(icon_options), ttl_seconds=30)  # Cache for an hour
        return icon_options
    
    # Return a default or empty list if there's an error
    return []

def retrieve_icon_options_dict():
    icon_options = retrieve_icon_options()
    return {option.display: option.value for option in icon_options}

def main(config):
    status_data = current_status()
    icon_options_dict = retrieve_icon_options_dict()

    name = status_data.get("name", config.str("name", DEFAULT_NAME))
    status = status_data.get("status", config.get("status", DEFAULT_STATUS))
    color = status_data.get("color", config.get("color", DEFAULT_COLOR))
    icon = base64.decode(icon_options_dict.get(status_data.get("icon"), config.get("icon", DEFAULT_ICON)))
    message = status_data.get("message", config.get("message", DEFAULT_MESSAGE))
    animations = status_data.get("animation", config.bool("animation", False))

    if config.bool("hide_app", False):
        return []

    if not animations:
        return render.Root(
            child = render.Row(
                children = [
                    create_box(color, icon),
                    render.Padding(
                        pad = (1, 2, 0, 1),
                        child = render.Column(
                            expanded = True,
                            main_align = "space_between",
                            children = [
                                create_marquee_text(name + " is", "tom-thumb"),
                                create_marquee_text(status.upper(), "6x13"),
                                create_marquee_text(message, "tom-thumb")
                            ]
                        )
                    )
                ]
            )
        )
    else:
        return render.Root(
            child = render.Stack(
                children = [
                    create_animation(create_box(color, icon), (-64, 0), (0, 0), 282, 0),
                    create_animation(create_marquee_text(name + " is", "tom-thumb", 80, 0), (11, 34), (-53, 2), 250, 30),
                    create_animation(create_marquee_text(status.upper(), "6x13"), (11, 42), (-53, 10), 250, 30),
                    create_animation(create_marquee_text(message, "tom-thumb", 80, 0), (11, 57), (-53, 25), 250, 30)
                ]
            )
        )

def create_box(color, icon):
    return render.Box(
        color = color,
        width = 10,
        child = render.Image(src = icon, width = 10)
    )

def create_marquee_text(content, font, offset_start=0, offset_end=0, width=53):
    return render.Marquee(
        child = render.Text(content=content, font=font),
        offset_start = offset_start,
        offset_end = offset_end,
        width = width
    )

def create_animation(child, start_pos, end_pos, duration, delay):
    return animation.Transformation(
        child = child,
        duration = duration,
        delay = delay,
        keyframes = [
            animation.Keyframe(percentage = 0.0, transforms = [animation.Translate(*start_pos)], curve = "ease_in_out"),
            animation.Keyframe(percentage = 1.0, transforms = [animation.Translate(*end_pos)])
        ]
    )

def get_schema():
    color_options = retrieve_color_options()
    icon_options = retrieve_icon_options()

    return schema.Schema(
        version = "1",
        fields = [
            schema.Text(
                id = "name",
                name = "Name",
                desc = "Enter the name you want to display.",
                icon = "user",
            ),
            schema.Text(
                id = "status",
                name = "Status",
                desc = "Enter a custom status.",
                icon = "font",
            ),
            # schema.Dropdown(
            #     id = "color",
            #     name = "Color",
            #     desc = "Select a custom status color.",
            #     icon = "palette",
            #     default = color_options[1].value,
            #     options = color_options,
            # ),
            # schema.Dropdown(
            #     id = "icon",
            #     name = "Icon",
            #     desc = "Select a custom status icon.",
            #     icon = "icons",
            #     default = icon_options[6].value,
            #     options = icon_options,
            # ),
            schema.Text(
                id = "message",
                name = "Message",
                desc = "Enter a custom status message.",
                icon = "font",
            ),
            schema.Toggle(
                id = "animation",
                name = "Show Animations",
                desc = "Turn on entry and exit animations.",
                icon = "arrowsRotate",
                default = False,
            ),
            schema.Toggle(
                id = "hide_app",
                name = "Hide App",
                desc = "Hide this app so that the custom status is not shown.",
                icon = "eyeSlash",
                default = False,
            ),
        ],
    )
