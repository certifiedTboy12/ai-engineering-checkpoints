from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from app.models.users import User
from app.exceptions.custom import CustomException
from app.helpers.auth_helpers import hash_password, generate_random_otp
from app.config.dbconfig import SessionLocal


def create_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str
) -> User:
    db = SessionLocal()
    try:
        user_exist = db.query(User).filter(User.email == email).first()

        otp = generate_random_otp()
        otp_expiry = datetime.now() + timedelta(minutes=10)

        if user_exist and user_exist.is_verified:
            raise CustomException(
                status_code=400,
                detail="User already exists"
            )

        if user_exist and not user_exist.is_verified:
            user_exist.first_name = first_name
            user_exist.last_name = last_name
            user_exist.otp = otp
            user_exist.otp_expiry = otp_expiry
            user_exist.password = hash_password(password)

            db.add(user_exist)
            db.commit()
            db.refresh(user_exist)

            return user_exist

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            otp=otp,
            otp_expiry=otp_expiry,
            password=hash_password(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()

        raise CustomException(
            status_code=409,
            detail="A user with this email already exists"
        )
    except Exception as e:
        print(e)
        raise CustomException(
            status_code=500,
            detail=str(e)
        )
    finally:
        db.close()







def verify_user(opt: str):
    db = SessionLocal()
    try:
        user_exist = get_user_by_otp(opt)

        if user_exist:
            if user_exist.otp_expiry and user_exist.otp_expiry > datetime.now():
                user_exist.is_verified = True
                user_exist.otp = None
                user_exist.otp_expiry = None
               
                db.add(user_exist)
                db.commit()
                db.refresh(user_exist)
        
                return user_exist
            else:
                raise CustomException(
                    status_code=400,
                    detail="OTP has expired"
                )
        
    except Exception as e:
        raise CustomException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()


def generate_new_otp(email: str):
    db = SessionLocal()
    try:
        user_exist = get_user_by_email(email)

        if isinstance(user_exist, User) and user_exist.is_verified is False:
           
            user_exist.otp = generate_random_otp()
            user_exist.otp_expiry = datetime.now() + timedelta(minutes=10)
            
            db.add(user_exist)
            db.commit()
            db.refresh(user_exist)
            return user_exist
    except Exception as e:

        raise CustomException(
            status_code=500,
            detail=str(e)
        )


def get_user_by_email(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_id(id: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise CustomException(
            status_code=404,
            detail=f"User with id {id} not found"
        )

    return user


def get_user_by_otp(otp: str):
    db = SessionLocal()
    user = db.query(User).filter(User.otp == otp).first()

    if not user:
        raise CustomException(
            status_code=404,
            detail="Invalid or expired OTP"
        )

    return user