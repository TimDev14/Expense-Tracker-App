"""Local development entry point."""

from app import create_app

app = create_app()

# TODO(Milestone 6): replace Flask's debug server with a production WSGI server
# and production configuration when deploying.

if __name__ == "__main__":
    app.run(debug=True)
