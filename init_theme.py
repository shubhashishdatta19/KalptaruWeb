from app import create_app, db
from app.models import SiteTheme

app = create_app()

def init_theme():
    with app.app_context():
        # Check if there's already a theme
        if not SiteTheme.query.first():
            default_theme = SiteTheme(
                name='Default Theme',
                is_active=True,
                primary_color='#007bff',
                secondary_color='#6c757d',
                accent_color='#28a745',
                font_family='system-ui, -apple-system, sans-serif',
                layout_type='full-width',
                navigation_style='standard'
            )
            db.session.add(default_theme)
            db.session.commit()
            print("Default theme created successfully!")
        else:
            print("Theme already exists in database.")
