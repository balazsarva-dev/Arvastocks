# ArvaStocks

A comprehensive stock tracking and analysis application with secure HTTPS access.

## Project Overview

ArvaStocks provides financial information and analysis tools for investors. The application offers stock data visualization, tracking capabilities, and market insights through an intuitive web interface.

## Architecture

- **Backend**: Flask Python application
- **Database**: MariaDB
- **Proxy/SSL**: Traefik with Let's Encrypt
- **Deployment**: Docker containerized application

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- Git

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LiZoMark841619/StockApp.git
   cd StockApp

2. **Create a .env file with the following variables**:

   ```properties
   API_KEY=get_an_api_key
   SECRET_KEY=get_a_secret_key
   DB_HOST=db
   DB_PORT=3306
   DB_NAME=your_db_name
   DB_ROOT_PASSWORD=your_root_password
   DB_USER=your_username
   DB_PASSWORD=your_password
   PORT=5000
   ENCRYPT=no
   TRUST_SERVER_CERTIFICATE=no
   MAIL_SERVER=your_email_provider
   MAIL_PORT=your_email_provider_port
   MAIL_USE_TLS=true
   MAIL_USE_SSL=false
   MAIL_USERNAME=your_email_address
   MAIL_PASSWORD=your_password
   MAIL_DEFAULT_SENDER=your_email_address
   MAIL_RECIPIENT=your_email_address
   ```
### Docker initialization

3. **Build the Images**:
    ```bash
    docker-compose build
    ```

4. **Start the Containers**:
    ```bash
    docker-compose up -d
    ```

5. **Access the Application**:
    ```properties
    Open a web browser and navigate to `http://localhost:5000`
