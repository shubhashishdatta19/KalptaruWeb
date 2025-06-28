from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import re
from flask_migrate import Migrate

app = Flask(__name__)

# Forms
class PageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    order = StringField('Order', validators=[Optional()])
    parent_page = QuerySelectField('Parent Page', query_factory=lambda: Page.query.order_by(Page.title).all(), get_label='title', allow_blank=True, blank_text='-- No Parent --')
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    schedule = TextAreaField('Schedule', validators=[Optional()])
    organizing_body = StringField('Organizing Body', validators=[Optional(), Length(max=100)])
    registration_form = QuerySelectField('Registration Form', query_factory=lambda: RegistrationForm.query.all(), get_label='name', allow_blank=True, blank_text='-- No Form --')
    page = QuerySelectField('Linked Page', query_factory=lambda: Page.query.order_by(Page.title).all(), get_label='title', allow_blank=True, blank_text='-- No Page --')
    is_upcoming = BooleanField('Upcoming Event (Show on Home Page)')
    submit = SubmitField('Submit')

class PhotoForm(FlaskForm):
    photo_file = FileField('Image File', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    caption = StringField('Caption', validators=[Optional(), Length(max=200)])
    event = QuerySelectField('Event', query_factory=lambda: Event.query.all(), get_label='title', allow_blank=True, blank_text='-- Select Event --')
    activity = QuerySelectField('Activity', query_factory=lambda: Activity.query.all(), get_label='title', allow_blank=True, blank_text='-- Select Activity --')
    submit = SubmitField('Submit')

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

app.config['SECRET_KEY'] = 'your_secret_key' # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Using SQLite for simplicity, can be changed to PostgreSQL/MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name='Kalpataru Admin', template_mode='bootstrap3')

# Models
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
    field_type = db.Column(db.String(50), nullable=False) # e.g., text, textarea, select, checkbox, radio
    options = db.Column(db.Text, nullable=True) # Comma-separated for select/radio
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

# Admin Views
class CustomPhotoView(ModelView):
    form = PhotoForm
    column_list = ('filename', 'caption', 'event', 'activity')

    def create_model(self, form):
        file_data = request.files.get(form.photo_file.name)
        if file_data:
            filename = secure_filename(file_data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_data.save(file_path)
            
            model = self.model(filename=filename,
                               caption=form.caption.data,
                               event=form.event.data,
                               activity=form.activity.data)
            self.session.add(model)
            self.session.commit()
            return True
        return False

    def on_model_change(self, form, model, is_created):
        if is_created:
            # For create, the file is handled in create_model
            pass
        else:
            # For edit, handle file upload if a new file is provided
            file_data = request.files.get(form.photo_file.name)
            if file_data:
                # Delete old file if it exists
                if model.filename:
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], model.filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                filename = secure_filename(file_data.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_data.save(file_path)
                model.filename = filename
            
            model.caption = form.caption.data
            model.event = form.event.data
            model.activity = form.activity.data

class CustomEventView(ModelView):
    form = EventForm
    column_list = ('title', 'schedule', 'organizing_body', 'registration_form', 'page', 'is_upcoming')
    form_columns = ('title', 'description', 'schedule', 'organizing_body', 'registration_form', 'page', 'is_upcoming')

    def on_model_change(self, form, model, is_created):
        if form.registration_form.data:
            model.registration_form_id = form.registration_form.data.id
        else:
            model.registration_form_id = None
        
        if form.page.data:
            model.page_id = form.page.data.id
        else:
            model.page_id = None
        
        model.is_upcoming = form.is_upcoming.data

class CustomActivityView(ModelView):
    column_list = ('title', 'description')
    form_columns = ('title', 'description', 'photos')

class CustomPageView(ModelView):
    column_list = ('title', 'slug', 'order', 'parent')
    form_columns = ('title', 'slug', 'content', 'order', 'parent_page')
    form = PageForm # Use the custom form

    def on_model_change(self, form, model, is_created):
        if form.parent_page.data:
            model.parent_id = form.parent_page.data.id
        else:
            model.parent_id = None

class CustomRegistrationFormView(ModelView):
    column_list = ('name', 'description')
    form_columns = ('name', 'description', 'fields')

class CustomFormFieldView(ModelView):
    column_list = ('form', 'field_name', 'field_type', 'required')
    form_columns = ('form', 'field_name', 'field_type', 'options', 'required')

admin.add_view(CustomEventView(Event, db.session))
admin.add_view(CustomActivityView(Activity, db.session))
admin.add_view(CustomPageView(Page, db.session))
admin.add_view(CustomRegistrationFormView(RegistrationForm, db.session))
admin.add_view(CustomFormFieldView(FormField, db.session))
admin.add_view(CustomPhotoView(Photo, db.session))

# Routes
@app.route('/')
def home():
    events = Event.query.order_by(Event.id.desc()).limit(5).all() # Latest 5 events
    upcoming_events = Event.query.filter_by(is_upcoming=True).order_by(Event.id.desc()).all() # Upcoming events
    activities = Activity.query.order_by(Activity.id.desc()).limit(5).all() # Latest 5 activities
    
    # Build page tree
    pages = Page.query.order_by(Page.order, Page.title).all()
    page_tree = build_page_tree(pages)

    return render_template('home.html', events=events, upcoming_events=upcoming_events, activities=activities, page_tree=page_tree)

def build_page_tree(pages):
    page_dict = {page.id: {'page': page, 'children': []} for page in pages}
    tree = []
    for page in pages:
        if page.parent_id is None:
            tree.append(page_dict[page.id])
        else:
            if page.parent_id in page_dict:
                page_dict[page.parent_id]['children'].append(page_dict[page.id])
    return tree

@app.route('/page/<slug>')
def static_page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    
    # Fetch events linked to this page
    linked_events = Event.query.filter_by(page_id=page.id).all()

    # Process content for embedded activities and events
    processed_content = page.content
    
    # Regex to find [activity:ID]
    activity_matches = re.findall(r'\[activity:(\d+)\]', processed_content)
    for activity_id in activity_matches:
        activity = Activity.query.get(activity_id)
        if activity:
            # Render activity details (you might want a more elaborate template for this)
            activity_html = render_template('_activity_embed.html', activity=activity)
            processed_content = processed_content.replace(f'[activity:{activity_id}]', activity_html)
        else:
            processed_content = processed_content.replace(f'[activity:{activity_id}]', f'<p>Activity with ID {activity_id} not found.</p>')

    # Regex to find [event:ID]
    event_matches = re.findall(r'\[event:(\d+)\]', processed_content)
    for event_id in event_matches:
        event = Event.query.get(event_id)
        if event:
            # Render event details (you might want a more elaborate template for this)
            event_html = render_template('_event_embed.html', event=event)
            processed_content = processed_content.replace(f'[event:{event_id}]', event_html)
        else:
            processed_content = processed_content.replace(f'[event:{event_id}]', f'<p>Event with ID {event_id} not found.</p>')

    return render_template('static_page.html', page=page, processed_content=processed_content, linked_events=linked_events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@app.route('/activity/<int:activity_id>')
def activity_detail(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return render_template('activity_detail.html', activity=activity)

@app.route('/register/<int:form_id>', methods=['GET', 'POST'])
def register_form(form_id):
    registration_form = RegistrationForm.query.get_or_404(form_id)
    
    class DynamicForm(FlaskForm):
        pass

    for field_def in registration_form.fields:
        field_class = None
        validators = []
        if field_def.required:
            validators.append(DataRequired())

        if field_def.field_type == 'text':
            field_class = StringField
        elif field_def.field_type == 'textarea':
            field_class = TextAreaField
        elif field_def.field_type == 'select':
            choices = [(opt.strip(), opt.strip()) for opt in field_def.options.split(',')] if field_def.options else []
            field_class = SelectField
            setattr(DynamicForm, field_def.field_name, field_class(
                field_def.field_name.replace('_', ' ').title(),
                choices=choices,
                validators=validators,
                flags={} # Explicitly set flags to an empty dictionary to prevent AttributeError
            ))
            continue # Skip default setattr below
        elif field_def.field_type == 'checkbox':
            field_class = BooleanField
        # Add more field types as needed (e.g., radio, email, number)

        if field_class:
            setattr(DynamicForm, field_def.field_name, field_class(field_def.field_name.replace('_', ' ').title(), validators=validators))
    
    setattr(DynamicForm, 'submit', SubmitField('Submit'))

    form = DynamicForm()

    if form.validate_on_submit():
        # Here you would process the form data and save it.
        # For demonstration, we'll just print it.
        print("Form Data Submitted:")
        for field_name, field_value in form.data.items():
            if field_name != 'csrf_token' and field_name != 'submit':
                print(f"{field_name}: {field_value}")
        flash('Registration successful!', 'success')
        return redirect(url_for('home')) # Redirect to home or a success page
    
    return render_template('registration_form.html', form=form, registration_form=registration_form)

if __name__ == '__main__':
    app.run(debug=True)
