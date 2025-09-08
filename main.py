import os
from nicegui import ui

# --- Your NiceGUI app logic goes here ---
ui.label('Hello, Cloud Run!')
ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))
# ----------------------------------------

# Get the port from the environment variable, defaulting to 8080.
# Cloud Run will set the PORT variable for you.
port = int(os.environ.get('PORT', 8080))

# Start the app.
# host='0.0.0.0' is crucial to make the app accessible from outside the container.
ui.run(
    host='0.0.0.0',
    port=port
)