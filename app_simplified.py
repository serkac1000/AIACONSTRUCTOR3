from flask import Flask, render_template, request, jsonify, send_file 
import json 
import zipfile 
import io 
import os 
import uuid 
from datetime import datetime 
 
app = Flask(__name__) 
 
# HTML template for the web interface 
