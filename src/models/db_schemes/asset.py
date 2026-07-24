# scheme for files

from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)  # is for file_id 
    asset_size: int = Field(ge=0, default=None)
    asset_config: dict = Field(default=None) # if their are any other config
    asset_pushed_at: datetime = Field(default=datetime.utcnow)

    # to accept value as ObjectId what ever it is.
    class Config:
        arbitrary_types_allowed = True

    # No need for object for static function ==> we use cls insted of self
    @classmethod
    def get_indexes(cls):
        # we can search by asset_project_id OR by (asset_project_id and asset_name)
        return [
            {
                "key":[
                    ("asset_project_id", 1 ) # all var we need to do index for it ("name", ase = 1, des = -1)

                ],
                "name":"asset_project_id_index_1",
                "unique" : False   # all the value unique or not

            },
            {
                "key":[
                    ("asset_project_id", 1 ),
                    ("asset_name", 1 )
                ],
                "name":"asset_project_id_name_index_1",
                "unique" : True   # all the value unique or not

            }
        ]
    
