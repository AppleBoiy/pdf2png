# PDF to PNG Converter

A Flask app to upload PDFs, convert them to PNG images, and download the images.

![Screenshot](/public/screenshots/2.png)

## Quick Start

1. **Clone the repo** and navigate to the directory.
2. **Set up a virtual environment** and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Create `uploads` and `converted` folders**.
4. **Run the app**:
   ```bash
   python app.py
   ```

Access the app at `http://127.0.0.1:5000/`.

## Endpoints

- **`GET /upload`**: Shows upload page.
- **`POST /conv`**: Upload and convert PDFs.
- **`GET /img/<hash>/<page>.png`**: Download converted PNG images.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
