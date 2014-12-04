from app import db
from datetime import datetime
from sqlalchemy import desc

import random


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(15), unique=True)
    active = db.Column(db.Boolean)
    unsub = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)

    @staticmethod
    def insert_phone(phone_number):
        phone = Phone(
            number=phone_number,
            active=False,
            unsub=False,
            created_at=datetime.now()
        )
        db.session.add(phone)
        db.session.commit()
        return phone

    def unsubscribe(self):
        self.active = False
        self.unsub = True
        db.session.commit()

    def activate(self):
        self.active = True
        self.unsub = False
        db.session.commit()


class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5))
    phone_id = db.Column(db.Integer, db.ForeignKey('phone.id'))
    created_at = db.Column(db.DateTime)

    @staticmethod
    def generate_ver_code(phone):
        verification = Verification(
            code=make_random_str(5),
            phone_id=phone.id,
            created_at=datetime.now()
        )
        db.session.add(verification)
        db.session.commit()
        return verification


def make_random_str(length):
    char = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(char) for i in range(length))


def check_verification_code(phone, code):
    ver = Verification.query.filter_by(phone_id=phone.id).order_by(
        desc(Verification.created_at)).first()
    if ver is None:
        return False
    return ver.code == code
