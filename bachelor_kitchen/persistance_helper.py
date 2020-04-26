from bachelor_kitchen import db
from bachelor_kitchen.models import User

def persistUser(username, password, email, firstname, lastname, phonenum, address, city, zipcode, state, dob, university):
    user = User(username=username,
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            phonenum=phonenum,
            address=address,
            city=city,
            zipcode=zipcode,
            state=state,
            dob=dob,
            university=university
            )
    db.session.add(user)
    db.session.commit()
    
def getUser(email, password):
    user = User.query.filter_by(email=email).first()
    if (user and user.password == password):
        return user
    else:
        return None