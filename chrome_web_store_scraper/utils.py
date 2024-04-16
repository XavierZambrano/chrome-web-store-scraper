import re
import json
from chrome_web_store_scraper.errors import InvalidManifest


def script_text_to_json(text):
    data = re.search(r'''data:(.*?), sideChannel: {}}\);$''', text).group(1)
    return json.loads(data)


def load_manifest(manifest_raw: str) -> dict:
    # Remove BOM
    manifest = manifest_raw.replace(u'\ufeff', '')

    return json.loads(manifest)


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


def format_script_data(script_data: list):
    images = [image_raw[-1] for image_raw in script_data[5]]
    address = script_data[10][-1] if script_data[10][-1] else ''
    address += '\n'
    address += script_data[10][1] if script_data[10][1] else ''

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
        'screenshots': images,
        'overview': script_data[6],
        'version': script_data[13],
        'size': script_data[15],
        'languages': script_data[16],
        'last_updated': script_data[14][0],
        'developer': {
            'name': script_data[10][5],
            'address': address,  # TODO fix
            'website': script_data[0][7],  # TODO fix
            'email': script_data[10][0],
            'trader': script_data[10][3]
        },

    }

    data['created_by_the_website_owner'] = True if data['website_owner'] else False

    return data


def script_to_data(script_text):
    data_raw = script_text_to_json(script_text)
    data = format_script_data(data_raw)
    return data
