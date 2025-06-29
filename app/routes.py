from flask import render_template, redirect, url_for, request, flash, current_app
from flask import Blueprint
from datetime import datetime
import re

from . import db
from .models import Event, Activity, Page, RegistrationForm, FormField
from .forms import PageForm, EventForm, PhotoForm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

main = Blueprint('main', __name__)

@main.app_context_processor
def inject_template_vars():
    from .models import SiteTheme, Event
    return {
        'current_year': datetime.now().year,
        'theme': SiteTheme.get_active_theme,
        'upcoming_events': Event.query.filter_by(is_upcoming=True).order_by(Event.id.desc()).all()
    }

@main.route('/')
def home():
    events = Event.query.order_by(Event.id.desc()).limit(5).all()
    activities = Activity.query.order_by(Activity.id.desc()).limit(5).all()
    pages = Page.query.order_by(Page.order, Page.title).all()
    page_tree = build_page_tree(pages)
    return render_template('home.html', events=events, activities=activities, page_tree=page_tree)

def serialize_page(page):
    return {
        'title': page.title,
        'slug': page.slug,
        'id': page.id
    }

def build_page_tree(pages):
    page_dict = {page.id: {'page': serialize_page(page), 'children': []} for page in pages}
    tree = []
    for page in pages:
        if page.parent_id is None:
            tree.append(page_dict[page.id])
        else:
            if page.parent_id in page_dict:
                page_dict[page.parent_id]['children'].append(page_dict[page.id])
    return tree

@main.route('/page/<slug>')
def static_page(slug):
    pages = Page.query.order_by(Page.order, Page.title).all()
    page_tree = build_page_tree(pages)
    page = Page.query.filter_by(slug=slug).first_or_404()
    linked_events = Event.query.filter_by(page_id=page.id).all()
    processed_content = page.content

    activity_matches = re.findall(r'\[activity:(\d+)\]', processed_content)
    for activity_id in activity_matches:
        activity = Activity.query.get(activity_id)
        if activity:
            activity_html = render_template('_activity_embed.html', activity=activity)
            processed_content = processed_content.replace(f'[activity:{activity_id}]', activity_html)
        else:
            processed_content = processed_content.replace(f'[activity:{activity_id}]', f'<p>Activity with ID {activity_id} not found.</p>')

    event_matches = re.findall(r'\[event:(\d+)\]', processed_content)
    for event_id in event_matches:
        event = Event.query.get(event_id)
        if event:
            event_html = render_template('_event_embed.html', event=event)
            processed_content = processed_content.replace(f'[event:{event_id}]', event_html)
        else:
            processed_content = processed_content.replace(f'[event:{event_id}]', f'<p>Event with ID {event_id} not found.</p>')

    return render_template('static_page.html', page=page, processed_content=processed_content, linked_events=linked_events, page_tree=page_tree)

@main.route('/event/<int:event_id>')
def event_detail(event_id):
    pages = Page.query.order_by(Page.order, Page.title).all()
    page_tree = build_page_tree(pages)
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event, page_tree=page_tree)

@main.route('/activity/<int:activity_id>')
def activity_detail(activity_id):
    pages = Page.query.order_by(Page.order, Page.title).all()
    page_tree = build_page_tree(pages)
    activity = Activity.query.get_or_404(activity_id)
    return render_template('activity_detail.html', activity=activity, page_tree=page_tree)

@main.route('/register/<int:form_id>', methods=['GET', 'POST'])
def register_form(form_id):
    pages = Page.query.order_by(Page.order, Page.title).all()
    page_tree = build_page_tree(pages)
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
                flags={}
            ))
            continue
        elif field_def.field_type == 'checkbox':
            field_class = BooleanField

        if field_class:
            setattr(DynamicForm, field_def.field_name, field_class(field_def.field_name.replace('_', ' ').title(), validators=validators))

    setattr(DynamicForm, 'submit', SubmitField('Submit'))

    form = DynamicForm()

    if form.validate_on_submit():
        print("Form Data Submitted:")
        for field_name, field_value in form.data.items():
            if field_name != 'csrf_token' and field_name != 'submit':
                print(f"{field_name}: {field_value}")
        flash('Registration successful!', 'success')
        return redirect(url_for('main.home'))

    return render_template('registration_form.html', form=form, registration_form=registration_form, page_tree=page_tree)
