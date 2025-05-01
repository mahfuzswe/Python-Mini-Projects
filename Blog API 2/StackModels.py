from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class StackModel(BaseModel):
    prediction: Optional[float] = None
    
    # Add the features your model expects here
    # For example, if your model takes features like 'age', 'income', etc.:
    # age: float
    # income: float
    # ...
    
    # Generic approach to allow any number of features
    class Config:
        extra = "allow"