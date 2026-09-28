# 🔒 Secure Cloud Storage System

**Advanced Hybrid Encryption with Steganography Technology**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Security-AES--256%20%2B%20RSA--2048-red)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Security Architecture](#security-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

The Secure Cloud Storage System is a state-of-the-art file encryption and storage solution that implements **hybrid encryption** combining **AES-256** and **RSA-2048** algorithms along with **steganography** to provide maximum security for sensitive data. Unlike traditional cloud storage services that store files without strong encryption or with easily detectable security measures, this system ensures that:

- Every file is encrypted with military-grade AES-256 encryption
- Encryption keys are protected using RSA-2048 asymmetric encryption
- File metadata is concealed using steganography techniques
- No separate metadata files are stored - everything is embedded within encrypted content

## ✨ Key Features

### 🛡️ Advanced Security
- **AES-256 Encryption**: Military-grade symmetric encryption for file content
- **RSA-2048 Key Protection**: Asymmetric encryption secures AES keys
- **Steganography**: Metadata concealed within encrypted files
- **Unique Keys**: Each file encrypted with a different AES key
- **CBC Mode**: Cryptographically secure cipher block chaining
- **Random IVs**: Initialization vectors generated for each encryption

### 🎨 Modern User Interface
- **Responsive Design**: Bootstrap 5 powered, mobile-friendly interface
- **Drag & Drop**: Intuitive file upload experience
- **Real-time Progress**: Visual feedback during uploads
- **Professional UI**: Beautiful gradient themes and animations
- **File Management**: Easy download and delete operations

### 🚀 Performance & Reliability
- **Fast Encryption**: Optimized cryptographic operations
- **Large File Support**: Handles files up to 50 MB
- **Error Handling**: Comprehensive error checking and reporting
- **Auto Key Management**: Automatic RSA key generation and loading
- **File Type Support**: Wide range of supported file formats

## 🏗️ Security Architecture

### Encryption Process Flow

```
1. File Upload
   ↓
2. Generate Unique AES-256 Key (256-bit)
   ↓
3. Encrypt File Content (AES-256-CBC)
   ↓
4. Encrypt AES Key (RSA-2048-OAEP)
   ↓
5. Create Metadata Package
   ↓
6. Hide Metadata via Steganography
   ↓
7. Store Steganographic File
```

### Decryption Process Flow

```
1. File Download Request
   ↓
2. Load Steganographic File
   ↓
3. Extract Hidden Metadata
   ↓
4. Decrypt AES Key (RSA-2048)
   ↓
5. Decrypt File Content (AES-256)
   ↓
6. Return Original File
```

### Steganography Implementation

The system uses a custom steganography technique to hide metadata within the encrypted file:

```
[MAGIC_HEADER][METADATA_LENGTH][METADATA_JSON][PADDING_SIZE][RANDOM_PADDING][ENCRYPTED_DATA]
```

**Benefits:**
- No separate metadata files to manage or secure
- Harder to detect the presence of metadata
- Protection against metadata tampering
- Simplified file management

## 💻 Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0.0**: Web framework for server and routing
- **Cryptography 41.0.7**: Industry-standard cryptographic library

### Frontend
- **HTML5**: Modern markup
- **CSS3**: Advanced styling with gradients and animations
- **Bootstrap 5.3**: Responsive UI framework
- **Font Awesome 6.0**: Professional icon library
- **Vanilla JavaScript**: No dependencies, pure JS

### Security Libraries
- **cryptography.hazmat**: Low-level cryptographic primitives
- **RSA (OAEP)**: Optimal Asymmetric Encryption Padding
- **AES (CBC)**: Cipher Block Chaining mode
- **SHA-256**: Hashing for key derivation

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 100 MB free disk space

### Step-by-Step Installation

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd secure-cloud-storage
   
   # Or download and extract the ZIP file
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python secure_cloud_storage_enhanced.py
   ```

5. **Access the Application**
   - Open your browser and navigate to: `http://localhost:5000`
   - The system will automatically generate RSA keys on first run

## 📖 Usage Guide

### First-Time Setup

When you run the application for the first time:

1. The system automatically creates two directories:
   - `cloud_storage/` - Stores encrypted files
   - `keys/` - Stores RSA key pairs

2. RSA-2048 key pair is generated and saved:
   - `keys/private_key.pem` - Private key for decryption
   - `keys/public_key.pem` - Public key for encryption

### Uploading Files

1. **Method 1: Click to Browse**
   - Click the "Choose File" button
   - Select a file from your computer
   - Click "Encrypt & Upload Securely"

2. **Method 2: Drag and Drop**
   - Drag any file onto the upload area
   - Drop the file
   - Click "Encrypt & Upload Securely"

3. **What Happens:**
   - File is encrypted with AES-256
   - AES key is encrypted with RSA-2048
   - Metadata is hidden using steganography
   - Encrypted file is stored securely

### Downloading Files

1. Locate your file in the "Your Encrypted Files" list
2. Click the download button (📥 icon)
3. File is automatically decrypted
4. Original file is downloaded to your computer

### Deleting Files

1. Locate the file you want to delete
2. Click the delete button (🗑️ icon)
3. Confirm deletion in the popup dialog
4. File is permanently removed

### Supported File Types

The system supports the following file types:

- **Documents**: txt, pdf, doc, docx, ppt, pptx, xls, xlsx
- **Images**: png, jpg, jpeg, gif
- **Archives**: zip, rar
- **Media**: mp3, mp4, avi

## 🔧 How It Works

### Detailed Encryption Process

1. **AES Key Generation**
   ```python
   # Generate a random 256-bit (32-byte) AES key
   aes_key = os.urandom(32)
   ```

2. **File Encryption (AES-256-CBC)**
   ```python
   # Generate random IV (Initialization Vector)
   iv = os.urandom(16)
   
   # Apply PKCS7 padding
   padding_length = 16 - (len(data) % 16)
   padded_data = data + bytes([padding_length]) * padding_length
   
   # Encrypt with AES-256 in CBC mode
   cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
   ciphertext = cipher.encryptor().update(padded_data) + finalize()
   ```

3. **Key Protection (RSA-2048-OAEP)**
   ```python
   # Encrypt AES key with RSA public key
   encrypted_key = public_key.encrypt(
       aes_key,
       padding.OAEP(
           mgf=padding.MGF1(algorithm=hashes.SHA256()),
           algorithm=hashes.SHA256(),
           label=None
       )
   )
   ```

4. **Metadata Creation**
   ```python
   metadata = {
       "file_name": "document.pdf",
       "file_id": "unique_identifier",
       "iv": base64_encoded_iv,
       "encrypted_key": base64_encoded_key,
       "original_size": 12345,
       "timestamp": "2026-01-29T10:30:00",
       "version": "2.0",
       "encryption": "AES-256-CBC + RSA-2048"
   }
   ```

5. **Steganography**
   ```python
   # Create steganographic structure
   stego_data = (
       MAGIC_HEADER +              # "STEGO_META_V2"
       struct.pack('>I', meta_len) +  # Metadata length (4 bytes)
       metadata_json +             # JSON metadata
       struct.pack('>I', pad_size) +  # Padding size (4 bytes)
       random_padding +            # Random bytes (32-160 bytes)
       encrypted_file              # Encrypted file content
   )
   ```

### Detailed Decryption Process

1. **Load Steganographic File**
   ```python
   with open(f"{file_id}.stego", "rb") as f:
       stego_data = f.read()
   ```

2. **Extract Metadata**
   ```python
   # Verify magic header
   assert stego_data[:13] == b"STEGO_META_V2"
   
   # Extract metadata length and content
   meta_len = struct.unpack('>I', stego_data[13:17])[0]
   metadata = json.loads(stego_data[17:17+meta_len])
   
   # Skip padding and extract encrypted data
   ```

3. **Decrypt AES Key**
   ```python
   aes_key = private_key.decrypt(
       encrypted_key,
       padding.OAEP(
           mgf=padding.MGF1(algorithm=hashes.SHA256()),
           algorithm=hashes.SHA256(),
           label=None
       )
   )
   ```

4. **Decrypt File**
   ```python
   # Decrypt with AES-256
   cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
   plaintext = cipher.decryptor().update(ciphertext) + finalize()
   
   # Remove PKCS7 padding
   padding_length = plaintext[-1]
   original_data = plaintext[:-padding_length]
   ```

## 📁 Project Structure

```
secure-cloud-storage/
│
├── secure_cloud_storage_enhanced.py  # Main application file
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
│
├── cloud_storage/                     # Encrypted files directory
│   ├── *.stego                       # Steganographic files
│   └── (auto-created on first run)
│
├── keys/                              # RSA keys directory
│   ├── private_key.pem               # RSA private key
│   ├── public_key.pem                # RSA public key
│   └── (auto-created on first run)
│
└── documentation/                     # Additional docs
    ├── Technical_Documentation.docx   # Technical details
    ├── Installation_Guide.pdf         # Setup instructions
    └── User_Manual.pdf                # Usage guide
```

## 🔌 API Reference

### SecureCloudUploader Class

#### Methods

##### `__init__()`
Initialize the uploader and load/generate RSA keys.

##### `upload_file(file_data: bytes, filename: str) -> str`
Encrypt and upload a file.

**Parameters:**
- `file_data`: Raw file content (bytes)
- `filename`: Original filename (string)

**Returns:** 
- `file_id`: Unique identifier for the uploaded file

**Example:**
```python
uploader = SecureCloudUploader()
file_id = uploader.upload_file(data, "document.pdf")
```

##### `download_file(file_id: str) -> tuple`
Download and decrypt a file.

**Parameters:**
- `file_id`: File identifier

**Returns:**
- `(plaintext, filename)`: Decrypted data and original filename

**Example:**
```python
data, name = uploader.download_file("abc123")
```

##### `list_files() -> list`
Get list of all encrypted files.

**Returns:**
- List of dictionaries containing file metadata

**Example:**
```python
files = uploader.list_files()
for file in files:
    print(f"{file['name']} - {file['size']} bytes")
```

##### `delete_file(file_id: str) -> bool`
Delete an encrypted file.

**Parameters:**
- `file_id`: File identifier

**Returns:**
- `True` if successful, `False` otherwise

### Steganography Class

#### Methods

##### `hide_metadata(encrypted_data: bytes, metadata: dict) -> bytes`
Hide metadata within encrypted content.

##### `extract_metadata(stego_data: bytes) -> tuple`
Extract metadata from steganographic data.

**Returns:** 
- `(metadata_dict, encrypted_data)`: Extracted metadata and encrypted content

## 🔐 Security Best Practices

### Key Management

1. **Protect Private Key**
   - Store `private_key.pem` securely
   - Never share or commit to version control
   - Consider using hardware security modules (HSM) for production

2. **Backup Keys**
   - Maintain secure backups of your RSA key pair
   - Without the private key, encrypted files cannot be decrypted

3. **Key Rotation**
   - For production systems, implement key rotation
   - Re-encrypt files periodically with new keys

### File Security

1. **Access Control**
   - Implement user authentication for production
   - Use HTTPS for all communications
   - Add rate limiting to prevent abuse

2. **Storage Security**
   - Ensure `cloud_storage/` directory has appropriate permissions
   - Consider encrypting the entire storage directory at OS level

3. **Secure Deletion**
   - Use secure deletion methods to prevent data recovery
   - Consider implementing file shredding

### Network Security

1. **HTTPS Only**
   - Always use HTTPS in production
   - Obtain and install SSL/TLS certificates

2. **Firewall Configuration**
   - Restrict access to port 5000
   - Use reverse proxy (nginx/Apache) in production

## 🐛 Troubleshooting

### Common Issues

#### Issue: "RSA keys not found"
**Solution:** 
- Let the application generate keys automatically on first run
- Check that `keys/` directory has write permissions

#### Issue: "File too large"
**Solution:**
- Maximum file size is 50 MB
- Increase `MAX_CONTENT_LENGTH` in code if needed
- Consider implementing chunked upload for larger files

#### Issue: "Decryption failed"
**Solution:**
- Ensure you're using the same RSA keys used for encryption
- Check that the encrypted file is not corrupted
- Verify file permissions

#### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Change port in code
app.run(host='0.0.0.0', port=5001)
```

### Debug Mode

Enable debug mode for detailed error messages:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

**Warning:** Never enable debug mode in production!

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Improvement

- User authentication and authorization
- Database integration for metadata
- Multi-user support with individual key pairs
- Cloud storage integration (AWS S3, Azure, etc.)
- File sharing with access control
- Audit logging
- Two-factor authentication
- Password-protected files

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

[Your Name]
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- **Cryptography Library**: Python cryptography developers
- **Flask Framework**: Flask and Werkzeug teams
- **Bootstrap**: Bootstrap UI framework team
- **Font Awesome**: Icon library

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing GitHub Issues
3. Create a new Issue with detailed description
4. Contact the author via email

## 🚀 Future Enhancements

### Planned Features

- [ ] User authentication system
- [ ] Multi-user support
- [ ] File sharing capabilities
- [ ] Cloud storage backend (AWS S3, Azure)
- [ ] Mobile application
- [ ] Browser extension
- [ ] Command-line interface
- [ ] REST API for integration
- [ ] File versioning
- [ ] Audit trail and logging
- [ ] Two-factor authentication
- [ ] Password-protected files
- [ ] Encrypted file search
- [ ] Batch operations
- [ ] File compression before encryption

---

**⚠️ Security Notice:** This application is provided for educational and research purposes. For production use, ensure proper security audits, penetration testing, and compliance with relevant regulations (GDPR, HIPAA, etc.).

**💡 Disclaimer:** While this system implements strong encryption, no system is 100% secure. Always follow security best practices and keep your software updated.

---

<div align="center">
  <strong>Made with ❤️ and 🔒 for secure cloud storage</strong>
</div>
