import logging
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import database
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Blog API", description="A simple blog platform API")

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Dependency to get DB connection
def get_db():
    connection = database.get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        yield connection
    finally:
        if connection.is_connected():
            connection.close()

@app.on_event("startup")
async def startup_event():
    # Optionally initialize a connection pool here if implemented
    database.init_db()

@app.post("/posts/", response_model=Post)
async def create_post(post: PostCreate, connection=Depends(get_db)):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO posts (title, content) VALUES (%s, %s)",
            (post.title, post.content)
        )
        connection.commit()
        post_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        result = cursor.fetchone()
        
        return Post(
            id=result[0],
            title=result[1],
            content=result[2],
            created_at=result[3]
        )
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.get("/posts/", response_model=List[Post])
async def read_posts(connection=Depends(get_db)):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
        posts = cursor.fetchall()
        return [Post(**post) for post in posts]
    except Exception as e:
        logger.error(f"Error reading posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: int, connection=Depends(get_db)):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post_record = cursor.fetchone()
        
        if post_record is None:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return Post(**post_record)
    except Exception as e:
        logger.error(f"Error reading post {post_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: int, post: PostCreate, connection=Depends(get_db)):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE posts SET title = %s, content = %s WHERE id = %s",
            (post.title, post.content, post_id)
        )
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Post not found")
        
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        result = cursor.fetchone()
        
        return Post(
            id=result[0],
            title=result[1],
            content=result[2],
            created_at=result[3]
        )
    except Exception as e:
        logger.error(f"Error updating post {post_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, connection=Depends(get_db)):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return {"message": "Post deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting post {post_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()