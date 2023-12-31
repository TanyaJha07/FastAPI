from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas, oauth2,database, models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
from sqlalchemy.orm import Session   
#secret key
#Algorithm
#expiration time

SECRET_KEY = "123XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        print("token", token)
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        print("payload", payload)
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    print(token, "gokul")
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first   
    return user
    