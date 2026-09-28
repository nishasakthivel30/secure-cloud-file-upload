# Installation Guide
## Secure Cloud Storage System

**Version:** 2.0  
**Last Updated:** January 29, 2026

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Checklist](#pre-installation-checklist)
3. [Installation Steps](#installation-steps)
4. [Post-Installation Configuration](#post-installation-configuration)
5. [Verification and Testing](#verification-and-testing)
6. [Troubleshooting](#troubleshooting)
7. [Quick Start Guide](#quick-start-guide)

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|------------|
| **Operating System** | Windows 10, macOS 10.14+, Linux (Ubuntu 18.04+) |
| **Python Version** | Python 3.8 or higher |
| **RAM** | 1 GB available |
| **Storage** | 100 MB free disk space |
| **Network** | Internet connection (for installation only) |
| **Browser** | Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ |

### Recommended Requirements

| Component | Requirement |
|-----------|------------|
| **Operating System** | Windows 11, macOS 12+, Ubuntu 22.04+ |
| **Python Version** | Python 3.11 or higher |
| **RAM** | 2 GB available |
| **Storage** | 500 MB free disk space |
| **CPU** | 2+ cores for better performance |

---

## Pre-Installation Checklist

Before installing, ensure you have:

- [ ] Python 3.8+ installed on your system
- [ ] pip package manager available
- [ ] Administrator/sudo access (if required)
- [ ] Internet connection for downloading packages
- [ ] Antivirus temporarily disabled (if it blocks pip)

### Check Python Installation

**Windows:**
```cmd
python --version
pip --version
```

**Linux/Mac:**
```bash
python3 --version
pip3 --version
```

**Expected Output:**
```
Python 3.8.0 or higher
pip 20.0.0 or higher
```

### Installing Python (If Not Installed)

**Windows:**
1. Download from: https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## Installation Steps

### Step 1: Download the Application

**Option A: Download ZIP File**
1. Download `secure-cloud-storage.zip`
2. Extract to desired location
3. Open terminal/command prompt in extracted folder

**Option B: Clone from Git Repository (if available)**
```bash
git clone <repository-url>
cd secure-cloud-storage
```

### Step 2: Create Virtual Environment

Creating a virtual environment is **highly recommended** to avoid conflicts with other Python packages.

**Windows:**
```cmd
cd secure-cloud-storage
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd secure-cloud-storage
python3 -m venv venv
source venv/bin/activate
```

**Verification:**
Your command prompt should now show `(venv)` at the beginning:
```
(venv) C:\Users\YourName\secure-cloud-storage>
```

### Step 3: Install Dependencies

With virtual environment activated:

```bash
pip install -r requirements.txt
```

**This will install:**
- Flask 3.0.0 (Web framework)
- Werkzeug 3.0.1 (WSGI utilities)
- cryptography 41.0.7 (Cryptographic library)

**Installation Progress:**
```
Collecting Flask==3.0.0
  Downloading Flask-3.0.0...
Installing collected packages: Flask, Werkzeug, cryptography
Successfully installed Flask-3.0.0 Werkzeug-3.0.1 cryptography-41.0.7
```

### Step 4: Verify Installation

Check that all packages are installed correctly:

```bash
pip list
```

**Expected Output:**
```
Package         Version
--------------- -------
Flask           3.0.0
Werkzeug        3.0.1
cryptography    41.0.7
...
```

### Step 5: Run the Application

```bash
python secure_cloud_storage_enhanced.py
```

**Expected Output:**
```
================================================================================
==================== SECURE CLOUD STORAGE SERVER ==============================
================================================================================
🌐 Server URL      : http://localhost:5000
📁 Storage Dir     : C:\...\cloud_storage
🔑 Keys Directory  : C:\...\keys
📦 Max Upload Size : 50.00 MB
--------------------------------------------------------------------------------
🛡️  SECURITY FEATURES
--------------------------------------------------------------------------------
  ✅ AES-256 Encryption       (File Content)
  ✅ RSA-2048 Encryption      (Key Protection)
  ✅ Steganography            (Metadata Concealment)
  ✅ Unique Keys Per File     (Maximum Security)
  ✅ CBC Mode with Random IV  (Cryptographic Best Practice)
================================================================================
⚡ Server is running! Press Ctrl+C to stop
================================================================================
```

### Step 6: Access the Application

1. Open your web browser
2. Navigate to: **http://localhost:5000**
3. You should see the Secure Cloud Storage interface

**First Run:**
- The application will automatically create `cloud_storage/` and `keys/` directories
- RSA-2048 key pair will be generated
- Private and public keys will be saved in `keys/` directory

---

## Post-Installation Configuration

### Security Configuration

#### 1. Protect RSA Private Key

**Windows:**
```cmd
icacls keys\private_key.pem /inheritance:r
icacls keys\private_key.pem /grant:r "%USERNAME%:(R)"
```

**Linux/Mac:**
```bash
chmod 600 keys/private_key.pem
chmod 644 keys/public_key.pem
```

#### 2. Backup RSA Keys

**Create encrypted backup:**

```bash
# Create backup directory
mkdir key_backups

# Copy keys to backup
cp keys/private_key.pem key_backups/
cp keys/public_key.pem key_backups/

# Compress and encrypt (example using 7zip)
7z a -p key_backups.7z key_backups/
```

**⚠️ CRITICAL:** Store backup in a secure location. Without the private key, encrypted files cannot be decrypted!

#### 3. Configure File Size Limit (Optional)

Edit `secure_cloud_storage_enhanced.py`:

```python
# Change from 50 MB to desired size (in bytes)
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
```

#### 4. Configure Allowed File Types (Optional)

Edit `secure_cloud_storage_enhanced.py`:

```python
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
    'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar',
    'mp3', 'mp4', 'avi', 'ppt', 'pptx',
    # Add more extensions as needed
}
```

### Performance Optimization

#### For Large Files

1. Increase chunk size for better performance
2. Consider implementing streaming upload/download
3. Use SSD for storage directory

#### For Multiple Users

1. Use production server (Gunicorn)
2. Implement caching
3. Use database for file metadata

---

## Verification and Testing

### Test 1: Upload a File

1. Open http://localhost:5000
2. Click "Choose File" or drag-and-drop a test file
3. Click "Encrypt & Upload Securely"
4. Check for success message: "✅ File uploaded successfully!"

### Test 2: Download and Verify

1. Click the download button (📥) for your uploaded file
2. Open the downloaded file
3. Verify it matches the original

### Test 3: Check Encryption

1. Navigate to `cloud_storage/` directory
2. Open any `.stego` file with a text editor
3. Verify the content is encrypted (unreadable binary data)

### Test 4: Verify Steganography

1. Check file size of `.stego` file
2. It should be slightly larger than original (metadata overhead)
3. No separate `.meta` files should exist

### Test 5: Delete a File

1. Click the delete button (🗑️) for a file
2. Confirm deletion
3. Verify file is removed from list
4. Check that `.stego` file is deleted from `cloud_storage/`

---

## Troubleshooting

### Issue 1: "Python is not recognized"

**Problem:** Python not in system PATH

**Solution:**
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to PATH:
   - Windows: Search "Environment Variables" → Edit PATH → Add Python directory
   - Linux/Mac: Add to ~/.bashrc or ~/.zshrc: `export PATH=$PATH:/usr/local/bin/python3`

### Issue 2: "pip install" fails

**Problem:** Network issues or permissions

**Solution:**
```bash
# Try with --user flag
pip install --user -r requirements.txt

# Or use pip3 (Linux/Mac)
pip3 install -r requirements.txt

# Update pip first
python -m pip install --upgrade pip
```

### Issue 3: "Port 5000 already in use"

**Problem:** Another application using port 5000

**Solution:**
```python
# Edit secure_cloud_storage_enhanced.py
# Change port number (line 1650)
app.run(host='0.0.0.0', port=5001)  # Use 5001 instead
```

**Or kill process using port 5000:**

**Windows:**
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

### Issue 4: "Module not found: cryptography"

**Problem:** Dependency not installed

**Solution:**
```bash
# Install manually
pip install cryptography==41.0.7

# Or reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 5: "Permission denied" (Linux/Mac)

**Problem:** Insufficient permissions

**Solution:**
```bash
# Give execute permission
chmod +x secure_cloud_storage_enhanced.py

# Or run with sudo (not recommended)
sudo python3 secure_cloud_storage_enhanced.py
```

### Issue 6: Browser shows "Connection refused"

**Problem:** Server not running or wrong URL

**Solution:**
1. Check server is running (should see server info in terminal)
2. Verify URL: http://localhost:5000
3. Try http://127.0.0.1:5000
4. Check firewall isn't blocking port 5000

### Issue 7: File upload fails

**Problem:** File too large or wrong format

**Solution:**
1. Check file size (max 50 MB by default)
2. Verify file type is in ALLOWED_EXTENSIONS
3. Check disk space in cloud_storage/ directory

### Issue 8: "RSA key generation failed"

**Problem:** Insufficient permissions or disk space

**Solution:**
1. Check write permissions for keys/ directory
2. Verify sufficient disk space (at least 10 MB)
3. Run as administrator/sudo (if necessary)

---

## Quick Start Guide

### 5-Minute Quick Start

1. **Install Python 3.8+** (if not already installed)

2. **Download and extract** the application

3. **Open terminal** in application directory

4. **Create virtual environment:**
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run application:**
   ```bash
   python secure_cloud_storage_enhanced.py
   ```

7. **Open browser:** http://localhost:5000

8. **Upload your first file:**
   - Drag and drop a file
   - Click "Encrypt & Upload Securely"

9. **Download and verify:**
   - Click download button
   - Open file to verify it's correct

10. **Done!** Your files are now encrypted with AES-256 + RSA-2048 + Steganography

### Usage Tips

1. **Keep your RSA keys safe** - backup `keys/` directory
2. **Monitor disk space** - encrypted files need storage
3. **Use strong passwords** - if implementing authentication
4. **Regular backups** - backup both keys and encrypted files
5. **HTTPS in production** - always use HTTPS for production deployment

---

## Next Steps

### For Development

1. **Read Technical Documentation:** Understand the architecture
2. **Explore the Code:** Review `secure_cloud_storage_enhanced.py`
3. **Customize Settings:** Adjust file size limits, allowed extensions
4. **Add Features:** Implement authentication, multi-user support

### For Production

1. **Setup HTTPS:** Obtain SSL certificate
2. **Use Production Server:** Deploy with Gunicorn/uWSGI
3. **Configure Reverse Proxy:** Setup nginx or Apache
4. **Implement Monitoring:** Add logging and monitoring
5. **Security Audit:** Conduct penetration testing
6. **Regular Updates:** Keep dependencies up to date

### Learning Resources

- **Technical Documentation:** Read TECHNICAL_DOCUMENTATION.md
- **README:** See README.md for detailed features
- **Python Cryptography:** https://cryptography.io/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **OWASP Security:** https://owasp.org/

---

## Support and Community

### Getting Help

1. **Check Documentation:** README.md, TECHNICAL_DOCUMENTATION.md
2. **Review Troubleshooting:** See troubleshooting section above
3. **Search Issues:** Check existing GitHub issues (if available)
4. **Create Issue:** Report bugs or request features

### Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Submit pull request

### Contact

- **Email:** [your-email@example.com]
- **GitHub:** [your-github-username]
- **Website:** [your-website.com]

---

## Appendix: Command Reference

### Virtual Environment Commands

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Deactivate
deactivate
```

### Package Management

```bash
# Install all dependencies
pip install -r requirements.txt

# Install specific package
pip install package-name

# Update package
pip install --upgrade package-name

# List installed packages
pip list

# Show package info
pip show package-name
```

### Application Commands

```bash
# Run application
python secure_cloud_storage_enhanced.py

# Run with specific port
# (Edit code: app.run(host='0.0.0.0', port=5001))

# Stop server
# Press Ctrl+C in terminal
```

### File Operations

```bash
# Check file structure
ls -la  # Linux/Mac
dir     # Windows

# Create directory
mkdir directory-name

# Remove directory
rm -rf directory-name  # Linux/Mac (be careful!)
rmdir /s directory-name  # Windows

# Copy files
cp source dest  # Linux/Mac
copy source dest  # Windows

# Move files
mv source dest  # Linux/Mac
move source dest  # Windows
```

---

**Installation Guide Version:** 1.0  
**Last Updated:** January 29, 2026  
**Status:** Complete

---

*For additional help, please refer to README.md or TECHNICAL_DOCUMENTATION.md*
