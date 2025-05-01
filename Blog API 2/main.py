import logging
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import database
from datetime import datetime


#new-----------------------------------
import uvicorn ##ASGI
from StackModels import StackModel ##Pydantic model for stack data
import pickle ##For serialization and deserialization of stack data
import numpy as np ##For numerical operations
import pandas as pd ##For reading and processing CSV files
import io ##For handling file objects

class CSVPredictionResponse(BaseModel):
    predictions: List[float]

# Add XGBoost import - this is required for loading the model
try:
    import xgboost
except ImportError:
    logging.error("XGBoost is not installed. Please install it using: pip install xgboost")
    raise ImportError("XGBoost is not installed. Please install it using: pip install xgboost")

#new-----------------------------------

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Blog API", description="A simple blog platform API")


#new-----------------------------------
# Load the model with proper error handling
try:
    pickle_in = open("stack_model.pkl", "rb") ##Load the pickled model 
    classifier = pickle.load(pickle_in) ##Load the model into a variable
    pickle_in.close()
except FileNotFoundError:
    logger.error("stack_model.pkl file not found")
    classifier = None
except ModuleNotFoundError as e:
    logger.error(f"Missing module: {e}")
    classifier = None
except Exception as e:
    logger.error(f"Error loading model: {e}")
    classifier = None


@app.post('/predict-from-combined-csv', response_model=CSVPredictionResponse)
async def predict_from_combined_csv():
    if classifier is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Check server logs for details.")
    
    try:
        # Read the combined.csv file
        df = pd.read_csv('combined.csv')
        
        # Make predictions using the loaded model
        predictions = classifier.predict(df)
        
        return {"predictions": predictions.tolist()}
    except FileNotFoundError:
        logger.error("combined.csv file not found")
        raise HTTPException(status_code=404, detail="combined.csv file not found")
    except Exception as e:
        logger.error(f"Error during combined.csv prediction: {e}")
        raise HTTPException(status_code=500, detail=f"combined.csv prediction failed: {str(e)}")


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