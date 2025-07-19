@echo off
title MIT App Inventor AIA Generator Server (Simplified Version)
color 0A

echo.
echo ========================================
echo  MIT App Inventor AIA Generator Server
echo  Simplified Version
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found: 
python --version

:: Check if Flask is installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Flask not found. Installing dependencies...
    echo.
    pip install flask requests
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo [INFO] Flask already installed
)

:: Check if requests is installed
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing requests library...
    pip install requests
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install requests
        pause
        exit /b 1
    )
)

echo.
echo [INFO] All dependencies installed successfully!
echo [INFO] Creating simplified app.py file...

:: Create a simplified version of the app
echo from flask import Flask, render_template, request, jsonify, send_file > app_simplified.py
echo import json >> app_simplified.py
echo import zipfile >> app_simplified.py
echo import io >> app_simplified.py
echo import os >> app_simplified.py
echo import uuid >> app_simplified.py
echo from datetime import datetime >> app_simplified.py
echo. >> app_simplified.py
echo app = Flask(__name__) >> app_simplified.py
echo. >> app_simplified.py

:: Add the HTML template (simplified)
echo # HTML template for the web interface >> app_simplified.py
echo HTML_TEMPLATE = '''<!DOCTYPE html> >> app_simplified.py
echo <html lang="en"> >> app_simplified.py
echo <head> >> app_simplified.py
echo     <meta charset="UTF-8"> >> app_simplified.py
echo     <meta name="viewport" content="width=device-width, initial-scale=1.0"> >> app_simplified.py
echo     <title>MIT App Inventor AIA Generator</title> >> app_simplified.py
echo     <style> >> app_simplified.py
echo         body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; } >> app_simplified.py
echo         .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); } >> app_simplified.py
echo         h1 { text-align: center; } >> app_simplified.py
echo         .form-group { margin-bottom: 15px; } >> app_simplified.py
echo         label { display: block; margin-bottom: 5px; font-weight: bold; } >> app_simplified.py
echo         input, textarea, select { width: 100%%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; } >> app_simplified.py
echo         .btn { background: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; } >> app_simplified.py
echo         .loading { display: none; text-align: center; margin: 20px 0; } >> app_simplified.py
echo         .result { display: none; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px; } >> app_simplified.py
echo     </style> >> app_simplified.py
echo </head> >> app_simplified.py
echo <body> >> app_simplified.py
echo     <div class="container"> >> app_simplified.py
echo         <h1>MIT App Inventor AIA Generator</h1> >> app_simplified.py
echo         <form id="aiaForm"> >> app_simplified.py
echo             <div class="form-group"> >> app_simplified.py
echo                 <label for="appName">App Name:</label> >> app_simplified.py
echo                 <input type="text" id="appName" name="appName" required placeholder="My App"> >> app_simplified.py
echo             </div> >> app_simplified.py
echo             <div class="form-group"> >> app_simplified.py
echo                 <label for="appType">App Type:</label> >> app_simplified.py
echo                 <select id="appType" name="appType"> >> app_simplified.py
echo                     <option value="basic">Basic App</option> >> app_simplified.py
echo                     <option value="game">Game</option> >> app_simplified.py
echo                     <option value="utility">Utility</option> >> app_simplified.py
echo                 </select> >> app_simplified.py
echo             </div> >> app_simplified.py
echo             <div class="form-group"> >> app_simplified.py
echo                 <label for="prompt">Describe your app:</label> >> app_simplified.py
echo                 <textarea id="prompt" name="prompt" required placeholder="Create a simple app with 2 buttons"></textarea> >> app_simplified.py
echo             </div> >> app_simplified.py
echo             <button type="submit" class="btn">Generate AIA File</button> >> app_simplified.py
echo         </form> >> app_simplified.py
echo         <div class="loading" id="loading">Generating your AIA file...</div> >> app_simplified.py
echo         <div class="result" id="result"> >> app_simplified.py
echo             <h3>Success!</h3> >> app_simplified.py
echo             <p>Your AIA file has been generated successfully.</p> >> app_simplified.py
echo             <a href="#" id="downloadLink">Download AIA File</a> >> app_simplified.py
echo         </div> >> app_simplified.py
echo     </div> >> app_simplified.py
echo     <script> >> app_simplified.py
echo         document.getElementById('aiaForm').addEventListener('submit', async function(e) { >> app_simplified.py
echo             e.preventDefault(); >> app_simplified.py
echo             const formData = new FormData(e.target); >> app_simplified.py
echo             const data = Object.fromEntries(formData); >> app_simplified.py
echo             document.getElementById('loading').style.display = 'block'; >> app_simplified.py
echo             try { >> app_simplified.py
echo                 const response = await fetch('/generate', { >> app_simplified.py
echo                     method: 'POST', >> app_simplified.py
echo                     headers: { 'Content-Type': 'application/json' }, >> app_simplified.py
echo                     body: JSON.stringify(data) >> app_simplified.py
echo                 }); >> app_simplified.py
echo                 if (response.ok) { >> app_simplified.py
echo                     const blob = await response.blob(); >> app_simplified.py
echo                     const url = window.URL.createObjectURL(blob); >> app_simplified.py
echo                     const filename = `${data.appName.replace(/[^a-z0-9]/gi, '_')}.aia`; >> app_simplified.py
echo                     document.getElementById('downloadLink').href = url; >> app_simplified.py
echo                     document.getElementById('downloadLink').download = filename; >> app_simplified.py
echo                     document.getElementById('result').style.display = 'block'; >> app_simplified.py
echo                 } else { >> app_simplified.py
echo                     alert('Error generating AIA file. Please try again.'); >> app_simplified.py
echo                 } >> app_simplified.py
echo             } catch (error) { >> app_simplified.py
echo                 alert('Network error. Please check your connection and try again.'); >> app_simplified.py
echo             } >> app_simplified.py
echo             document.getElementById('loading').style.display = 'none'; >> app_simplified.py
echo         }); >> app_simplified.py
echo     </script> >> app_simplified.py
echo </body> >> app_simplified.py
echo </html>''' >> app_simplified.py
echo. >> app_simplified.py

:: Add the rest of the code
echo def create_basic_project_structure(app_name, app_type, prompt): >> app_simplified.py
echo     """Create basic MIT App Inventor project structure based on prompt""" >> app_simplified.py
echo     # Base project properties >> app_simplified.py
echo     project_properties = { >> app_simplified.py
echo         "name": app_name, >> app_simplified.py
echo         "assets": [], >> app_simplified.py
echo         "settings": { >> app_simplified.py
echo             "icon": "", >> app_simplified.py
echo             "versioncode": "1", >> app_simplified.py
echo             "versionname": "1.0", >> app_simplified.py
echo             "useslocation": "false", >> app_simplified.py
echo             "aname": app_name, >> app_simplified.py
echo             "sizing": "Responsive", >> app_simplified.py
echo             "showlistsasjson": "true", >> app_simplified.py
echo             "actionbar": "false", >> app_simplified.py
echo             "theme": "AppTheme.Light.DarkActionBar", >> app_simplified.py
echo             "color_primary": "#3F51B5", >> app_simplified.py
echo             "color_primary_dark": "#303F9F", >> app_simplified.py
echo             "color_accent": "#FF4081" >> app_simplified.py
echo         }, >> app_simplified.py
echo         "authURL": [], >> app_simplified.py
echo         "YaVersion": "208", >> app_simplified.py
echo         "Source": "Form", >> app_simplified.py
echo         "Properties": { >> app_simplified.py
echo             "$Name": "Screen1", >> app_simplified.py
echo             "$Type": "Form", >> app_simplified.py
echo             "$Version": "31", >> app_simplified.py
echo             "AppName": app_name, >> app_simplified.py
echo             "Title": app_name, >> app_simplified.py
echo             "Uuid": str(uuid.uuid4()) >> app_simplified.py
echo         } >> app_simplified.py
echo     } >> app_simplified.py
echo. >> app_simplified.py
echo     # Generate components based on app type and prompt >> app_simplified.py
echo     components = [] >> app_simplified.py
echo     prompt_lower = prompt.lower() >> app_simplified.py
echo. >> app_simplified.py
echo     # Check for buttons in the prompt >> app_simplified.py
echo     if 'button' in prompt_lower: >> app_simplified.py
echo         # Try to find a number before "button" >> app_simplified.py
echo         import re >> app_simplified.py
echo         button_match = re.search(r'(\d+)\s*buttons?', prompt_lower) >> app_simplified.py
echo         button_count = int(button_match.group(1)) if button_match else 1 >> app_simplified.py
echo. >> app_simplified.py
echo         # Create the specified number of buttons >> app_simplified.py
echo         for i in range(1, button_count+1): >> app_simplified.py
echo             components.append({ >> app_simplified.py
echo                 "$Name": f"Button{i}", >> app_simplified.py
echo                 "$Type": "Button", >> app_simplified.py
echo                 "$Version": "7", >> app_simplified.py
echo                 "Text": f"Button {i}", >> app_simplified.py
echo                 "Uuid": str(uuid.uuid4()) >> app_simplified.py
echo             }) >> app_simplified.py
echo     else: >> app_simplified.py
echo         # Default button >> app_simplified.py
echo         components.append({ >> app_simplified.py
echo             "$Name": "Button1", >> app_simplified.py
echo             "$Type": "Button", >> app_simplified.py
echo             "$Version": "7", >> app_simplified.py
echo             "Text": "Click Me", >> app_simplified.py
echo             "Uuid": str(uuid.uuid4()) >> app_simplified.py
echo         }) >> app_simplified.py
echo. >> app_simplified.py
echo     # Add components to project >> app_simplified.py
echo     if components: >> app_simplified.py
echo         project_properties["Properties"]["$Components"] = components >> app_simplified.py
echo. >> app_simplified.py
echo     return project_properties >> app_simplified.py
echo. >> app_simplified.py

echo def create_blocks_file(app_name, components): >> app_simplified.py
echo     """Create basic blocks file with simple event handlers""" >> app_simplified.py
echo     blocks_data = { >> app_simplified.py
echo         "YaVersion": "208", >> app_simplified.py
echo         "Source": "Form", >> app_simplified.py
echo         "Properties": { >> app_simplified.py
echo             "$Name": "Screen1", >> app_simplified.py
echo             "$Type": "Form", >> app_simplified.py
echo             "$Version": "31", >> app_simplified.py
echo             "Uuid": str(uuid.uuid4()), >> app_simplified.py
echo             "$Components": [] >> app_simplified.py
echo         } >> app_simplified.py
echo     } >> app_simplified.py
echo. >> app_simplified.py
echo     # Add basic event blocks for buttons >> app_simplified.py
echo     event_blocks = [] >> app_simplified.py
echo     for component in components: >> app_simplified.py
echo         if component.get("$Type") == "Button": >> app_simplified.py
echo             event_blocks.append({ >> app_simplified.py
echo                 "type": "component_event", >> app_simplified.py
echo                 "id": str(uuid.uuid4()), >> app_simplified.py
echo                 "component": component["$Name"], >> app_simplified.py
echo                 "event": "Click" >> app_simplified.py
echo             }) >> app_simplified.py
echo. >> app_simplified.py
echo     if event_blocks: >> app_simplified.py
echo         blocks_data["blocks"] = event_blocks >> app_simplified.py
echo. >> app_simplified.py
echo     return blocks_data >> app_simplified.py
echo. >> app_simplified.py

echo @app.route('/') >> app_simplified.py
echo def index(): >> app_simplified.py
echo     return HTML_TEMPLATE >> app_simplified.py
echo. >> app_simplified.py

echo @app.route('/generate', methods=['POST']) >> app_simplified.py
echo def generate_aia(): >> app_simplified.py
echo     try: >> app_simplified.py
echo         data = request.json >> app_simplified.py
echo         app_name = data.get('appName', 'MyApp') >> app_simplified.py
echo         app_type = data.get('appType', 'basic') >> app_simplified.py
echo         prompt = data.get('prompt', '') >> app_simplified.py
echo. >> app_simplified.py
echo         # Create project structure >> app_simplified.py
echo         project_data = create_basic_project_structure(app_name, app_type, prompt) >> app_simplified.py
echo         components = project_data["Properties"].get("$Components", []) >> app_simplified.py
echo. >> app_simplified.py
echo         # Create blocks data >> app_simplified.py
echo         blocks_data = create_blocks_file(app_name, components) >> app_simplified.py
echo. >> app_simplified.py
echo         # Create AIA file in memory >> app_simplified.py
echo         aia_buffer = io.BytesIO() >> app_simplified.py
echo. >> app_simplified.py
echo         with zipfile.ZipFile(aia_buffer, 'w', zipfile.ZIP_DEFLATED) as aia_file: >> app_simplified.py
echo             # Add project.properties >> app_simplified.py
echo             project_json = json.dumps(project_data, indent=2) >> app_simplified.py
echo             aia_file.writestr('youngandroidproject/project.properties', f""" >> app_simplified.py
echo main=appinventor.ai_user.{app_name}.Screen1 >> app_simplified.py
echo name={app_name} >> app_simplified.py
echo assets=../assets >> app_simplified.py
echo source=../src >> app_simplified.py
echo build=../build >> app_simplified.py
echo versioncode=1 >> app_simplified.py
echo versionname=1.0 >> app_simplified.py
echo useslocation=false >> app_simplified.py
echo aname={app_name} >> app_simplified.py
echo             """.strip()) >> app_simplified.py
echo. >> app_simplified.py
echo             # Add Screen1.scm (scheme file) >> app_simplified.py
echo             screen_scm = "#|\\n$JSON\\n" + project_json + "\\n|#" >> app_simplified.py
echo             aia_file.writestr(f'src/appinventor/ai_user/{app_name}/Screen1.scm', screen_scm) >> app_simplified.py
echo. >> app_simplified.py
echo             # Add Screen1.bky (blocks file) >> app_simplified.py
echo             blocks_json = json.dumps(blocks_data, indent=2) >> app_simplified.py
echo             blocks_content = "#|\\n$JSON\\n" + blocks_json + "\\n|#" >> app_simplified.py
echo             aia_file.writestr(f'src/appinventor/ai_user/{app_name}/Screen1.bky', blocks_content) >> app_simplified.py
echo. >> app_simplified.py
echo             # Add required empty directories >> app_simplified.py
echo             for dir_path in ['assets', 'src', 'build']: >> app_simplified.py
echo                 aia_file.writestr(f'{dir_path}/.gitkeep', '') >> app_simplified.py
echo. >> app_simplified.py
echo             # Add proper directory structure >> app_simplified.py
echo             aia_file.writestr(f'src/appinventor/ai_user/{app_name}/.gitkeep', '') >> app_simplified.py
echo. >> app_simplified.py
echo             # Add a simple asset file to ensure assets are properly recognized >> app_simplified.py
echo             aia_file.writestr('assets/README.txt', f'Assets for {app_name}') >> app_simplified.py
echo. >> app_simplified.py
echo         aia_buffer.seek(0) >> app_simplified.py
echo. >> app_simplified.py
echo         # Save a copy locally for debugging >> app_simplified.py
echo         with open(f'{app_name.replace(" ", "_")}.aia', 'wb') as f: >> app_simplified.py
echo             f.write(aia_buffer.getvalue()) >> app_simplified.py
echo. >> app_simplified.py
echo         # Reset buffer position >> app_simplified.py
echo         aia_buffer.seek(0) >> app_simplified.py
echo. >> app_simplified.py
echo         return send_file( >> app_simplified.py
echo             aia_buffer, >> app_simplified.py
echo             as_attachment=True, >> app_simplified.py
echo             download_name=f'{app_name.replace(" ", "_")}.aia', >> app_simplified.py
echo             mimetype='application/zip' >> app_simplified.py
echo         ) >> app_simplified.py
echo. >> app_simplified.py
echo     except Exception as e: >> app_simplified.py
echo         return jsonify({'error': str(e)}), 500 >> app_simplified.py
echo. >> app_simplified.py

echo if __name__ == '__main__': >> app_simplified.py
echo     print("🚀 Starting MIT App Inventor AIA Generator Server (Simplified Version)...") >> app_simplified.py
echo     print("📱 Server running at: http://127.0.0.1:5000") >> app_simplified.py
echo     print("💡 Navigate to the URL above to start creating AIA files!") >> app_simplified.py
echo     app.run(host='127.0.0.1', port=5000, debug=True) >> app_simplified.py

echo.
echo [INFO] Starting server...
echo.
echo ========================================
echo  Server will start on: http://127.0.0.1:5000
echo  Press Ctrl+C to stop the server
echo ========================================
echo.

:: Start the Flask application
python app_simplified.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server failed to start
    echo Check if port 5000 is already in use
    echo.
)

echo.
echo Server stopped.
pause