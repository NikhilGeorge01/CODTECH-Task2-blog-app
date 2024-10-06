from blogs  import app, db  # Import your app and db from your application package (replace with your actual package/module name)

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
