from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import FileInput
from flask_ckeditor import CKEditorField
from wtforms.widgets import ColorInput

from .models import Page, RegistrationForm, Event, Activity, SiteTheme

class PageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=100)])
    content = CKEditorField('Content', validators=[DataRequired()])
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

class MultiFileInput(FileInput):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('multiple', True)
        return super().__call__(field, **kwargs)

class PhotoForm(FlaskForm):
    photo_file = FileField('Image File', widget=MultiFileInput(), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    caption = StringField('Caption', validators=[Optional(), Length(max=200)])
    event = QuerySelectField('Event', query_factory=lambda: Event.query.all(), get_label='title', allow_blank=True, blank_text='-- Select Event --')
    activity = QuerySelectField('Activity', query_factory=lambda: Activity.query.all(), get_label='title', allow_blank=True, blank_text='-- Select Activity --')
    submit = SubmitField('Submit')

class SiteThemeForm(FlaskForm):
    name = StringField('Theme Name', validators=[DataRequired(), Length(max=100)])
    is_active = BooleanField('Activate Theme')
    primary_color = StringField('Primary Color', widget=ColorInput())
    secondary_color = StringField('Secondary Color', widget=ColorInput())
    accent_color = StringField('Accent Color', widget=ColorInput())
    font_family = SelectField('Font Family', choices=[
        ('system-ui, -apple-system, sans-serif', 'System Default'),
        ('Arial, sans-serif', 'Arial'),
        ('Helvetica, sans-serif', 'Helvetica'),
        ('Georgia, serif', 'Georgia'),
        ('Verdana, sans-serif', 'Verdana'),
        ('Roboto, sans-serif', 'Roboto')
    ])
    layout_type = SelectField('Layout Type', choices=[
        ('full-width', 'Full Width'),
        ('boxed', 'Boxed')
    ])
    navigation_style = SelectField('Navigation Style', choices=[
        ('standard', 'Standard'),
        ('centered', 'Centered')
    ])
    custom_css = TextAreaField('Custom CSS', validators=[Optional()])
    submit = SubmitField('Save Theme')
