from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from platform_sdk import Portal, User

from .data import urlaubstage_von

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")  # autoescape ist an


def build_router(portal: Portal) -> APIRouter:
    router = portal.router()

    @router.get("/", response_class=HTMLResponse, dependencies=[Depends(portal.requires("employee"))])
    async def home(user: User = Depends(portal.user)) -> str:
        tage = [
            {"datum": tag.datum.strftime("%d.%m.%Y"), "iso": tag.datum.isoformat(), "grund": tag.grund}
            for tag in urlaubstage_von(user.sub)
        ]
        body = templates.get_template("page.html").render(tage=tage)
        return await portal.layout(title="Meine Urlaubstage", body=body, current=portal.url("/"), user=user)

    return router
