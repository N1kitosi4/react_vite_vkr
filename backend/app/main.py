from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import user, book, review, recommendations, recs


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static/avatars", StaticFiles(directory="app/uploads/avatars"), name="avatars")
app.mount("/static/book_images", StaticFiles(directory="app/uploads/book_images"), name="book_images")
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(user.router, prefix="/users")
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(review.router, prefix="/reviews", tags=["Reviews"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(recs.router, prefix="/recs", tags=["Recs"])


@app.get("/")
def root():
    return {"message": "Welcome to the Book Reviews App"}
