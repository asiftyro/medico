from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    SelectField,
    SubmitField,
    TextAreaField,
    PasswordField,
    BooleanField,
    HiddenField,
    DecimalField,
)


from wtforms.validators import ValidationError, Email, InputRequired, Optional, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
from application.model import User, PaymentDescription, PaymentMethod


class NumbersOnly(object):
    def __init__(self, message="Numbers allowed only."):
        self.message = message

    def __call__(self, form, field):
        for c in field.data:
            if c not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                raise ValidationError(self.message)


class Unique(object):
    def __init__(self, model, field_name, message="Item already exists."):
        self.model = model
        self.field_name = field_name
        self.message = message

    def __call__(self, form, field):
        query_result = self.model.query.filter(self.field_name == field.data).first()
        if query_result:
            raise ValidationError(self.message)


class UniqueUserOnUpdate(object):
    def __init__(self, model, field_name, user_id_field, message="Item already exists."):
        self.model = model
        self.field_name = field_name
        self.user_id_field = user_id_field
        self.message = message

    def __call__(self, form, field):
        user_id = form[self.user_id_field].data
        query_result = self.model.query.filter(self.field_name == field.data).first()
        if query_result and (query_result.id != int(user_id.strip())):
            raise ValidationError(self.message)


class CreateUserForm(FlaskForm):
    username = StringField(
        "Mobile (Username)",
        validators=[
            Unique(User, User.username, "Mobile/Username already exists."),
            NumbersOnly(),
            InputRequired(),
            Length(min=4, max=16),
        ],
    )
    password = StringField("Password", validators=[InputRequired(), Length(min=4, max=16)])
    fullname = StringField("Full Name", validators=[InputRequired(), Length(min=4, max=64)])
    nickname = StringField(
        "Nick Name",
        validators=[
            Unique(User, User.nickname, "Nick name already exists."),
            Optional(strip_whitespace=True),
            Length(max=32),
        ],
        filters=[lambda x: x or None]
    )





    # dob = DateField("Date of Birth", validators=[InputRequired()])
    age = StringField("Age", validators=[NumbersOnly(),InputRequired()])
    sex = SelectField("Sex", choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
    blood = SelectField(
        "Blood Group",
        choices=[
            ("U", "Unknown"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
        ],
    )
    reference = StringField("Reference", validators=[Length(max=64)])
    email = StringField(
        "Email", validators=[Email(), Optional(strip_whitespace=True), Length(max=64)], filters=[lambda x: x or None]
    )
    address = StringField("Address", validators=[Length(max=64)])
    avatar = FileField(
        "Patient' Photo", validators=[FileAllowed(["jpg", "png", "jpeg"], "Allowed JPG or PNG Images only.")]
    )
    active = SelectField("Active", choices=[(1, "Yes"), (0, "No")])
    # admin = SelectField('Admin', choices=[(0, "No"), (1, "Yes")])
    save = SubmitField("Save")


class EditUserForm(FlaskForm):
    id = HiddenField("user_id")
    username = StringField(
        "Mobile (Username)",
        validators=[
            UniqueUserOnUpdate(User, User.username, "id", "Mobile/Username already exists."),
            NumbersOnly(),
            InputRequired(),
            Length(min=4, max=16),
        ],
    )
    fullname = StringField("Full Name", validators=[InputRequired(), Length(min=4, max=64)])
    nickname = StringField(
        "Nick Name",
        validators=[
            Unique(User, User.nickname, "Nick name already exists."),
            InputRequired(),
            Length(min=2, max=32),
        ],
    )
    dob = DateField("Date of Birth", validators=[InputRequired()])
    sex = SelectField("Sex", choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
    blood = SelectField(
        "Blood Group",
        choices=[
            ("U", "Unknown"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
        ],
    )
    reference = StringField("Reference", validators=[Length(max=64)])
    email = StringField(
        "Email", validators=[Email(), Optional(strip_whitespace=True), Length(max=64)], filters=[lambda x: x or None]
    )
    address = StringField("Address", validators=[Length(max=64)])
    avatar = FileField(
        "Patient's Photo", validators=[FileAllowed(["jpg", "png", "jpeg"], "Allowed JPG or PNG Images only.")]
    )
    active = SelectField("Active", choices=[(1, "Yes"), (0, "No")])
    # admin = SelectField('Admin', choices=[(0, "No"), (1, "Yes")])
    save = SubmitField("Save")


class CaseAnalysisForm(FlaskForm):
    analysis = TextAreaField(
        "Case Analysis",
        validators=[Optional(strip_whitespace=True), Length(max=2048)],
        filters=[lambda x: x or None],
        render_kw={"rows": 10},
    )
    case_photo_1 = FileField(
        "Case Photo 1", validators=[FileAllowed(["jpg", "png", "jpeg"], "Allowed JPG or PNG Images only.")]
    )
    case_photo_2 = FileField(
        "Case Photo 2", validators=[FileAllowed(["jpg", "png", "jpeg"], "Allowed JPG or PNG Images only.")]
    )
    case_photo_3 = FileField(
        "Case Photo 3", validators=[FileAllowed(["jpg", "png", "jpeg"], "Allowed JPG or PNG Images only.")]
    )
    case_photo_4 = FileField(
        "Case Photo 4", validators=[FileAllowed(["jpg", "png", "jpeg"], "Allowed JPG or PNG Images only.")]
    )
    save = SubmitField("Save")


class PrescriptionCreateForm(FlaskForm):
    prescription = TextAreaField(
        "Prescription",
        validators=[Optional(strip_whitespace=True), Length(max=2048)],
        filters=[lambda x: x or None],
        render_kw={"rows": 10},
    )
    follow_up_date = DateField(
        "Follow up date", validators=[Optional(strip_whitespace=True)], filters=[lambda x: x or None]
    )
    note = TextAreaField(
        "Notes/Outcome/Observation",
        validators=[Optional(strip_whitespace=True), Length(max=2048)],
        filters=[lambda x: x or None],
        render_kw={"rows": 10},
    )
    save = SubmitField("Save")


class PrescriptionEditForm(PrescriptionCreateForm):
    pass


class LoginForm(FlaskForm):
    username = StringField("Mobile/Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")


class ConversationForm(FlaskForm):
    conversation = StringField("Send Message", validators=[InputRequired(), Length(max=128)])
    conversation_attachment = FileField(
        "Send Photo/Video",
        validators=[
            FileAllowed(
                ["jpg", "png", "jpeg", "mpeg", "mpg", "aac", "avi", "mov", "mp4"], "Allowed Images & Video only."
            )
        ],
    )
    send = SubmitField("Send")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[InputRequired(), Length(min=4, max=16)])
    verify_password = PasswordField(
        "Verify new Password", validators=[EqualTo("password", message="Password must match.")]
    )
    submit = SubmitField("Change")


class MedicineForm(FlaskForm):
    medicine = StringField("Medicine", validators=[InputRequired(), Length(min=2, max=64)])
    potency = StringField("Potency", validators=[InputRequired(), Length(min=2, max=64)])
    short_name = StringField("Short Name", validators=[InputRequired(), Length(min=2, max=64)])
    save = SubmitField("Save")


class AdminSettingsForm(FlaskForm):
    id = HiddenField("user_id")
    username = StringField(
        "Mobile (Username)",
        validators=[
            UniqueUserOnUpdate(User, User.username, "id", "Username/Mobile already exists."),
            NumbersOnly(),
            InputRequired(),
            Length(min=4, max=16),
        ],
    )
    fullname = StringField("Full Name", validators=[InputRequired(), Length(min=4, max=64)])
    dob = DateField("Date of Birth", validators=[InputRequired()])
    sex = SelectField("Sex", choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
    blood = SelectField(
        "Blood Group",
        choices=[
            ("U", "Unknown"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
        ],
    )
    email = StringField(
        "Email", validators=[Email(), Optional(strip_whitespace=True), Length(max=64)], filters=[lambda x: x or None]
    )
    address = StringField("Address", validators=[Length(max=64)])
    save_admin_settings_form = SubmitField("Save")


class OrganizationForm(FlaskForm):
    id = HiddenField("user_id")
    name = StringField("Organization Name", validators=[InputRequired(), Length(min=2, max=128)])
    title = StringField(
        "Title line",
        validators=[Length(min=2, max=128), Optional(strip_whitespace=True)],
        filters=[lambda x: x or None],
    )
    description = StringField(
        "Description",
        validators=[Length(min=2, max=128), Optional(strip_whitespace=True)],
        filters=[lambda x: x or None],
    )
    address = StringField(
        "Address", validators=[Length(min=2, max=128), Optional(strip_whitespace=True)], filters=[lambda x: x or None]
    )
    logo = FileField("Logo", validators=[FileAllowed(["jpg", "png", "jpeg"], "Allowed JPG or PNG Images only.")])
    save_organization_form = SubmitField("Save")


class ParcelForm(FlaskForm):
    id = HiddenField("id")
    parcel_photo_1 = FileField(
        "Parcel photo", validators=[FileAllowed(["jpg", "png", "jpeg"], "Allowed JPG or PNG Images only.")]
    )
    parcel_date_1 = DateField(
        "Parcel date", validators=[Optional(strip_whitespace=True)], filters=[lambda x: x or None]
    )
    save_parcel_form = SubmitField("Save")


class PaymentInstructionBaseForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        paym_method = [("", "")] + [(p.payment_method, p.payment_method) for p in PaymentMethod.query.all()]
        paym_desc = [("", "")] + [
            (p.payment_description, p.payment_description) for p in PaymentDescription.query.all()
        ]
        self.payment_method.choices = paym_method
        self.payment_description.choices = paym_desc

    payment_description = SelectField("Payment Description", validators=[InputRequired()])
    payment_method = SelectField("Payment Method", validators=[InputRequired()])
    amount = DecimalField("Amount", validators=[InputRequired()])
    payment_status = SelectField("Payment Status", choices=[(0, "Unpaid"), (1, "Paid")])


class PaymentInstructionCreateForm(PaymentInstructionBaseForm):
    patient_id = SelectField("Patient", validators=[InputRequired()])
    save_created_payment_status = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        usr = [("", "")] + [
            (u.id, u.fullname + " - " + u.username)
            for u in User.query.filter((User.admin != 1) & User.active == 1).order_by(User.fullname).all()
        ]
        self.patient_id.choices = usr


class PaymentInstructionEditForm(PaymentInstructionBaseForm):
    visible_to_patient = BooleanField("Notify Patient")
    save_edited_payment_status = SubmitField("Save")


class PaymentMethodCreateForm(FlaskForm):
    payment_method = StringField(
        "Payment Method",
        validators=[
            Unique(PaymentMethod, PaymentMethod.payment_method, "Payment method already exists."),
            InputRequired(),
            Length(min=4, max=64),
        ],
    )
    save_payment_method = SubmitField("Add Payment Method")

class PaymentDescriptionCreateForm(FlaskForm):
    payment_description = StringField(
        "Payment Description",
        validators=[
            Unique(PaymentDescription, PaymentDescription.payment_description, "Payment description already exists."),
            InputRequired(),
            Length(min=4, max=64),
        ],
    )
    save_payment_description = SubmitField("Add Payment Description")