from flask import Flask, render_template, request, jsonify, send_file
import json
import zipfile
import io
import os
import uuid
import base64
import requests
from datetime import datetime

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIT App Inventor AIA Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        input[type="text"], textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
            box-sizing: border-box;
        }
        input[type="text"]:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea {
            height: 150px;
            resize: vertical;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            transition: transform 0.2s;
            display: block;
            margin: 20px auto;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .btn-secondary {
            background: #6c757d;
            padding: 10px 20px;
            font-size: 16px;
            margin: 10px 5px;
            display: inline-block;
        }
        .btn-success {
            background: #28a745;
            padding: 10px 20px;
            font-size: 16px;
            margin: 10px 5px;
            display: inline-block;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            display: none;
        }
        .download-link {
            background: #28a745;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin-top: 10px;
        }
        .row {
            display: flex;
            gap: 20px;
        }
        .col {
            flex: 1;
        }
        .image-preview {
            max-width: 100%;
            max-height: 300px;
            margin-top: 10px;
            border: 2px dashed #ddd;
            border-radius: 8px;
            display: none;
        }
        .file-input-container {
            position: relative;
            overflow: hidden;
            display: inline-block;
            margin-top: 10px;
        }
        .file-input-container input[type=file] {
            font-size: 100px;
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            cursor: pointer;
        }
        .file-input-button {
            background: #6c757d;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            display: inline-block;
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            margin-right: 5px;
            border-radius: 5px 5px 0 0;
        }
        .tab.active {
            background: #667eea;
            color: white;
            border-bottom: 2px solid #667eea;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .preview-container {
            margin-top: 20px;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            background: #f8f9fa;
        }
        .preview-phone {
            width: 300px;
            height: 600px;
            margin: 0 auto;
            border: 10px solid #333;
            border-radius: 30px;
            background: white;
            position: relative;
            overflow: hidden;
        }
        .preview-screen {
            width: 100%;
            height: 100%;
            background: white;
            position: relative;
        }
        .preview-component {
            position: absolute;
            background: #eee;
            border: 1px solid #ccc;
            padding: 5px;
            border-radius: 5px;
            font-size: 14px;
        }
        .api-section {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        .api-response {
            margin-top: 15px;
            padding: 15px;
            background: #e9ecef;
            border-radius: 5px;
            font-family: monospace;
            white-space: pre-wrap;
            display: none;
        }
        @media (max-width: 768px) {
            .row {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 MIT App Inventor AIA Generator</h1>

        <div class="tabs">
            <div class="tab active" data-tab="basic">Basic Settings</div>
            <div class="tab" data-tab="design">Design Upload</div>
            <div class="tab" data-tab="ai">AI Coding</div>
            <div class="tab" data-tab="preview">App Preview</div>
        </div>

        <form id="aiaForm">
            <div class="tab-content active" id="basic-tab">
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label for="appName">App Name:</label>
                            <input type="text" id="appName" name="appName" required placeholder="My Awesome App">
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label for="appType">App Type:</label>
                            <select id="appType" name="appType">
                                <option value="basic">Basic App</option>
                                <option value="game">Game</option>
                                <option value="utility">Utility</option>
                                <option value="educational">Educational</option>
                                <option value="social">Social</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="prompt">Describe your app (be specific about features, UI, and functionality):</label>
                    <textarea id="prompt" name="prompt" required placeholder="Create a simple calculator app with buttons for numbers 0-9, basic operations (+, -, *, /), equals button, and clear button. The app should have a display screen showing the current number and result. Use a clean, modern design with blue buttons and white background."></textarea>
                </div>
            </div>

            <div class="tab-content" id="design-tab">
                <div class="form-group">
                    <label for="designImage">Upload Design Image (optional):</label>
                    <div class="file-input-container">
                        <div class="file-input-button">Choose Image</div>
                        <input type="file" id="designImage" name="designImage" accept="image/*">
                    </div>
                    <p>Upload a sketch, mockup, or reference design for your app</p>
                    <img id="imagePreview" class="image-preview" alt="Design Preview">
                    <input type="hidden" id="imageData" name="imageData">
                </div>
            </div>

            <div class="tab-content" id="ai-tab">
                <div class="api-section">
                    <div class="form-group">
                        <label for="geminiApiKey">Gemini API Key:</label>
                        <input type="text" id="geminiApiKey" name="geminiApiKey" placeholder="Enter your Gemini API key">
                    </div>
                    <div class="form-group">
                        <label for="aiPrompt">AI Prompt for Code Generation:</label>
                        <textarea id="aiPrompt" name="aiPrompt" placeholder="Generate blocks code for a calculator app that can add, subtract, multiply and divide two numbers"></textarea>
                    </div>
                    <button type="button" id="saveApiKey" class="btn btn-secondary">Save API Key</button>
                    <button type="button" id="testApiKey" class="btn btn-success">Test API</button>
                    <div class="api-response" id="apiResponse"></div>
                </div>
            </div>

            <div class="tab-content" id="preview-tab">
                <div class="preview-container">
                    <h3>App Preview</h3>
                    <p>This is a simplified preview of how your app might look. The actual appearance in MIT App Inventor may vary.</p>
                    <div class="preview-phone">
                        <div class="preview-screen" id="previewScreen">
                            <!-- Components will be added here dynamically -->
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" class="btn">Generate AIA File</button>
        </form>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Generating your MIT App Inventor project...</p>
        </div>

        <div class="result" id="result">
            <h3>Success! 🎉</h3>
            <p>Your AIA file has been generated successfully.</p>
            <a href="#" class="download-link" id="downloadLink">Download AIA File</a>
        </div>
    </div>

    <script>
        // Tab functionality
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', function() {
                // Remove active class from all tabs
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                // Add active class to clicked tab
                this.classList.add('active');

                // Hide all tab content
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
                // Show content for clicked tab
                document.getElementById(this.dataset.tab + '-tab').classList.add('active');
            });
        });

        // Image upload preview
        document.getElementById('designImage').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const imagePreview = document.getElementById('imagePreview');
                    imagePreview.src = event.target.result;
                    imagePreview.style.display = 'block';

                    // Store base64 image data
                    document.getElementById('imageData').value = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        });

        // Save API Key
        document.getElementById('saveApiKey').addEventListener('click', function() {
            const apiKey = document.getElementById('geminiApiKey').value;
            if (apiKey) {
                localStorage.setItem('geminiApiKey', apiKey);
                alert('API Key saved successfully!');
            } else {
                alert('Please enter an API Key');
            }
        });

        // Load saved API Key
        if (localStorage.getItem('geminiApiKey')) {
            document.getElementById('geminiApiKey').value = localStorage.getItem('geminiApiKey');
        }

        // Test API Key
        document.getElementById('testApiKey').addEventListener('click', async function() {
            const apiKey = document.getElementById('geminiApiKey').value;
            const prompt = document.getElementById('aiPrompt').value || 'Generate a simple greeting';

            if (!apiKey) {
                alert('Please enter an API Key');
                return;
            }

            const apiResponse = document.getElementById('apiResponse');
            apiResponse.textContent = 'Testing API connection...';
            apiResponse.style.display = 'block';

            try {
                const response = await fetch('/test-gemini-api', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ apiKey, prompt })
                });

                const data = await response.json();

                if (response.ok) {
                    apiResponse.textContent = 'API Test Successful! Response:\n\n' + data.response;
                } else {
                    apiResponse.textContent = 'API Test Failed: ' + data.error;
                }
            } catch (error) {
                apiResponse.textContent = 'Error: ' + error.message;
            }
        });

        // Generate preview based on form inputs
        function updatePreview() {
            const appName = document.getElementById('appName').value || 'My App';
            const appType = document.getElementById('appType').value;
            const prompt = document.getElementById('prompt').value;

            // Clear previous preview
            const previewScreen = document.getElementById('previewScreen');
            previewScreen.innerHTML = '';

            // Add app title
            const titleBar = document.createElement('div');
            titleBar.style.width = '100%';
            titleBar.style.height = '40px';
            titleBar.style.backgroundColor = '#3F51B5';
            titleBar.style.color = 'white';
            titleBar.style.textAlign = 'center';
            titleBar.style.lineHeight = '40px';
            titleBar.style.fontWeight = 'bold';
            titleBar.textContent = appName;
            previewScreen.appendChild(titleBar);

            // Parse prompt for components
            if (prompt.toLowerCase().includes('calculator')) {
                // Add calculator display
                const display = document.createElement('div');
                display.className = 'preview-component';
                display.style.top = '50px';
                display.style.left = '10px';
                display.style.right = '10px';
                display.style.height = '60px';
                display.style.backgroundColor = 'white';
                display.style.border = '1px solid #ddd';
                display.style.textAlign = 'right';
                display.style.fontSize = '24px';
                display.style.lineHeight = '60px';
                display.style.paddingRight = '10px';
                display.textContent = '0';
                previewScreen.appendChild(display);

                // Add calculator buttons
                const buttonContainer = document.createElement('div');
                buttonContainer.style.position = 'absolute';
                buttonContainer.style.top = '120px';
                buttonContainer.style.left = '10px';
                buttonContainer.style.right = '10px';
                buttonContainer.style.bottom = '10px';
                buttonContainer.style.display = 'grid';
                buttonContainer.style.gridTemplateColumns = 'repeat(4, 1fr)';
                buttonContainer.style.gridGap = '10px';

                // Numbers and operations
                const buttons = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '=', '+'];
                buttons.forEach(btn => {
                    const button = document.createElement('div');
                    button.className = 'preview-component';
                    button.style.position = 'relative';
                    button.style.height = '50px';
                    button.style.backgroundColor = isNaN(btn) ? '#FF4081' : '#3F51B5';
                    button.style.color = 'white';
                    button.style.textAlign = 'center';
                    button.style.lineHeight = '50px';
                    button.style.borderRadius = '5px';
                    button.textContent = btn;
                    buttonContainer.appendChild(button);
                });

                previewScreen.appendChild(buttonContainer);
            } else if (prompt.toLowerCase().includes('list')) {
                // Create a list view
                const listView = document.createElement('div');
                listView.style.position = 'absolute';
                listView.style.top = '50px';
                listView.style.left = '10px';
                listView.style.right = '10px';
                listView.style.bottom = '10px';
                listView.style.backgroundColor = 'white';
                listView.style.border = '1px solid #ddd';
                listView.style.overflow = 'auto';

                // Add list items
                for (let i = 1; i <= 10; i++) {
                    const item = document.createElement('div');
                    item.style.padding = '15px';
                    item.style.borderBottom = '1px solid #eee';
                    item.textContent = 'Item ' + i;
                    listView.appendChild(item);
                }

                previewScreen.appendChild(listView);
            } else {
                // Default layout with some basic components
                const label = document.createElement('div');
                label.className = 'preview-component';
                label.style.top = '70px';
                label.style.left = '50%';
                label.style.transform = 'translateX(-50%)';
                label.style.padding = '10px 20px';
                label.textContent = 'Welcome to ' + appName;
                previewScreen.appendChild(label);

                const button = document.createElement('div');
                button.className = 'preview-component';
                button.style.top = '150px';
                button.style.left = '50%';
                button.style.transform = 'translateX(-50%)';
                button.style.padding = '15px 30px';
                button.style.backgroundColor = '#3F51B5';
                button.style.color = 'white';
                button.style.borderRadius = '5px';
                button.textContent = 'Click Me';
                previewScreen.appendChild(button);
            }
        }

        // Update preview when inputs change
        document.getElementById('appName').addEventListener('input', updatePreview);
        document.getElementById('appType').addEventListener('change', updatePreview);
        document.getElementById('prompt').addEventListener('input', updatePreview);

        // Initial preview update
        document.addEventListener('DOMContentLoaded', updatePreview);

        // Form submission
        document.getElementById('aiaForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);

            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.querySelector('.btn').disabled = true;

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const filename = `${data.appName.replace(/[^a-z0-9]/gi, '_')}.aia`;

                    document.getElementById('downloadLink').href = url;
                    document.getElementById('downloadLink').download = filename;
                    document.getElementById('result').style.display = 'block';
                } else {
                    alert('Error generating AIA file. Please try again.');
                }
            } catch (error) {
                alert('Network error. Please check your connection and try again.');
            }

            document.getElementById('loading').style.display = 'none';
            document.querySelector('.btn').disabled = false;
        });
    </script>
</body>
</html>
'''

def create_basic_project_structure(app_name, app_type, prompt):
    """Create basic MIT App Inventor project structure based on prompt"""

    # Base project properties
    project_properties = {
        "name": app_name,
        "assets": [],
        "settings": {
            "icon": "",
            "versioncode": "1",
            "versionname": "1.0",
            "useslocation": "false",
            "aname": app_name,
            "sizing": "Responsive",
            "showlistsasjson": "true",
            "actionbar": "false",
            "theme": "AppTheme.Light.DarkActionBar",
            "color_primary": "#3F51B5",
            "color_primary_dark": "#303F9F",
            "color_accent": "#FF4081"
        },
        "authURL": [],
        "YaVersion": "208",
        "Source": "Form",
        "Properties": {
            "$Name": "Screen1",
            "$Type": "Form",
            "$Version": "31",
            "AppName": app_name,
            "Title": app_name,
            "Uuid": str(uuid.uuid4())
        }
    }

    # Generate components based on app type and prompt
    components = []

    # Parse prompt for common UI elements
    prompt_lower = prompt.lower()

    if 'button' in prompt_lower:
        components.append({
            "$Name": "Button1",
            "$Type": "Button",
            "$Version": "7",
            "Text": "Click Me",
            "Uuid": str(uuid.uuid4())
        })

    if 'label' in prompt_lower or 'text' in prompt_lower or 'display' in prompt_lower:
        components.append({
            "$Name": "Label1",
            "$Type": "Label",
            "$Version": "5",
            "Text": "Hello World!",
            "Uuid": str(uuid.uuid4())
        })

    if 'textbox' in prompt_lower or 'input' in prompt_lower:
        components.append({
            "$Name": "TextBox1",
            "$Type": "TextBox",
            "$Version": "5",
            "Hint": "Enter text here",
            "Uuid": str(uuid.uuid4())
        })

    if 'image' in prompt_lower:
        components.append({
            "$Name": "Image1",
            "$Type": "Image",
            "$Version": "4",
            "Uuid": str(uuid.uuid4())
        })

    if 'list' in prompt_lower:
        components.append({
            "$Name": "ListView1",
            "$Type": "ListView",
            "$Version": "6",
            "Uuid": str(uuid.uuid4())
        })

    # Add calculator-specific components if mentioned
    if 'calculator' in prompt_lower:
        # Add number buttons
        for i in range(10):
            components.append({
                "$Name": f"Button{i}",
                "$Type": "Button",
                "$Version": "7",
                "Text": str(i),
                "Uuid": str(uuid.uuid4())
            })

        # Add operation buttons
        operations = ['+', '-', '*', '/', '=', 'C']
        for i, op in enumerate(operations):
            components.append({
                "$Name": f"ButtonOp{i}",
                "$Type": "Button",
                "$Version": "7",
                "Text": op,
                "Uuid": str(uuid.uuid4())
            })

        # Add display label
        components.append({
            "$Name": "DisplayLabel",
            "$Type": "Label",
            "$Version": "5",
            "Text": "0",
            "FontSize": "24",
            "Uuid": str(uuid.uuid4())
        })

    # Add components to project
    if components:
        project_properties["Properties"]["$Components"] = components

    return project_properties

def create_blocks_file(app_name, components):
    """Create basic blocks file with simple event handlers"""
    blocks_data = {
        "YaVersion": "208",
        "Source": "Form",
        "Properties": {
            "$Name": "Screen1",
            "$Type": "Form",
            "$Version": "31",
            "Uuid": str(uuid.uuid4()),
            "$Components": []
        }
    }

    # Add basic event blocks for buttons
    event_blocks = []
    for component in components:
        if component.get("$Type") == "Button":
            event_blocks.append({
                "type": "component_event",
                "id": str(uuid.uuid4()),
                "component": component["$Name"],
                "event": "Click"
            })

    if event_blocks:
        blocks_data["blocks"] = event_blocks

    return blocks_data

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/test-gemini-api', methods=['POST'])
def test_gemini_api():
    try:
        data = request.json
        api_key = data.get('apiKey')
        prompt = data.get('prompt', 'Generate a simple greeting')

        if not api_key:
            return jsonify({'error': 'API key is required'}), 400

        # Call Gemini API
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            # Extract text from the response
            if 'candidates' in result and len(result['candidates']) > 0:
                if 'content' in result['candidates'][0] and 'parts' in result['candidates'][0]['content']:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    return jsonify({'response': text})

            return jsonify({'error': 'Could not parse API response'}), 500
        else:
            return jsonify({'error': f'API Error: {response.status_code} - {response.text}'}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_aia():
    try:
        data = request.json
        app_name = data.get('appName', 'MyApp')
        app_type = data.get('appType', 'basic')
        prompt = data.get('prompt', '')
        image_data = data.get('imageData', '')
        gemini_api_key = data.get('geminiApiKey', '')
        ai_prompt = data.get('aiPrompt', '')

        # Create project structure
        project_data = create_basic_project_structure(app_name, app_type, prompt)
        components = project_data["Properties"].get("$Components", [])

        # If AI coding is requested, use Gemini API to enhance blocks
        ai_generated_blocks = None
        if gemini_api_key and ai_prompt:
            try:
                # Call Gemini API for AI-generated code
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
                headers = {
                    "Content-Type": "application/json",
                    "x-goog-api-key": gemini_api_key
                }

                # Enhance the prompt with specific instructions for MIT App Inventor blocks
                enhanced_prompt = f"""
                Generate MIT App Inventor blocks code for the following app:
                App Name: {app_name}
                App Type: {app_type}
                Description: {prompt}

                User's specific request: {ai_prompt}

                Please provide the blocks code in a format that can be used in MIT App Inventor.
                Focus on functionality that matches the description.
                """

                payload = {
                    "contents": [{
                        "parts": [{
                            "text": enhanced_prompt
                        }]
                    }]
                }

                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    if 'candidates' in result and len(result['candidates']) > 0:
                        if 'content' in result['candidates'][0] and 'parts' in result['candidates'][0]['content']:
                            ai_generated_blocks = result['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                print(f"Error using Gemini API: {str(e)}")

        # Create blocks data
        blocks_data = create_blocks_file(app_name, components)

        # If AI generated blocks are available, add them to documentation
        if ai_generated_blocks:
            blocks_data["ai_generated_code"] = ai_generated_blocks

        # Create AIA file in memory
        aia_buffer = io.BytesIO()

        with zipfile.ZipFile(aia_buffer, 'w', zipfile.ZIP_DEFLATED) as aia_file:
            # Add project.properties
            project_json = json.dumps(project_data, indent=2)
            aia_file.writestr('youngandroidproject/project.properties', f"""
main=appinventor.ai_user.{app_name}.Screen1
name={app_name}
assets=../assets
source=../src
build=../build
versioncode=1
versionname=1.0
useslocation=false
aname={app_name}
            """.strip())

            # Add Screen1.scm (scheme file)
            screen_scm = f"#|\n$JSON\n{project_json}\n|#"
            aia_file.writestr(f'src/appinventor/ai_user/{app_name}/Screen1.scm', screen_scm)

            # Add Screen1.bky (blocks file)
            blocks_json = json.dumps(blocks_data, indent=2)
            blocks_content = f"#|\n$JSON\n{blocks_json}\n|#"
            aia_file.writestr(f'src/appinventor/ai_user/{app_name}/Screen1.bky', blocks_content)

            # Add required empty directories
            for dir_path in ['assets', 'src', 'build']:
                aia_file.writestr(f'{dir_path}/.gitkeep', '')

            # Add proper directory structure
            aia_file.writestr(f'src/appinventor/ai_user/{app_name}/.gitkeep', '')

            # Add design image if provided
            if image_data and image_data.startswith('data:image/'):
                try:
                    # Extract the base64 encoded image data
                    image_format = image_data.split(';')[0].split('/')[1]
                    image_base64 = image_data.split(',')[1]
                    image_binary = base64.b64decode(image_base64)

                    # Save the image as an asset
                    image_filename = f'design_reference.{image_format}'
                    aia_file.writestr(f'assets/{image_filename}', image_binary)

                    # Add the image to project assets list
                    project_data['assets'].append(image_filename)

                    # Update the project.json with the new asset
                    updated_project_json = json.dumps(project_data, indent=2)
                    screen_scm = f"#|\n$JSON\n{updated_project_json}\n|#"
                    aia_file.writestr(f'src/appinventor/ai_user/{app_name}/Screen1.scm', screen_scm)
                except Exception as e:
                    print(f"Error processing image: {str(e)}")

            # Add AI-generated documentation if available
            if ai_generated_blocks:
                aia_file.writestr('assets/ai_generated_code.txt', ai_generated_blocks)

                # Create a documentation component in the app if AI code was generated
                if 'ai_generated_code' in blocks_data:
                    # Add a button to view AI code
                    ai_button = {
                        "$Name": "ViewAICodeButton",
                        "$Type": "Button",
                        "$Version": "7",
                        "Text": "View AI Generated Code",
                        "Uuid": str(uuid.uuid4())
                    }

                    if "$Components" in project_data["Properties"]:
                        project_data["Properties"]["$Components"].append(ai_button)
                    else:
                        project_data["Properties"]["$Components"] = [ai_button]

                    # Update the project.json with the new component
                    updated_project_json = json.dumps(project_data, indent=2)
                    screen_scm = f"#|\n$JSON\n{updated_project_json}\n|#"
                    aia_file.writestr(f'src/appinventor/ai_user/{app_name}/Screen1.scm', screen_scm)

            # Add a simple asset file to ensure assets are properly recognized
            aia_file.writestr('assets/README.txt', f'Assets for {app_name}')

        aia_buffer.seek(0)

        # Save a copy locally for debugging
        with open(f'{app_name.replace(" ", "_")}.aia', 'wb') as f:
            f.write(aia_buffer.getvalue())

        # Reset buffer position
        aia_buffer.seek(0)

        return send_file(
            aia_buffer,
            as_attachment=True,
            download_name=f'{app_name.replace(" ", "_")}.aia',
            mimetype='application/zip'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting MIT App Inventor AIA Generator Server...")
    print("📱 Server running at: http://127.0.0.1:5000")
    print("💡 Navigate to the URL above to start creating AIA files!")
    app.run(host='0.0.0.0', port=5000, debug=True)