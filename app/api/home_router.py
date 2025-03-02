from fastapi import APIRouter

home_page_router = APIRouter(tags=["Home"])


@home_page_router.get("/")
async def index() -> dict:
    return {"message": "🤖🚀✨ Fastapi Backnend Challenge 🤖🚀✨"}
