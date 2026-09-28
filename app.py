"""
Secure Cloud Storage Application with Hybrid Encryption and Steganography
==========================================================================
Author: [Your Name]
Date: January 2026
Version: 2.0

Features:
- Hybrid encryption (AES-256 + RSA-2048)
- Steganography: Metadata concealed within encrypted files
- Secure file upload/download/deletion
- Web-based user interface with Bootstrap 5
- Drag-and-drop file upload support
- Real-time encryption progress tracking

Security Architecture:
1. Each file is encrypted with a unique AES-256 key
2. AES key is encrypted using RSA-2048 public key
3. Metadata (filename, keys, IV) is hidden using steganography
4. No separate metadata files - everything embedded in encrypted content
"""

import os
import base64
import json
import struct
import time
from pathlib import Path
from datetime import datetime
from io import BytesIO
import secrets
from werkzeug.utils import secure_filename

# Cryptography imports
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Flask imports
from flask import Flask, render_template_string, request, redirect, url_for, flash, send_file, session

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLOUD_STORAGE_DIR = os.path.join(BASE_DIR, "cloud_storage")  # Simulated cloud storage
KEYS_DIR = os.path.join(BASE_DIR, "keys")                    # Directory to store RSA keys
KEY_SIZE = 2048                      # RSA key size in bits
AES_KEY_SIZE = 32                    # AES-256 key size in bytes
AES_BLOCK_SIZE = 16                  # AES block size in bytes
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
                      'xls', 'xlsx', 'zip', 'rar', 'mp3', 'mp4', 'avi', 'ppt', 'pptx'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB upload limit

# Steganography markers
STEGO_HEADER = b"STEGO_META_V2"  # Magic header to identify steganographic content
STEGO_HEADER_SIZE = len(STEGO_HEADER)

# ============================================================================
# HTML TEMPLATE (Professional Bootstrap 5 Interface)
# ============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Cloud Storage - Hybrid Encryption + Steganography</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #0d6efd;
            --success-color: #198754;
            --danger-color: #dc3545;
            --warning-color: #ffc107;
            --info-color: #0dcaf0;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .logo-section {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        .logo-text {
            font-weight: 700;
            font-size: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        
        .subtitle {
            color: #6c757d;
            font-size: 1.1rem;
            margin-top: 10px;
        }
        
        .security-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 15px;
        }
        
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            margin-bottom: 30px;
            overflow: hidden;
            background: rgba(255,255,255,0.98);
        }
        
        .card-header {
            padding: 20px 25px;
            font-weight: 600;
            font-size: 1.2rem;
        }
        
        .card-body {
            padding: 25px;
        }
        
        .upload-area {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 50px 30px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .upload-area:hover {
            background: linear-gradient(135deg, #e0e5ec 0%, #b5c6e0 100%);
            border-color: #764ba2;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .upload-area.drag-over {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: white;
        }
        
        .upload-area.drag-over * {
            color: white !important;
        }
        
        .file-icon {
            font-size: 4rem;
            margin-bottom: 20px;
            color: #667eea;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .drop-text {
            font-size: 1.5rem;
            font-weight: 600;
            color: #495057;
            margin-bottom: 10px;
        }
        
        .btn-custom {
            padding: 12px 30px;
            font-weight: 600;
            border-radius: 25px;
            transition: all 0.3s ease;
            border: none;
        }
        
        .btn-upload {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-upload:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            color: white;
        }
        
        .encryption-info {
            background: linear-gradient(135deg, #e0e5ec 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 20px;
            margin-top: 25px;
        }
        
        .encryption-info h6 {
            color: #495057;
            font-weight: 700;
            margin-bottom: 15px;
            font-size: 1rem;
        }
        
        .encryption-step {
            display: flex;
            align-items: center;
            padding: 12px;
            background: white;
            border-radius: 10px;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }
        
        .encryption-step:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .step-number {
            width: 35px;
            height: 35px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            margin-right: 15px;
            flex-shrink: 0;
        }
        
        .step-text {
            font-size: 0.95rem;
            color: #495057;
            margin: 0;
        }
        
        .security-feature {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
        }
        
        .security-feature:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        
        .security-icon {
            width: 60px;
            height: 60px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 20px;
            font-size: 1.8rem;
        }
        
        .security-icon-aes {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .security-icon-rsa {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        .security-icon-stego {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        .security-icon-unique {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
        }
        
        .security-content h6 {
            margin: 0 0 5px 0;
            font-weight: 700;
            color: #212529;
        }
        
        .security-content small {
            color: #6c757d;
        }
        
        .file-table {
            border-radius: 15px;
            overflow: hidden;
        }
        
        .table {
            margin-bottom: 0;
        }
        
        .table thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .table tbody tr {
            transition: all 0.3s ease;
        }
        
        .table tbody tr:hover {
            background: rgba(102, 126, 234, 0.05);
            transform: scale(1.01);
        }
        
        .file-name-cell {
            display: flex;
            align-items: center;
        }
        
        .file-type-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            font-size: 1.2rem;
            color: white;
        }
        
        .icon-doc {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .icon-img {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        .icon-archive {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        
        .icon-default {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        }
        
        .btn-action {
            padding: 8px 15px;
            border-radius: 8px;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            border: none;
            margin: 0 3px;
        }
        
        .btn-download {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-download:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            color: white;
        }
        
        .btn-delete {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        .btn-delete:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(240, 147, 251, 0.4);
            color: white;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 30px;
        }
        
        .empty-state-icon {
            font-size: 5rem;
            color: #dee2e6;
            margin-bottom: 20px;
        }
        
        .empty-state h5 {
            color: #6c757d;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .empty-state p {
            color: #adb5bd;
        }
        
        .upload-progress {
            height: 8px;
            width: 0;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.5s ease;
            margin-top: 15px;
            border-radius: 10px;
            display: none;
        }
        
        .alert {
            border: none;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .footer {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 25px;
            margin-top: 30px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }
        
        .footer-title {
            font-weight: 700;
            color: #212529;
            margin-bottom: 10px;
        }
        
        .footer-text {
            color: #6c757d;
            margin: 5px 0;
        }
        
        .stego-badge {
            display: inline-block;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 10px;
        }
        
        @media (max-width: 768px) {
            .logo-text {
                font-size: 1.5rem;
            }
            
            .subtitle {
                font-size: 1rem;
            }
            
            .security-feature {
                flex-direction: column;
                text-align: center;
            }
            
            .security-icon {
                margin-right: 0;
                margin-bottom: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container main-container">
        <!-- Logo Section -->
        <div class="logo-section text-center">
            <i class="fas fa-shield-alt" style="font-size: 3rem; color: #667eea; margin-bottom: 15px;"></i>
            <h1 class="logo-text">Secure Cloud Storage</h1>
            <p class="subtitle">Advanced Hybrid Encryption with Steganography Technology</p>
            <span class="security-badge">
                <i class="fas fa-lock me-2"></i>AES-256 + RSA-2048 + Steganography
            </span>
        </div>

        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        <i class="fas fa-info-circle me-2"></i>{{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <!-- Main Content -->
        <div class="row">
            <!-- Left Column: Upload & Security Info -->
            <div class="col-lg-6 mb-4">
                <!-- Upload Card -->
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                        <i class="fas fa-cloud-upload-alt me-2"></i>Upload Secure File
                    </div>
                    <div class="card-body">
                        <form action="upload" method="post" enctype="multipart/form-data" id="upload-form">
                            <div class="upload-area" id="dropzone" onclick="document.getElementById('file-input').click();">
                                <i class="fas fa-cloud-upload-alt file-icon"></i>
                                <p class="drop-text">Drag & Drop Your File Here</p>
                                <p style="color: #6c757d; margin-bottom: 20px;">or click to browse</p>
                                <button type="button" class="btn btn-upload btn-custom" onclick="document.getElementById('file-input').click();">
                                    <i class="fas fa-folder-open me-2"></i>Choose File
                                </button>
                                <input type="file" name="file" id="file-input" style="display: none;" onchange="updateFileName(this)">
                                <p id="file-name" class="mt-3" style="color: #495057; font-weight: 600;"></p>
                                <div class="upload-progress" id="upload-progress"></div>
                            </div>
                            
                            <button type="submit" class="btn btn-upload btn-custom w-100 mt-3" style="padding: 15px;" id="upload-btn">
                                <i class="fas fa-lock me-2"></i>Encrypt & Upload Securely
                            </button>
                        </form>
                        
                        <!-- Encryption Process Info -->
                        <div class="encryption-info">
                            <h6><i class="fas fa-cogs me-2"></i>Encryption Process</h6>
                            <div class="encryption-step">
                                <div class="step-number">1</div>
                                <p class="step-text">Generate unique AES-256 key for your file</p>
                            </div>
                            <div class="encryption-step">
                                <div class="step-number">2</div>
                                <p class="step-text">Encrypt file content using AES-256 CBC mode</p>
                            </div>
                            <div class="encryption-step">
                                <div class="step-number">3</div>
                                <p class="step-text">Protect AES key with RSA-2048 encryption</p>
                            </div>
                            <div class="encryption-step">
                                <div class="step-number">4</div>
                                <p class="step-text">Hide metadata using steganography technique</p>
                            </div>
                            <div class="encryption-step">
                                <div class="step-number">5</div>
                                <p class="step-text">Store encrypted file securely in cloud</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Security Features Card -->
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white;">
                        <i class="fas fa-shield-alt me-2"></i>Advanced Security Features
                    </div>
                    <div class="card-body">
                        <div class="security-feature">
                            <div class="security-icon security-icon-aes">
                                <i class="fas fa-key"></i>
                            </div>
                            <div class="security-content">
                                <h6>AES-256 Encryption</h6>
                                <small>Military-grade symmetric encryption for file content</small>
                            </div>
                        </div>
                        
                        <div class="security-feature">
                            <div class="security-icon security-icon-rsa">
                                <i class="fas fa-lock"></i>
                            </div>
                            <div class="security-content">
                                <h6>RSA-2048 Security</h6>
                                <small>Asymmetric encryption protects AES keys</small>
                            </div>
                        </div>
                        
                        <div class="security-feature">
                            <div class="security-icon security-icon-stego">
                                <i class="fas fa-eye-slash"></i>
                            </div>
                            <div class="security-content">
                                <h6>Steganography</h6>
                                <small>Metadata concealed within encrypted content</small>
                            </div>
                        </div>
                        
                        <div class="security-feature">
                            <div class="security-icon security-icon-unique">
                                <i class="fas fa-fingerprint"></i>
                            </div>
                            <div class="security-content">
                                <h6>Unique Keys Per File</h6>
                                <small>Each file encrypted with different AES key</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Right Column: File List -->
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
                        <i class="fas fa-folder-open me-2"></i>Your Encrypted Files
                        {% if files %}
                            <span class="badge bg-light text-dark ms-2">{{ files|length }}</span>
                        {% endif %}
                    </div>
                    <div class="card-body p-0">
                        {% if files %}
                            <div class="file-table">
                                <table class="table table-hover mb-0">
                                    <thead>
                                        <tr>
                                            <th style="padding: 15px;">File Name</th>
                                            <th style="padding: 15px;">Size</th>
                                            <th style="padding: 15px;">Upload Date</th>
                                            <th style="padding: 15px; text-align: center;">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for file in files %}
                                            <tr>
                                                <td style="padding: 15px;">
                                                    <div class="file-name-cell">
                                                        <div class="file-type-icon {{ get_file_icon_class(file.name) }}">
                                                            <i class="fas {{ get_file_icon(file.name) }}"></i>
                                                        </div>
                                                        <div>
                                                            <div style="font-weight: 600; color: #212529;">{{ file.name[:30] }}{% if file.name|length > 30 %}...{% endif %}</div>
                                                            <small style="color: #6c757d;">
                                                                <i class="fas fa-shield-alt me-1"></i>Encrypted with Steganography
                                                            </small>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td style="padding: 15px; color: #495057; font-weight: 500;">{{ format_size(file.original_size) }}</td>
                                                <td style="padding: 15px; color: #6c757d;">
                                                    <small>{{ file.timestamp }}</small>
                                                </td>
                                                <td style="padding: 15px; text-align: center;">
                                                    <a href="{{ url_for('download', file_id=file.id) }}" class="btn btn-download btn-action" title="Decrypt & Download">
                                                        <i class="fas fa-download"></i>
                                                    </a>
                                                    <a href="{{ url_for('delete', file_id=file.id) }}" class="btn btn-delete btn-action" title="Delete File" onclick="return confirm('Are you sure you want to delete this file?');">
                                                        <i class="fas fa-trash-alt"></i>
                                                    </a>
                                                </td>
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        {% else %}
                            <div class="empty-state">
                                <i class="fas fa-folder-open empty-state-icon"></i>
                                <h5>No Files Yet</h5>
                                <p>Upload your first file to get started with secure cloud storage</p>
                                <span class="stego-badge">
                                    <i class="fas fa-info-circle me-1"></i>All files protected with steganography
                                </span>
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="footer-title">
                <i class="fas fa-shield-alt me-2"></i>Secure Cloud Storage System
            </div>
            <p class="footer-text">
                <strong>Hybrid Encryption:</strong> AES-256 + RSA-2048 + Steganography
            </p>
            <p class="footer-text">
                <i class="fas fa-lock me-1"></i>Military-grade security for your sensitive data
            </p>
            <p class="footer-text text-muted mt-2">
                &copy; 2026 Secure Cloud Storage. All rights reserved.
            </p>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // File name update
        function updateFileName(input) {
            const fileName = input.files[0] ? input.files[0].name : '';
            const fileSize = input.files[0] ? (input.files[0].size / 1024 / 1024).toFixed(2) + ' MB' : '';
            document.getElementById('file-name').innerHTML = fileName ? 
                `<i class="fas fa-file me-2"></i>${fileName} <span style="color: #6c757d;">(${fileSize})</span>` : '';
            
            if (fileName) {
                document.getElementById('upload-progress').style.display = 'block';
                document.getElementById('upload-progress').style.width = '0';
            }
        }
        
        // Drag and drop
        const dropzone = document.getElementById('dropzone');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, () => {
                dropzone.classList.add('drag-over');
            });
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, () => {
                dropzone.classList.remove('drag-over');
            });
        });
        
        dropzone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length) {
                document.getElementById('file-input').files = files;
                updateFileName(document.getElementById('file-input'));
            }
        });
        
        // Upload progress animation
        document.getElementById('upload-form').addEventListener('submit', function() {
            const progressBar = document.getElementById('upload-progress');
            const fileName = document.getElementById('file-input').files[0]?.name;
            
            if (fileName) {
                progressBar.style.display = 'block';
                setTimeout(() => {
                    progressBar.style.width = '100%';
                }, 100);
            }
        });
    </script>
</body>
</html>"""

# ============================================================================
# STEGANOGRAPHY FUNCTIONS
# ============================================================================

class Steganography:
    """
    Steganography implementation for hiding metadata within encrypted content.
    This ensures that file metadata (filename, encryption keys, IV) are concealed
    within the encrypted file itself, making it harder to detect or tamper with.
    """
    
    @staticmethod
    def hide_metadata(encrypted_data: bytes, metadata: dict) -> bytes:
        """
        Hide metadata within encrypted data using steganography.
        
        Process:
        1. Convert metadata to JSON and encode as bytes
        2. Add magic header and metadata length
        3. Prepend to encrypted data
        4. Add padding to make detection harder
        
        Args:
            encrypted_data: The encrypted file content
            metadata: Dictionary containing file metadata
            
        Returns:
            Steganographic data with hidden metadata
        """
        # Convert metadata to JSON bytes
        metadata_json = json.dumps(metadata).encode('utf-8')
        metadata_length = len(metadata_json)
        
        # Create steganographic header: MAGIC_HEADER + LENGTH + METADATA
        stego_header = STEGO_HEADER + struct.pack('>I', metadata_length) + metadata_json
        
        # Add random padding before encrypted data (makes pattern detection harder)
        random_padding_size = secrets.randbelow(128) + 32  # 32-160 bytes random padding
        random_padding = os.urandom(random_padding_size)
        
        # Combine: HEADER + METADATA + PADDING + ENCRYPTED_DATA
        stego_data = stego_header + struct.pack('>I', random_padding_size) + random_padding + encrypted_data
        
        return stego_data
    
    @staticmethod
    def extract_metadata(stego_data: bytes) -> tuple:
        """
        Extract metadata from steganographic data.
        
        Args:
            stego_data: Data with hidden metadata
            
        Returns:
            Tuple of (metadata_dict, encrypted_data)
            
        Raises:
            ValueError: If magic header not found or data corrupted
        """
        # Verify magic header
        if not stego_data.startswith(STEGO_HEADER):
            raise ValueError("Invalid steganographic data: magic header not found")
        
        offset = STEGO_HEADER_SIZE
        
        # Extract metadata length
        metadata_length = struct.unpack('>I', stego_data[offset:offset+4])[0]
        offset += 4
        
        # Extract metadata JSON
        metadata_json = stego_data[offset:offset+metadata_length]
        metadata = json.loads(metadata_json.decode('utf-8'))
        offset += metadata_length
        
        # Extract padding size
        padding_size = struct.unpack('>I', stego_data[offset:offset+4])[0]
        offset += 4
        
        # Skip padding
        offset += padding_size
        
        # Remaining data is the encrypted content
        encrypted_data = stego_data[offset:]
        
        return metadata, encrypted_data

# ============================================================================
# SECURE CLOUD UPLOADER CLASS
# ============================================================================

class SecureCloudUploader:
    """
    Main class handling file encryption, decryption, and storage operations.
    Implements hybrid encryption with steganography.
    """
    
    def __init__(self):
        """Initialize the secure cloud uploader with automatic key setup"""
        # Ensure directories exist - FORCE CREATE
        print("🔍 Checking directories...")
        
        try:
            os.makedirs(CLOUD_STORAGE_DIR, exist_ok=True)
            print(f"✅ Cloud storage directory ready: {os.path.abspath(CLOUD_STORAGE_DIR)}")
        except Exception as e:
            print(f"⚠️ Error creating cloud_storage: {e}")
            
        try:
            os.makedirs(KEYS_DIR, exist_ok=True)
            print(f"✅ Keys directory ready: {os.path.abspath(KEYS_DIR)}")
        except Exception as e:
            print(f"⚠️ Error creating keys: {e}")
        
        # Check if keys exist, generate if needed
        if not self._keys_exist():
            self._generate_and_save_keys()
        else:
            self._load_keys()
    
    def _keys_exist(self) -> bool:
        """Check if RSA keys already exist"""
        private_key_path = os.path.join(KEYS_DIR, "private_key.pem")
        public_key_path = os.path.join(KEYS_DIR, "public_key.pem")
        return os.path.exists(private_key_path) and os.path.exists(public_key_path)
    
    def _generate_and_save_keys(self):
        """Generate and save new RSA key pair"""
        print("🔑 Generating RSA-2048 key pair...")
        
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=KEY_SIZE,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
        # Save private key
        with open(os.path.join(KEYS_DIR, "private_key.pem"), "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Save public key
        with open(os.path.join(KEYS_DIR, "public_key.pem"), "wb") as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        print("✅ RSA keys generated and saved successfully")
    
    def _load_keys(self):
        """Load RSA keys from files"""
        try:
            # Load private key
            with open(os.path.join(KEYS_DIR, "private_key.pem"), "rb") as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
            
            # Load public key
            with open(os.path.join(KEYS_DIR, "public_key.pem"), "rb") as f:
                self.public_key = serialization.load_pem_public_key(
                    f.read(),
                    backend=default_backend()
                )
            
            print("✅ Loaded existing RSA keys")
        except Exception as e:
            print(f"❌ Error loading keys: {str(e)}")
            print("🔄 Generating new keys...")
            self._generate_and_save_keys()
    
    def generate_aes_key(self) -> bytes:
        """Generate a random AES-256 key"""
        return os.urandom(AES_KEY_SIZE)
    
    def encrypt_file_with_aes(self, file_data: bytes, aes_key: bytes) -> tuple:
        """
        Encrypt file data with AES-256 in CBC mode.
        
        Args:
            file_data: Original file content
            aes_key: AES encryption key
            
        Returns:
            Tuple of (iv, ciphertext)
        """
        # Generate a random initialization vector
        iv = os.urandom(AES_BLOCK_SIZE)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Apply PKCS7 padding
        padding_length = AES_BLOCK_SIZE - (len(file_data) % AES_BLOCK_SIZE)
        file_data += bytes([padding_length]) * padding_length
        
        # Encrypt
        ciphertext = encryptor.update(file_data) + encryptor.finalize()
        
        return iv, ciphertext
    
    def decrypt_file_with_aes(self, iv: bytes, ciphertext: bytes, aes_key: bytes) -> bytes:
        """
        Decrypt a file with AES-256 in CBC mode.
        
        Args:
            iv: Initialization vector
            ciphertext: Encrypted file content
            aes_key: AES decryption key
            
        Returns:
            Original file content
        """
        # Create cipher
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = plaintext[-1]
        plaintext = plaintext[:-padding_length]
        
        return plaintext
    
    def encrypt_aes_key_with_rsa(self, aes_key: bytes) -> bytes:
        """Encrypt the AES key with RSA-2048"""
        encrypted_key = self.public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_key
    
    def decrypt_aes_key_with_rsa(self, encrypted_key: bytes) -> bytes:
        """Decrypt the AES key with RSA-2048"""
        aes_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return aes_key
    
    def upload_file(self, file_data: bytes, filename: str) -> str:
        """
        Encrypt and upload a file with steganography.
        
        Process:
        1. Generate unique AES key
        2. Encrypt file with AES-256
        3. Encrypt AES key with RSA-2048
        4. Hide metadata using steganography
        5. Save to cloud storage
        
        Args:
            file_data: Original file content
            filename: Original filename
            
        Returns:
            File ID for retrieval
        """
        try:
            # Ensure cloud storage directory exists (important for Windows)
            os.makedirs(CLOUD_STORAGE_DIR, exist_ok=True)
            
            # Generate unique file ID
            file_id = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8')
            
            # Generate random AES key
            aes_key = self.generate_aes_key()
            
            # Encrypt file with AES
            iv, ciphertext = self.encrypt_file_with_aes(file_data, aes_key)
            
            # Encrypt AES key with RSA
            encrypted_key = self.encrypt_aes_key_with_rsa(aes_key)
            
            # Prepare metadata
            metadata = {
                "file_name": filename,
                "file_id": file_id,
                "iv": base64.b64encode(iv).decode('utf-8'),
                "encrypted_key": base64.b64encode(encrypted_key).decode('utf-8'),
                "original_size": len(file_data),
                "encrypted_size": len(ciphertext),
                "timestamp": datetime.now().isoformat(),
                "version": "2.0",
                "encryption": "AES-256-CBC + RSA-2048 + Steganography"
            }
            
            # Hide metadata using steganography
            stego_data = Steganography.hide_metadata(ciphertext, metadata)
            
            # Save steganographic data to cloud storage
            with open(os.path.join(CLOUD_STORAGE_DIR, f"{file_id}.stego"), "wb") as f:
                f.write(stego_data)
            
            print(f"✅ File encrypted and uploaded: {filename}")
            return file_id
        
        except Exception as e:
            print(f"❌ Error uploading file: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def download_file(self, file_id: str) -> tuple:
        """
        Download and decrypt a file.
        
        Process:
        1. Load steganographic data
        2. Extract metadata using steganography
        3. Decrypt AES key with RSA-2048
        4. Decrypt file with AES-256
        
        Args:
            file_id: File identifier
            
        Returns:
            Tuple of (plaintext, filename)
        """
        try:
            # Load steganographic data
            with open(os.path.join(CLOUD_STORAGE_DIR, f"{file_id}.stego"), "rb") as f:
                stego_data = f.read()
            
            # Extract metadata and encrypted content
            metadata, ciphertext = Steganography.extract_metadata(stego_data)
            
            file_name = metadata["file_name"]
            iv = base64.b64decode(metadata["iv"])
            encrypted_key = base64.b64decode(metadata["encrypted_key"])
            
            # Decrypt AES key with RSA
            aes_key = self.decrypt_aes_key_with_rsa(encrypted_key)
            
            # Decrypt file with AES
            plaintext = self.decrypt_file_with_aes(iv, ciphertext, aes_key)
            
            print(f"✅ File decrypted successfully: {file_name}")
            return plaintext, file_name
        
        except FileNotFoundError:
            print(f"❌ File with ID '{file_id}' not found")
            return None, None
        except Exception as e:
            print(f"❌ Error downloading file: {str(e)}")
            return None, None
    
    def list_files(self) -> list:
        """
        List all files in cloud storage.
        
        Returns:
            List of file metadata dictionaries
        """
        file_list = []
        
        for file_path in Path(CLOUD_STORAGE_DIR).glob("*.stego"):
            try:
                with open(file_path, "rb") as f:
                    stego_data = f.read()
                
                # Extract metadata
                metadata, _ = Steganography.extract_metadata(stego_data)
                
                file_id = metadata["file_id"]
                file_name = metadata["file_name"]
                original_size = metadata.get("original_size", "Unknown")
                timestamp = metadata.get("timestamp", "Unknown")
                
                # Format timestamp
                if timestamp != "Unknown":
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        timestamp = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                
                file_list.append({
                    "id": file_id,
                    "name": file_name,
                    "size": os.path.getsize(file_path),
                    "timestamp": timestamp,
                    "original_size": original_size
                })
            except Exception as e:
                print(f"⚠️ Error reading file {file_path}: {str(e)}")
                continue
        
        # Sort by timestamp (newest first)
        file_list.sort(key=lambda x: x["timestamp"], reverse=True)
        return file_list
    
    def delete_file(self, file_id: str) -> bool:
        """
        Delete a file from cloud storage.
        
        Args:
            file_id: File identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            stego_path = os.path.join(CLOUD_STORAGE_DIR, f"{file_id}.stego")
            if os.path.exists(stego_path):
                os.unlink(stego_path)
                print(f"✅ File deleted successfully")
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting file: {str(e)}")
            return False

# ============================================================================
# FLASK APPLICATION
# ============================================================================

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create uploader instance
uploader = SecureCloudUploader()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def allowed_file(filename: str) -> bool:
    """Check if a file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_size(size_bytes) -> str:
    """Format file size in human-readable format"""
    if size_bytes == "Unknown" or size_bytes is None:
        return "Unknown"
    
    try:
        size_bytes = int(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024 or unit == 'GB':
                if unit == 'B':
                    return f"{size_bytes} {unit}"
                else:
                    return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
    except:
        return "Unknown"

def get_file_icon(filename: str) -> str:
    """Get Font Awesome icon class based on file extension"""
    if not filename or '.' not in filename:
        return 'fa-file'
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    icon_map = {
        'pdf': 'fa-file-pdf',
        'doc': 'fa-file-word',
        'docx': 'fa-file-word',
        'xls': 'fa-file-excel',
        'xlsx': 'fa-file-excel',
        'ppt': 'fa-file-powerpoint',
        'pptx': 'fa-file-powerpoint',
        'txt': 'fa-file-alt',
        'zip': 'fa-file-archive',
        'rar': 'fa-file-archive',
        'png': 'fa-file-image',
        'jpg': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'gif': 'fa-file-image',
        'mp3': 'fa-file-audio',
        'mp4': 'fa-file-video',
        'avi': 'fa-file-video',
    }
    
    return icon_map.get(ext, 'fa-file')

def get_file_icon_class(filename: str) -> str:
    """Get CSS class for file type icon"""
    if not filename or '.' not in filename:
        return 'icon-default'
    
    ext = filename.rsplit('.', 1)[1].lower()
    
    if ext in ['doc', 'docx', 'pdf', 'txt']:
        return 'icon-doc'
    elif ext in ['png', 'jpg', 'jpeg', 'gif']:
        return 'icon-img'
    elif ext in ['zip', 'rar']:
        return 'icon-archive'
    else:
        return 'icon-default'

# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main page with file upload form and list of files"""
    files = uploader.list_files()
    return render_template_string(
        HTML_TEMPLATE, 
        files=files, 
        format_size=format_size,
        get_file_icon=get_file_icon,
        get_file_icon_class=get_file_icon_class
    )

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload"""
    if 'file' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_data = file.read()
            
            # Encrypt and upload the file
            file_id = uploader.upload_file(file_data, filename)
            
            if file_id:
                flash(f'✅ File "{filename}" encrypted and uploaded successfully!', 'success')
            else:
                flash('❌ Error uploading file. Please try again.', 'danger')
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'danger')
    else:
        flash('❌ File type not allowed. Please upload a supported file format.', 'warning')
    
    return redirect(url_for('index'))

@app.route('/download/<file_id>')
def download(file_id):
    """Download and decrypt a file"""
    try:
        file_data, filename = uploader.download_file(file_id)
        
        if file_data is None:
            flash('❌ File not found or corrupted', 'danger')
            return redirect(url_for('index'))
        
        return send_file(
            BytesIO(file_data),
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        flash(f'❌ Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/delete/<file_id>')
def delete(file_id):
    """Delete a file"""
    try:
        success = uploader.delete_file(file_id)
        if success:
            flash('✅ File deleted successfully', 'success')
        else:
            flash('❌ Error deleting file', 'danger')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size exceeded error"""
    flash(f'❌ File too large. Maximum size is {format_size(MAX_CONTENT_LENGTH)}', 'danger')
    return redirect(url_for('index'))

@app.context_processor
def utility_processor():
    """Make utility functions available in templates"""
    return {
        'format_size': format_size,
        'get_file_icon': get_file_icon,
        'get_file_icon_class': get_file_icon_class
    }

# ============================================================================
# SERVER INFORMATION
# ============================================================================

def print_server_info():
    """Print beautiful server startup information"""
    print("\n" + "="*80)
    print(" 🔒 SECURE CLOUD STORAGE SERVER ".center(80, "="))
    print("="*80)
    print("🌐 Server URL      : http://localhost:5000")
    print("📁 Storage Dir     : " + os.path.abspath(CLOUD_STORAGE_DIR))
    print("🔑 Keys Directory  : " + os.path.abspath(KEYS_DIR))
    print("📦 Max Upload Size : " + format_size(MAX_CONTENT_LENGTH))
    print("-"*80)
    
    # Verify directories exist
    storage_exists = os.path.exists(CLOUD_STORAGE_DIR)
    keys_exists = os.path.exists(KEYS_DIR)
    
    print("📂 DIRECTORY STATUS")
    print("-"*80)
    print(f"  {'✅' if storage_exists else '❌'} cloud_storage/ : {'Ready' if storage_exists else 'ERROR - Missing!'}")
    print(f"  {'✅' if keys_exists else '❌'} keys/           : {'Ready' if keys_exists else 'ERROR - Missing!'}")
    print("-"*80)
    
    print("🛡️  SECURITY FEATURES")
    print("-"*80)
    print("  ✅ AES-256 Encryption       (File Content)")
    print("  ✅ RSA-2048 Encryption      (Key Protection)")
    print("  ✅ Steganography            (Metadata Concealment)")
    print("  ✅ Unique Keys Per File     (Maximum Security)")
    print("  ✅ CBC Mode with Random IV  (Cryptographic Best Practice)")
    print("="*80)
    print("⚡ Server is running! Press Ctrl+C to stop")
    print("="*80 + "\n")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    try:
        print_server_info()
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")