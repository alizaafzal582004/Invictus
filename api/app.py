from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
import cv2
import numpy as np
import tempfile
from io import BytesIO
import json

app = Flask(__name__)

# Simple angle calculation function
def calculate_angle(a, b, c):
    """Calculate angle between three points"""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Simple pose detection using OpenCV (fallback without YOLO)
def detect_pose_simple(image):
    """Simple pose detection using basic computer vision"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # This is a simplified version - in production you'd use MediaPipe or similar
    # For demo purposes, return dummy keypoints
    height, width = image.shape[:2]
    
    # Dummy keypoints for demonstration
    keypoints = {
        'left_shoulder': [width*0.3, height*0.3],
        'left_elbow': [width*0.25, height*0.5],
        'left_wrist': [width*0.2, height*0.7],
        'right_shoulder': [width*0.7, height*0.3],
        'right_elbow': [width*0.75, height*0.5],
        'right_wrist': [width*0.8, height*0.7]
    }
    
    return keypoints

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.get_json()
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process image (simplified version)
        keypoints = detect_pose_simple(image)
        
        # Calculate arm angle
        left_angle = calculate_angle(
            keypoints['left_shoulder'],
            keypoints['left_elbow'], 
            keypoints['left_wrist']
        )
        
        right_angle = calculate_angle(
            keypoints['right_shoulder'],
            keypoints['right_elbow'],
            keypoints['right_wrist']
        )
        
        # Average angle
        avg_angle = (left_angle + right_angle) / 2
        
        # Determine stage
        stage = "up" if avg_angle > 145 else "down" if avg_angle < 105 else "mid"
        
        return jsonify({
            'success': True,
            'angle': round(avg_angle, 1),
            'stage': stage,
            'keypoints': keypoints
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)