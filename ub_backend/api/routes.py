import random
from fastapi import APIRouter, Depends
from aiohttp import ClientSession
from fastapi.responses import HTMLResponse
from loguru import logger

from ub_backend.app.model.enum.cat_mode import CatMode
from ub_backend.app.model.enum.color import Color

from .v1.all_routes import router as v1_router
from .depends import http_client

router = APIRouter(prefix="/api")

@router.get("/cat_say")
async def cat_say(phrase: str = None, mode: CatMode = None, http_cli: ClientSession = Depends(http_client)):
    if not mode:
        mode = CatMode.default

    async def render_cat(phrase: str):
        if phrase:
            cat = f"""
               MMM.           .MMM
               MMMMMMMMMMMMMMMMMMM
               MMMMMMMMMMMMMMMMMMM      _{"_" * len(phrase)}_
              MMMMMMMMMMMMMMMMMMMMM    | {" " * len(phrase)} |
             MMMMMMMMMMMMMMMMMMMMMMM   | {phrase} |
            MMMMMMMMMMMMMMMMMMMMMMMM   |_   {"_" * (len(phrase) - 3)}_|
            MMMM::- -:::::::- -::MMMM    |/
             MM~:~ 00~:::::~ 00~:~MM
        .. MMMMM::.00:::+:::.00::MMMMM ..
              .MM::::: ._. :::::MM.
                 MMMM;:::::;MMMM
          -MM        MMMMMMM
          ^  M+     MMMMMMMMM
              MMMMMMM MM MM MM
                   MM MM MM MM
                   MM MM MM MM
                .~~MM~MM~MM~MM~~.
             ~~~~MM:~MM~~~MM~:MM~~~~
            ~~~~~~==~==~~~==~==~~~~~~
             ~~~~~~==~==~==~==~~~~~~
                 :~==~==~==~==~~
        """
        else:
            async with http_cli.get("https://api.github.com/octocat") as resp:
                cat = await resp.text()

        return cat
    
    async def render_content() -> HTMLResponse:
        cat = await render_cat(phrase=phrase)
        if mode == CatMode.rainbow:
            cat = "".join([f'<span style="color:{random.choice(list(Color))}">{char}</span>' for char in cat])
            
        styles = {
            CatMode.default: {
                "bgcolor": "white",
                "color": "black"
            },
            CatMode.dark: {
                "bgcolor": "black",
                "color": "white"
            },
            CatMode.rainbow: {
                "bgcolor": "cyan",
                "color": "black"
            },
        }
        return HTMLResponse(content=f"""
<html><head>
<style>
body {{
  background-color: {styles.get(mode).get("bgcolor")};
  color: {styles.get(mode).get("color")};
}}
div {{
    font-size: 0.6vw;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -9vw;
    margin-left: -12vw;
}}
</style>
</head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">
<div>
{cat}
</div>
</pre></body></html>
    """, status_code=200)

    return await render_content()

router.include_router(v1_router)
