from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import utils

app = FastAPI()


@app.get("/{url_id}")
async def convert_link(url_id: str):
    if not utils.check_key(url_id):
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"Error": "Link not found"},
        )
    else:
        return RedirectResponse(utils.get_link(url_id))


@app.post("/create/")
async def create_link(link: str, api_key: str):
    return utils.add_key(api_key, link)


@app.delete("/delete/")
def delete_hero(url_id: str, api_key: str):
    return utils.remove_key(url_id, api_key)