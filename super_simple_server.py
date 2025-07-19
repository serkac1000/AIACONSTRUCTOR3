from flask import Flask, request, send_file
import json
import zipfile
import io
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AIA Generator</title>
        <style>
            body { font-family: Arial; max-width: 500px; margin: 0 auto; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input, textarea { width: 100%; padding: 8px; }
            button { background: #4CAF50; color: white; padding: 10px; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>AIA Generator</h1>
        <form action="/generate" method="post">
            <div class="form-group">
                <label>App Name:</label>
                <input type="text" name="app_name" required>
            </div>
            <div class="form-group">
                <label>Number of Buttons:</label>
                <input type="number" name="button_count" value="2" min="1" max="10">
            </div>
            <button type="submit">Generate AIA</button>
        </form>
    </body>
    </html>
    '''

@app.route('/generate', methods=['POST'])
def generate_aia():
    try:
        app_name = request.form.get('app_name', 'MyApp')
        button_count = int(request.form.get('button_count', 1))
        
        # Create components
        components = []
        for i in range(1, button_count + 1):
            components.append({
                "$Name": f"Button{i}",
                "$Type": "Button",
                "$Version": "7",
                "Text": f"Button {i}",
                "Uuid": str(uuid.uuid4())
            })
        
        # Create project structure
        project_data = {
            "name": app_name,
            "assets": [],
            "YaVersion": "208",
            "Source": "Form",
            "Properties": {
                "$Name": "Screen1",
                "$Type": "Form",
                "$Version": "31",
                "AppName": app_name,
                "Title": app_name,
                "Uuid": str(uuid.uuid4()),
                "$Components": components
            }
        }
        
        # Create AIA file
        aia_buffer = io.BytesIO()
        with zipfile.ZipFile(aia_buffer, 'w', zipfile.ZIP_DEFLATED) as aia_file:
            # Add project.properties
            aia_file.writestr('youngandroidproject/project.properties', f'''
main=appinventor.ai_user.{app_name}.Screen1
name={app_name}
assets=../assets
source=../src
build=../build
versioncode=1
versionname=1.0
useslocation=false
aname={app_name}
            '''.strip())
            
            # Add Screen1.scm
            project_json = json.dumps(project_data, indent=2)
            aia_file.writestr(f'src/appinventor/ai_user/{app_name}/Screen1.scm', 
                              f'#|\n$JSON\n{project_json}\n|#')
            
            # Add empty directories
            for path in ['assets', 'src/appinventor/ai_user', 'build']:
                aia_file.writestr(f'{path}/.gitkeep', '')
        
        aia_buffer.seek(0)
        
        # Save locally for debugging
        with open(f'{app_name.replace(" ", "_")}.aia', 'wb') as f:
            f.write(aia_buffer.getvalue())
        
        aia_buffer.seek(0)
        return send_file(
            aia_buffer,
            as_attachment=True,
            download_name=f'{app_name.replace(" ", "_")}.aia',
            mimetype='application/zip'
        )
    
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    print("Starting AIA generator on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)