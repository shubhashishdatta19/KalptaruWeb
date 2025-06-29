from init_theme import init_theme

if __name__ == '__main__':
    init_theme()  # Initialize default theme if not exists
    from app import create_app
    app = create_app()
    app.run(debug=True)
