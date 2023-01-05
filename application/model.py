import datetime
from dateutil.relativedelta import relativedelta
from flask import url_for
import markdown
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from application.database import db
import pytz
from application.configuration import BaseConfiguration

local_timezone = pytz.timezone(BaseConfiguration.LOCAL_TIMEZONE)

class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(64), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    blood = db.Column(db.String(3))
    reference = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=True, unique=True)
    address = db.Column(db.String(64))
    avatar = db.Column(db.String(128))
    analysis = db.Column(db.Text)
    case_photo_1 = db.Column(db.String(128))
    case_photo_2 = db.Column(db.String(128))
    case_photo_3 = db.Column(db.String(128))
    case_photo_4 = db.Column(db.String(128))
    admin = db.Column(db.SmallInteger, nullable=False, default=0)
    active = db.Column(db.SmallInteger, nullable=False, default=0)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(datetime.timezone.utc))
    author_desc = db.relationship("User", remote_side=[id])

    def __repr__(self):
        return f"<User: {self.id}>"

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plaintext_password):
        self.password_hash = generate_password_hash(plaintext_password, method="sha256")

    def check_password(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)

    def get_id(self):
        return self.username

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin

    def to_dict(self):
        avatar = ""
        if self.avatar:
            avatar = url_for("static", filename=f"img/user-avatar/{self.avatar}")
        elif not self.avatar and self.sex == "M":
            avatar = url_for("static", filename="img/default-avatar-male.png")
        elif not self.avatar and self.sex == "F":
            avatar = url_for("static", filename="img/default-avatar-female.png")
        else:
            avatar = url_for("static", filename="img/default-avatar-other.png")

        case_photo_1 = "img/case-photo/" + self.case_photo_1 if self.case_photo_1 else "img/default-case-photo.png"
        case_photo_2 = "img/case-photo/" + self.case_photo_2 if self.case_photo_2 else "img/default-case-photo.png"
        case_photo_3 = "img/case-photo/" + self.case_photo_3 if self.case_photo_3 else "img/default-case-photo.png"
        case_photo_4 = "img/case-photo/" + self.case_photo_4 if self.case_photo_4 else "img/default-case-photo.png"

        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "dob": self.dob,
            "dob_str": self.dob.strftime("%Y-%m-%d"),
            "age": "{0.years}y {0.months}m {0.days}d".format(relativedelta(datetime.date.today(), self.dob)),
            "sex": self.sex,
            "blood": self.blood,
            "reference": self.reference,
            "email": self.email,
            "address": self.address,
            "avatar": avatar,
            "analysis": markdown.markdown(self.analysis or "", extensions=["fenced_code", "nl2br"]),
            "case_photo_1": url_for("static", filename=case_photo_1),
            "case_photo_2": url_for("static", filename=case_photo_2),
            "case_photo_3": url_for("static", filename=case_photo_3),
            "case_photo_4": url_for("static", filename=case_photo_4),
            "admin": self.admin,
            "active": self.active,
            "author": self.author,
            "created_at": self.created_at.replace(tzinfo=pytz.utc)
            .astimezone(local_timezone)
            .strftime("%Y-%m-%d %H:%M:%S"),
            "modified_at": self.modified_at,
            "author_username": self.author_desc.username,
        }


class Prescription(db.Model):

    __tablename__ = "prescription"

    id = db.Column(db.Integer, primary_key=True)
    prescription = db.Column(db.Text)
    note = db.Column(db.Text)
    follow_up_date = db.Column(db.Date)
    parcel_date_1 = db.Column(db.Date)
    parcel_photo_1 = db.Column(db.String(128))
    patient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(datetime.timezone.utc))
    author_desc = db.relationship("User", foreign_keys=author)
    patient_desc = db.relationship("User", foreign_keys=patient_id)

    def __repr__(self):
        return f"<Prescription: {self.id}>"

    def to_dict(self):
        parcel_photo_1 = f"img/parcel-photo/{self.parcel_photo_1}" if self.parcel_photo_1 else "img/default-parcel-photo.png"
        return {
            "id": self.id,
            "prescription": markdown.markdown(self.prescription or "", extensions=["fenced_code", "nl2br"]),
            "note": markdown.markdown(self.note or "", extensions=["fenced_code", "nl2br"]),
            "follow_up_date": self.follow_up_date,
            "author": self.author,
            "parcel_date_1": self.parcel_date_1,
            "parcel_photo_1": url_for("static", filename=parcel_photo_1),
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "author_username": self.author_desc.username,
            "patient_username": self.patient_desc.username,
        }


class Conversation(db.Model):

    __tablename__ = "conversation"

    id = db.Column(db.Integer, primary_key=True)
    conversation = db.Column(db.String(128))
    read = db.Column(db.SmallInteger, default=0)
    patient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    conversation_attachment = db.Column(db.String(128))
    conversation_attachment_type = db.Column(db.String(8))
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(datetime.timezone.utc))
    author_desc = db.relationship("User", foreign_keys=author)
    patient_desc = db.relationship("User", foreign_keys=patient_id)
    admin_desc = db.relationship("User", foreign_keys=admin_id)

    def __repr__(self):
        return f"<Conversation: {self.id}>"

    def to_dict(self):
        conversation_attachment = url_for("static", filename=f"img/conversation-photo/{self.conversation_attachment}")
        return {
            "id": self.id,
            "conversation": self.conversation,
            "conversation_attachment": self.conversation_attachment,
            "patient_id": self.patient_id,
            "author": self.author,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "author_username": self.author_desc.username,
            "patient_username": self.patient_desc.username,
            "admin_username": self.admin_desc.username,
        }


class Medicine(db.Model):

    __tablename__ = "medicine"

    id = db.Column(db.Integer, primary_key=True)
    medicine = db.Column(db.String(128))
    potency = db.Column(db.String(128))
    short_name = db.Column(db.String(128), unique=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(datetime.timezone.utc))
    author_desc = db.relationship("User", foreign_keys=author)

    def __repr__(self):
        return f"<Medicine: {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "medicine": self.medicine,
            "short_name": self.short_name,
            "author": self.author,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "author_username": self.author_desc.username,
            "patient_username": self.patient_desc.username,
        }


class Organization(db.Model):

    __tablename__ = "organization"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    title = db.Column(db.String(128))
    logo = db.Column(db.String(128))
    description = db.Column(db.String(128))
    address = db.Column(db.String(128))
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(datetime.timezone.utc))
    author_desc = db.relationship("User", foreign_keys=author)

    def __repr__(self):
        return f"<Organization: {self.id}>"
