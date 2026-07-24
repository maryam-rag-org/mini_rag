from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)


    
    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')

        return value

    # to accept value as ObjectId what ever it is.
    class Config:
        arbitrary_types_allowed = True

    # No need for object for static function ==> we use cls insted of self
    @classmethod
    def get_indexes(cls):

        return [
            {
                "key":[
                    ("project_id", 1 ) # all var we need to do index for it ("name", ase = 1, des = -1)
                ],
                "name":"project_id_index_1",
                "unique" : True   # all the value unique or not

            }
        ]
    
    
