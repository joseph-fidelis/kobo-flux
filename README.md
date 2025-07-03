# Kobo Flux Form Uploader

A web application for uploading CSV/Excel files to Kobo Toolbox forms. Built with NiceGUI for a modern, responsive interface.

## Features

- 📊 **File Upload**: Support for CSV, Excel (.xlsx, .xls) files
- 🔐 **Kobo API Integration**: Direct upload to Kobo Toolbox forms
- 📋 **Form Management**: Browse and select available Kobo forms
- 📈 **Progress Tracking**: Real-time upload progress with progress bar
- 📝 **Logging**: Comprehensive logging of upload success/failure
- 🎨 **Modern UI**: Dark mode interface with responsive design
- 📁 **File Management**: Automatic file processing and temporary storage

## Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Kobo Toolbox API credentials

## Environment Variables

Create a `.env` file in the project root:

```bash
BASE_URL=https://kc.kobotoolbox.org
API_TOKEN=your_kobo_api_token_here
```

## Local Development

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

The application will be available at `http://localhost:8080`

## Docker Deployment

### Building the Docker Image

```bash
# Build the image
docker build -t fidelis/koboFlux:latest .

# Verify the image was created
docker images fidelis/koboFlux:latest
```

### Running with Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Running with Docker Directly

```bash
# Run the container
docker run -d \
  --name kobo-flux \
  -p 81:8080 \
  -e BASE_URL="your_base_url" \
  -e API_TOKEN=your_api_token \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/tmp:/app/tmp \
  fidelis/koboFlux:latest


## Project Structure

kobo-tanzania/
├── main.py              # Main application entry point
├── kobo_api.py          # Kobo API integration
├── file_processor.py    # File processing utilities
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker build exclusions
├── .env               # Environment variables (create this)
├── logs/              # Upload logs (auto-created)
└── tmp/               # Temporary files (auto-created)


## Usage

### 1. Access the Application

Navigate to `http://localhost:81` (or `http://localhost:8080` for local development)

### 2. Select a Form

- Browse available Kobo forms
- Click on a form to select it for upload

### 3. Upload Data

- Upload a CSV or Excel file
- Preview the data in the table
- Click "Upload File" to submit to Kobo
- Monitor progress with the progress bar
- View real-time logs

### 4. Download Logs

- Click "Download Log" to get the upload log file
- Logs are saved in the `logs/` directory

## API Endpoints

- `/` - Forms listing page
- `/upload/` - File upload page (requires form_id and form_title parameters)

## File Formats Supported

- **CSV**: Comma-separated values
- **Excel**: .xlsx and .xls files
- **Data Structure**: Must match the selected Kobo form fields

## Troubleshooting

### DNS Resolution Issues

If you encounter DNS resolution errors in Docker:

1. Add DNS configuration to `docker-compose.yml`:
```yaml
dns:
  - 8.8.8.8
  - 8.8.4.4
```

2. Or use host networking:
```yaml
network_mode: host
```

### Permission Issues

Ensure the `logs/` and `tmp/` directories have proper permissions:

```bash
mkdir -p logs tmp
chmod 755 logs tmp
```

### API Token Issues

- Verify your API token is correct
- Ensure the token has proper permissions for the forms
- Check the BASE_URL is accessible

## Development

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Add type hints where appropriate
- Include docstrings for functions and classes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the logs in the `logs/` directory
- Create an issue in the repository

## Changelog

### v1.0.0
- Initial release
- File upload functionality
- Kobo API integration
- Progress tracking
- Logging system
- Docker support