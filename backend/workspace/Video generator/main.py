
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from services.video_generator import VideoGenerator
from services.image_animator import ImageAnimator
from services.voice_cloner import VoiceCloner
from services.ai_character import AICharacter
from services.timeline_editor import TimelineEditor
from services.youtube_clip_generator import YouTubeClipGenerator
from services.video_exporter import VideoExporter

app = Flask(__name__)
CORS(app)

# Load configuration
config = Config()

# Initialize services
video_generator = VideoGenerator()
image_animator = ImageAnimator()
voice_cloner = VoiceCloner()
ai_character = AICharacter()
timeline_editor = TimelineEditor()
youtube_clip_generator = YouTubeClipGenerator()
video_exporter = VideoExporter()

# API Endpoints
@app.route('/generate_video', methods=['POST'])
def generate_video():
    data = request.get_json()
    video = video_generator.generate_video(data['prompt'], data['reference_image'])
    return jsonify({'video': video})

@app.route('/animate_image', methods=['POST'])
def animate_image():
    data = request.get_json()
    animation = image_animator.animate_image(data['image'], data['animation_style'])
    return jsonify({'animation': animation})

@app.route('/clone_voice', methods=['POST'])
def clone_voice():
    data = request.get_json()
    cloned_voice = voice_cloner.clone_voice(data['voice'], data['text'])
    return jsonify({'cloned_voice': cloned_voice})

@app.route('/create_ai_character', methods=['POST'])
def create_ai_character():
    data = request.get_json()
    character = ai_character.create_ai_character(data['character_name'], data['character_description'])
    return jsonify({'character': character})

@app.route('/edit_video', methods=['POST'])
def edit_video():
    data = request.get_json()
    edited_video = timeline_editor.edit_video(data['video'], data['edits'])
    return jsonify({'edited_video': edited_video})

@app.route('/generate_youtube_clip', methods=['POST'])
def generate_youtube_clip():
    data = request.get_json()
    clip = youtube_clip_generator.generate_youtube_clip(data['video'], data['clip_length'])
    return jsonify({'clip': clip})

@app.route('/export_video', methods=['POST'])
def export_video():
    data = request.get_json()
    exported_video = video_exporter.export_video(data['video'], data['resolution'])
    return jsonify({'exported_video': exported_video})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
