from flask import request, redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from wtforms import SelectField
from werkzeug.utils import secure_filename
import os
import uuid

from . import db, admin
from .models import Event, Activity, Page, RegistrationForm, FormField, Photo, SiteTheme, Sponsor
from flask_admin import BaseView, expose
from .forms import EventForm, PageForm, PhotoForm, SiteThemeForm

def unique_endpoint():
    return str(uuid.uuid4())[:8]

class CustomPhotoView(ModelView):
    form = PhotoForm
    column_list = ('filename', 'caption', 'event', 'activity')

    def create_model(self, form):
        file_list = request.files.getlist(form.photo_file.name)
        created = False
        for file_data in file_list:
            if file_data and file_data.filename:
                filename = secure_filename(file_data.filename)
                file_path = os.path.join(self.admin.app.config['UPLOAD_FOLDER'], filename)
                file_data.save(file_path)
                model = self.model(
                    filename=filename,
                    caption=form.caption.data,
                    event=form.event.data,
                    activity=form.activity.data
                )
                self.session.add(model)
                created = True
        if created:
            self.session.commit()
            return True
        return False

    def on_model_change(self, form, model, is_created):
        if is_created:
            pass
        else:
            file_data = request.files.get(form.photo_file.name)
            if file_data:
                if model.filename:
                    old_file_path = os.path.join(self.admin.app.config['UPLOAD_FOLDER'], model.filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                filename = secure_filename(file_data.filename)
                file_path = os.path.join(self.admin.app.config['UPLOAD_FOLDER'], filename)
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
    form_overrides = dict(content='CKEditorField')
    edit_template = 'admin/page_edit.html'
    form = PageForm

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
    form_overrides = dict(field_type=SelectField)
    form_args = dict(
        field_type=dict(
            choices=[
                ('text', 'Text'),
                ('textarea', 'Textarea'),
                ('select', 'Select'),
                ('checkbox', 'Checkbox'),
                ('radio', 'Radio'),
                ('email', 'Email'),
                ('number', 'Number'),
                ('date', 'Date'),
            ]
        )
    )

class ThemeView(ModelView):
    form = SiteThemeForm
    column_list = ('name', 'is_active', 'primary_color', 'secondary_color', 'layout_type')
    
    form_widget_args = {
        'primary_color': {'type': 'color'},
        'secondary_color': {'type': 'color'},
        'accent_color': {'type': 'color'},
    }

    form_overrides = {
        'font_family': SelectField,
        'layout_type': SelectField,
        'navigation_style': SelectField
    }

    def on_model_change(self, form, model, is_created):
        if model.is_active:
            # Deactivate all other themes
            other_themes = self.session.query(SiteTheme).filter(SiteTheme.id != model.id)
            for theme in other_themes:
                theme.is_active = False
            self.session.commit()
        flash('Theme settings updated successfully!', 'success')

class SponsorView(ModelView):
    column_list = ('name', 'website_url', 'logo_filename', 'description')
    form_columns = ('name', 'website_url', 'logo_filename', 'description')

class CustomSponsorsPageView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/sponsors.html')

def register_admin_views():
    # Check if views are already registered to avoid duplicates
    registered_endpoints = [view.endpoint for view in admin._views]
    
    view_configs = [
        (CustomEventView, Event, 'Events', 'admin_events'),
        (CustomActivityView, Activity, 'Activities', 'admin_activities'),
        (CustomPageView, Page, 'Pages', 'admin_pages'),
        (CustomRegistrationFormView, RegistrationForm, 'Forms', 'admin_forms'),
        (CustomFormFieldView, FormField, 'Form Fields', 'admin_form_fields'),
        (CustomPhotoView, Photo, 'Photos', 'admin_photos'),
        (ThemeView, SiteTheme, 'Theme Settings', 'admin_theme'),
        (SponsorView, Sponsor, 'Sponsors', 'admin_sponsors')
    ]
    
    for view_class, model, name, endpoint in view_configs:
        if endpoint not in registered_endpoints:
            admin.add_view(view_class(model, db.session, name=name, endpoint=endpoint))
    
    # Add custom sponsors page view
    if 'custom_sponsors_page' not in registered_endpoints:
        admin.add_view(CustomSponsorsPageView(name='Custom Sponsors Page', endpoint='custom_sponsors_page', category='Admin'))
