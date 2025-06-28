from . import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    schedule = db.Column(db.Text, nullable=True)
    organizing_body = db.Column(db.String(100), nullable=True)
    registration_form_id = db.Column(db.Integer, db.ForeignKey('registration_form.id'), nullable=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)
    is_upcoming = db.Column(db.Boolean, default=False)
    photos = db.relationship('Photo', backref='event', lazy=True)
    page = db.relationship('Page', backref='events', lazy=True)

    def __repr__(self):
        return f"Event('{self.title}')"

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photos = db.relationship('Photo', backref='activity', lazy=True)

    def __repr__(self):
        return f"Activity('{self.title}')"

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=True)
    children = db.relationship('Page', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return f"Page('{self.title}')"

class RegistrationForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    fields = db.relationship('FormField', backref='form', lazy=True)
    events = db.relationship('Event', backref='registration_form', lazy=True)

    def __repr__(self):
        return f"RegistrationForm('{self.name}')"

class FormField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('registration_form.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)
    options = db.Column(db.Text, nullable=True)
    required = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"FormField('{self.field_name}', type='{self.field_type}')"

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    caption = db.Column(db.String(200), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=True)

    def __repr__(self):
        return f"Photo('{self.filename}')"
