# Kalpataru Web Application

This is a Flask-based web application designed to manage events, activities, pages, registration forms, photos, site themes, and sponsors. It features an administrative interface for content management and a user-facing site to display information.

## Admin Functionality

The application provides a comprehensive Flask-Admin interface for managing various aspects of the site. The admin panel can typically be accessed at `/admin` (e.g., `http://localhost:5000/admin` when running locally).

Key administrative sections include:

*   **Events**: Manage event details, schedules, organizing bodies, link to registration forms, associate with static pages, and mark as upcoming.
*   **Activities**: Manage activity details and associate photos.
*   **Pages**: Create and manage static pages with rich content using CKEditor. Pages can be organized hierarchically with parent-child relationships. Special slugs like `/contact` and `/about` are handled as dedicated pages. Dynamic content embedding for activities and events using `[activity:ID]` and `[event:ID]` shortcodes is supported.
*   **Forms**: Define custom registration forms with various field types (text, textarea, select, checkbox, radio, email, number, date).
*   **Form Fields**: Manage individual fields for registration forms, including their type, options (for select/radio), and whether they are required.
*   **Photos**: Upload and manage photos, associating them with events or activities. Supports multiple photo uploads for a single entry.
*   **Theme Settings**: Customize the site's appearance, including primary, secondary, and accent colors, font family, layout type (full-width/boxed), and navigation style (standard/centered). Only one theme can be active at a time.
*   **Sponsors**: Manage sponsor information, including name, website URL, logo, and description.

## User Pages

The user-facing part of the application provides the following key functionalities:

*   **Home Page (`/`)**: Displays a list of recent events and activities. It also features a dynamic navigation menu built from the hierarchical page structure.
*   **Static Pages (`/page/<slug>`)**: Renders custom content pages. Special pages like `/contact` and `/about` have dedicated templates. These pages can embed event and activity details using shortcodes like `[event:ID]` and `[activity:ID]`.
*   **Event Detail Page (`/event/<int:event_id>`)**: Displays detailed information about a specific event.
*   **Activity Detail Page (`/activity/<int:activity_id>`)**: Displays detailed information about a specific activity, including associated photos.
*   **Registration Form Page (`/register/<int:form_id>`)**: Dynamically generates and handles submission for custom registration forms.

## Deployment and Run Steps

### Local Development Setup

1.  **Clone the repository**:
    ```bash
    git clone [repository_url]
    cd KalptaruWeb
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Initialize the database and migrations**:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```
    *Note: If you encounter issues with `flask db`, ensure your `FLASK_APP` environment variable is set correctly. For this project, `run.py` is the entry point.*

6.  **Initialize default theme**:
    The `init_theme.py` script ensures a default theme is present in the database. This is called automatically when `run.py` is executed.

7.  **Run the application**:
    ```bash
    python run.py
    ```
    The application will typically run on `http://localhost:5000`.

### Deployment

The application is configured for deployment using **Vercel** and includes a **GitHub Actions** workflow for continuous integration and deployment.

#### Vercel Deployment

The `vercel.json` file configures the deployment for Vercel. It specifies that `api/index.py` is the entry point for the serverless function.

To deploy to Vercel:
1.  Install the Vercel CLI: `npm install -g vercel`
2.  Navigate to the project root: `cd KalptaruWeb`
3.  Run `vercel` and follow the prompts.

#### GitHub Actions (CI/CD)

The `.github/workflows/python-app.yml` file defines a GitHub Actions workflow. This workflow is currently configured for building a Jekyll site and deploying to GitHub Pages. **This workflow needs to be updated to reflect the Python Flask application's build and deployment process (e.g., to Vercel or another Python-compatible hosting service).**

**Current Workflow (Jekyll-specific - requires modification for Flask app):**
```yaml
name: Build and Deploy Jekyll Site

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Jekyll site with Docker
        run: |
          docker run --rm \
            -v ${{ github.workspace }}:/srv/jekyll \
            -v ${{ github.workspace }}/_site:/srv/jekyll/_site \
            jekyll/jekyll:latest jekyll build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
```

**Note on GitHub Actions**: The existing workflow is for a Jekyll site. For a Flask application, you would typically:
1.  Set up Python.
2.  Install dependencies from `requirements.txt`.
3.  Run tests (if any).
4.  Trigger a deployment to Vercel using the Vercel CLI or a similar service.
