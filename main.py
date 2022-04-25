from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import string

app = FastAPI()
symbols_key = []
symbols_key[:0] = string.ascii_letters + string.digits
symbols_key_len = len(symbols_key)

# power 1: manage your links, 2: manage all links, 3: generate API keys
api_keys = {"123": 1, "321": 2, "333": 3}
links = {"foo": ["https://google.com", "321"], "boo": ["https://youtube.com", "123"], "bOo": ["https://reddit.com", "123"]}
generated_keys = 0


def get_link(key):
    return links[key][0]


def check_key(key):
    if key in links:
        return True
    else:
        return False


def check_power(api_key):
    if api_key in api_keys:
        return api_keys[api_key]
    else:
        return 0


def add_key(api_key, url):
    if check_power(api_key) >= 1:
        new_key = generate_key()
        links[new_key] = [url, api_key]
        return new_key
    return False


def generate_key():
    global generated_keys
    local_gen_keys = generated_keys
    generated_keys += 1
    new_key = ""
    i = 1
    while local_gen_keys > 0:
        new_key = symbols_key[local_gen_keys%pow(symbols_key_len, i)]+new_key
        local_gen_keys -= pow(symbols_key_len, i)
        i += 1
    return new_key


@app.get("/{url_id}")
async def convert_link(url_id: str):
    if not check_key(url_id):
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Link not foudn"},
        )
    else:
        return RedirectResponse(get_link(url_id))


@app.post("/create/")
async def create_link(link: str, api_key: str):
    link_id = add_key(api_key, link)
    return link_id