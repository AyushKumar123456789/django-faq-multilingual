
# Django FAQ Multilingual Project

## Overview

The Django FAQ Multilingual Project is an FAQ management system built with Django. It allows you to:

- **Store FAQs**: Each FAQ includes a question and an answer.
- **Multilingual Support**: The question is stored in English by default, and the project automatically generates translations (e.g., Hindi and Bengali) using the `googletrans` library.
- **Rich Text Editing**: The answer field uses **CKEditor** (a WYSIWYG editor) so that you can easily format your content.
- **REST API**: Provides endpoints to create, retrieve, update, and delete FAQs. The API supports a query parameter (`?lang=`) to return the FAQ question in a specified language.
- **Caching with Redis**: Uses Redis (via `django-redis`) to cache API responses for faster performance.
- **Admin Interface**: Utilize Django’s built-in admin panel to manage FAQ entries.
- **Testing and Code Quality**: Unit tests are written with `pytest` and the project follows PEP8 style guidelines using `flake8`.
- **Docker Support**: (Optional) Dockerfile and docker-compose.yml are provided for containerized deployment.

## Features

- **FAQ Model with Multilingual Fields**: Automatically translates the English question into Hindi and Bengali if no translation is provided.
- **WYSIWYG Editor Integration**: Uses `django-ckeditor` for rich text formatting of the answer.
- **REST API with Language Selection**: API endpoints allow language selection via `?lang=` query parameter.
- **Redis Caching**: API responses are cached in Redis for 5 minutes to improve performance.
- **Comprehensive Testing**: Unit tests written using `pytest` ensure that core functionalities work as expected.
- **Docker and Docker Compose**: Easily deploy the application using Docker.

## Installation

### Prerequisites

- **Windows 10/11** (with WSL recommended) or Docker Desktop installed.
- **WSL (Windows Subsystem for Linux)** installed with Ubuntu.  
- **Python 3.x** installed.
- **Git** installed.

### Using WSL (Recommended)

1. **Enable and Install WSL**:  
   Open PowerShell as Administrator and run:
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   wsl --install

```
   Restart your PC if prompted.

2. **Open Ubuntu in WSL**:  
   Launch Ubuntu from the Start Menu and create your Linux username and password.

3. **Update Packages**:
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

4. **Install Git (if not already installed)**:
   ```bash
   sudo apt-get install git -y
   ```

5. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/django-faq-multilingual.git
   cd django-faq-multilingual
   ```

6. **Set Up a Python Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

7. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *The `requirements.txt` file should list:*
   - Django
   - djangorestframework
   - django-ckeditor
   - redis
   - django-redis
   - googletrans==4.0.0-rc1
   - flake8
   - pytest
   - coverage

8. **Install and Start Redis on WSL**:
   ```bash
   sudo apt-get install redis-server -y
   sudo service redis-server start
   redis-cli ping  # Should output: PONG
   ```

9. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

10. **Create a Superuser for the Admin Interface**:
    ```bash
    python manage.py createsuperuser
    ```

11. **Run the Django Development Server**:
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```
    Open your browser and visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Using Docker (Optional)

1. **Install Docker Desktop** on Windows and ensure WSL 2 integration is enabled.
2. **Build and Run Containers**:
   ```bash
   docker-compose up --build
   ```
3. **Access the Application**:
   - Django app: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Redis runs in its container.

*Note: If using Docker, update the `CACHES` setting in `faq_project/settings.py` to use the service name `redis` (e.g., `"LOCATION": "redis://redis:6379/1"`).*

## Usage

### Admin Interface

- Visit [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).
- Log in using the superuser credentials created earlier.
- Use the admin panel to add, edit, or delete FAQ entries. The **answer** field uses CKEditor for rich text formatting.

### REST API Endpoints

- **List All FAQs (English by Default)**:
  ```
  GET http://127.0.0.1:8000/api/faqs/
  ```
- **List FAQs in a Specific Language** (e.g., Hindi):
  ```
  GET http://127.0.0.1:8000/api/faqs/?lang=hi
  ```
- **Create a New FAQ**:
  ```
  POST http://127.0.0.1:8000/api/faqs/
  ```
  *Example JSON body:*
  ```json
  {
      "question": "What is your return policy?",
      "answer": "<p>You can return items within 30 days of purchase.</p>"
  }
  ```
- **Retrieve, Update, or Delete a Single FAQ**:
  ```
  GET/PUT/PATCH/DELETE http://127.0.0.1:8000/api/faqs/<id>/
  ```

### How Automatic Translation Works

- When a new FAQ is created, if the `question_hi` (Hindi) or `question_bn` (Bengali) fields are empty, the project automatically translates the English question using `googletrans` and saves these translations.
- When fetching FAQs, you can specify the language using the `?lang=` parameter (e.g., `?lang=hi`), and the API will return the corresponding translation if available.

### Caching with Redis

- API responses are cached in Redis for 5 minutes to speed up repeated requests.
- Redis keys are generated dynamically based on the language parameter.

## Testing

### Running Unit Tests

- With your virtual environment activated, run:
  ```bash
  pytest
  ```
- To check test coverage:
  ```bash
  coverage run -m pytest
  coverage report -m
  ```

### Code Linting

- To check for PEP8 compliance, run:
  ```bash
  flake8 .
  ```

## Project Structure

```

django-faq-multilingual/
├── faq_project/             # Main Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py        # Contains caching and app configurations
│   ├── urls.py           # Root URL configurations
│   └── wsgi.py
├── faqs/                  # FAQs app directory
│   ├── __init__.py
│   ├── admin.py         # Admin registration for the FAQ model
│   ├── apps.py
│   ├── models.py        # FAQ model with translations and auto-translation logic
│   ├── serializers.py   # DRF serializers for FAQ data
│   ├── tests.py         # Unit tests for FAQ endpoints
│   ├── urls.py          # URL configurations for the FAQs app
│   └── views.py         # API views with caching logic
├── Dockerfile           # Dockerfile for building the Docker image
├── docker-compose.yml   # Docker Compose file for Django and Redis services
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies list
└── README.md            # This file
```



## Contact

For questions or further information, please contact:  
[Ayush Kumar](mailto:ayushjitendra28@gmail.com)
