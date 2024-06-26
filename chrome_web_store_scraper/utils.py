import re
import json
from chrome_web_store_scraper.errors import InvalidManifest
import pyjson5


def script_text_to_json(text):
    data = re.search(r'''data:(.*?), sideChannel: {}}\);$''', text).group(1)
    return json.loads(data, strict=False)


def load_manifest(manifest_raw: str) -> dict:
    try:
        # Remove BOM
        manifest = manifest_raw.replace(u'\ufeff', '')
        return json.loads(manifest, strict=False)
    except json.JSONDecodeError:
        return pyjson5.loads(manifest_raw)


def is_manifest_valid(manifest):
    if not isinstance(manifest, dict):
        return False

    if 'name' not in manifest or 'version' not in manifest:
        return False

    return True


def get_users(script_data: list):
    if len(script_data[0]) > 14:
        users = script_data[0][14]
        return users
    else:
        return 0


def get_screenshots(script_data: list):
    if script_data[5]:
        screenshots = [image_raw[-1] for image_raw in script_data[5]]
    else:
        screenshots = []

    return screenshots


def get_developer(script_data: list):
    if script_data[10]:
        developer = {
            'name': script_data[10][5] if len(script_data[10]) > 5 else None,
            'email': script_data[10][0],
        }
    else:
        developer = {
            'name': None,
            'email': None,
        }
    return developer


def format_script_data(script_data: list):
    manifest = load_manifest(script_data[20])

    if not is_manifest_valid(manifest):
        raise InvalidManifest('Invalid manifest')
    if 'theme' in manifest.keys():
        type = 'Theme'
    elif 'app' in manifest.keys():
        type = 'App'
    else:
        type = 'Extension'

    data = {
        'id': script_data[0][0],
        'icon': script_data[0][1],
        'small_promo_tile': script_data[0][5],
        'title': script_data[0][2],
        'website_owner': script_data[0][7],
        'rating': script_data[0][3],
        'rating_count': script_data[0][4],
        'type': type,
        'category': script_data[0][11][0] if script_data[0][11] else None,
        'users': get_users(script_data),
        'screenshots': get_screenshots(script_data),
        'overview': script_data[6],
        'version': script_data[13],
        'size': script_data[15],
        'languages': script_data[16],
        'last_updated': script_data[14][0],
        'developer': get_developer(script_data)
    }

    data['created_by_the_website_owner'] = True if data['website_owner'] else False

    return data


def script_to_data(script_text):
    data_raw = script_text_to_json(script_text)
    data = format_script_data(data_raw)
    return data
