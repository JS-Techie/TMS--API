from string import Template



CRUD_code_temp= Template(
'''
from fastapi import APIRouter, Response, Depends



router = APIRouter(prefix='$router_prefix_path')


from models.models import $model_class as $model
from Types.$types_class import $create_type_class, $update_type_class
from services.middleware import authenticateAdmin
from config.db_engine import Session



session = Session()



async def middleware():
    authenticateAdmin



@router.post('/create', dependencies=[Depends(middleware)])
async def create(req:$create_type_class):
    createData= None
    try:
        
        createData = $model( _id= req. _id,  _id= req. _id  ,status=True, created_by=req.created_by)
        session.add(createData)
        
    except Exception as e:
        
        session.rollback()
        Response.status_code = 500
        return{
            "data": str(e),
            "client_message":"Unknown Error. PLEASE TRY AGAIN LATER",
            "dev_message":"Exception Met.",
            "success":False
        }
        
    else:
        
        session.commit()       
        if not createData:    
            Response.status_code=400 
            return{
                "data":{},
                "client_message":"No Data Inserted",
                "dev_message":"insertion error. no rows inserted",
                "success":False
            }        
                        
        print("Created :",createData.id)
        Response.status_code=200 
        return{
            "data":createData,
            "client_message":"Data Insertion Successful",
            "dev_message":"row generation successful",
            "success":True
        }
        
    finally:
        
        session.close()



@router.get('/view', dependencies=[Depends(middleware)])
def view(Id: str | None = None, limit: int |None = None, offset: int| None=None ):
    try:
        
        fetchData=None
        if Id is None and limit is None and offset is None:
            fetchData = session.query($model).filter($model.status == True).all()
        if Id is None and limit is not None and offset is not None:
            fetchData = session.query($model).filter($model.status == True).limit(int(limit)).offset(int(offset)).all()
        if Id is not None:
            fetchData = session.query($model).filter($model.id == Id and $model.status == True).first()
        if not fetchData:
            Response.status_code=404
            return{
                    "data":{},
                    "client_message":"No Data Available",
                    "dev_message":"no rows available show ",
                    "success":False
                }
        Response.status_code=200
        return{
                "data":fetchData,
                "client_message":"Data Fetched Successful",
                "dev_message":"row fetching successful",
                "success":True
            }
    except Exception as e:
        
        Response.status_code = 500
        return {
            "data": str(e),
            "client_message":"Unknown Error. PLEASE TRY AGAIN LATER",
            "dev_message":"Exception Met.",
            "success":False
        }
        
    finally:
        session.close()
        




@router.delete('/delete/{Id}', dependencies=[Depends(middleware)])            
def delete(Id: str):

    try:
        
        fetchData = session.query($model).filter($model.id == Id and $model.status == True).first()
        
        if not fetchData:
            Response.status_code= 404
            return{
                    "data":{},
                    "client_message":"No Data Available With The Given Credentials",
                    "dev_message":"no rows available with the provided attribute values",
                    "success":False
                }
        
        fetchData.status = False


    except Exception as e:
        
        session.rollback()
        Response.status_code = 500
        return {
            "data": str(e),
            "client_message":"Unknown Error. PLEASE TRY AGAIN LATER",
            "dev_message":"Exception Met.",
            "success":False
        }
        
    else:
        
        session.commit()
        print("deleted :",fetchData.id)
        if not fetchData:
            Response.status_code=400       
            return{
                    "data":{},
                    "client_message":"No Data Deleted",
                    "dev_message":"no rows deleted.",
                    "success":False
                    }
                
        Response.status_code=204
        return{
            "data":{},
            "client_message":"Data Deleted Successfully",
            "dev_message":"row deletion successful",
            "success":True
        }
                
        
    finally:
        
        session.close()
            
        
        
        

@router.patch('/update/{Id}', dependencies=[Depends(middleware)])
def update(req: $update_type_class, Id :str):
    fetchData = None
    try:    
        
        fetchData = session.query($model).filter($model.status==True and $model.id == Id).first()
        
        if not fetchData:
            Response.status_code= 404
            return{
                    "data":{},
                    "client_message":"No Data Available With The Given Credentials",
                    "dev_message":"no rows available with the provided attribute values",
                    "success":False
                }
        
        updateCount=0
        for key, value in req:
            if value is not None:
                try:
                    if getattr(fetchData, key) != value:
                        setattr(fetchData, key, value)
                        updateCount=updateCount+1
                        
                    fetchData.updated_at = "NOW()"
                except Exception as e:
                    return {
                        "data": f"Error assigning value to attribute '{key}': {str(e)}",
                        "client_message":"Unknown Error. PLEASE TRY AGAIN LATER",
                        "dev_message":"Exception Met.",
                        "success":False
                    }
                    
            
    except Exception as e:
        
        session.rollback()
        Response.status_code = 500
        return {
            "data": str(e),
            "client_message":"Unknown Error. PLEASE TRY AGAIN LATER",
            "dev_message":"Exception Met.",
            "success":False
        }
        
    else:
        
        if updateCount == 0:
            Response.status_code=400       
            return {
                "data":{},
                "client_message":"No New Data to Update",
                "dev_message":"no rows updated due to lack of new data.",
                "success":False                
            }
        session.commit()
        if not fetchData:
            Response.status_code=400       
            return{
                        "data":{},
                        "client_message":"No Data Updated",
                        "dev_message":"no rows updated.",
                        "success":False
                    }
            
        print("UPDATED ::",fetchData.id)
        Response.status_code=200
        return{
            "data":fetchData,
            "client_message":"Data Updated Successfully",
            "dev_message":"row updation successful",
            "success":True
        }
        
    finally:
        
        session.close()


'''            
)




Type_Code_temp= Template(
    '''
from pydantic import BaseModel
from datetime import datetime


class $create_type_class(BaseModel):

    _id: str
    _id: str
    created_by:str
    
    class Config:
        orm_mode=True
        
        


class $update_type_class(BaseModel):

    _id: str | None= None
    _id: str | None= None
    updated_by:str
    status: bool |None=None

    
    class Config:
        orm_mode=True

    
    '''
    
)



def main():
    router_prefix_path=input("Enter the Prefix path for your Router :")
    model_class=input("\nEnter the name of the first model class needed :")
    model= model_class+"Model"
    types_class= model_class[3:]+"MasterTypes"
    create_type_class= model_class+"CreateReq"
    update_type_class= model_class+"UpdateReq"
    
    CRUD_code= CRUD_code_temp.safe_substitute(
        router_prefix_path = router_prefix_path, 
        model_class = model_class,
        model= model,
        types_class = types_class,
        create_type_class= create_type_class,
        update_type_class= update_type_class,
        
        )
    
    Type_code = Type_Code_temp.safe_substitute(
        create_type_class= create_type_class,
        update_type_class= update_type_class
    )
    
    controller_path = input("\nEnter the file name for the controller :")
    controllerdoc = open('../controllers/masterController/'+controller_path, mode='w+', encoding='utf-8')
    controllerdoc.write(CRUD_code)
    controllerdoc.close()
    
    type_path = input("\nEnter the file name for the types :")
    typedoc = open('../Types/'+type_path, mode='w+', encoding='utf-8')
    typedoc.write(Type_code)
    typedoc.close()


if __name__== "__main__":
    main()