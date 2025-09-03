# Deployment Guide - Medical Appointment Scheduling AI Agent

## 🚀 Local Development Setup

### Step 1: Environment Setup
```bash
# Clone or download the project files
# Navigate to the project directory

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration
```bash
# Copy environment template
cp .env.template .env

# Edit .env with your actual credentials (optional for basic functionality)
# The system works without external API keys but with limited features
```

### Step 3: Run the Application
```bash
# Test the system
python test_system.py

# Start the Streamlit application
streamlit run main.py
```

## ☁️ Streamlit Cloud Deployment

### Step 1: Prepare Repository
1. Upload all project files to GitHub repository
2. Ensure `requirements.txt` is in the root directory
3. Make sure all CSV files are included

### Step 2: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Connect your GitHub account
3. Select your repository
4. Set main file path: `main.py`
5. Deploy!

### Step 3: Environment Variables (Optional)
In Streamlit Cloud settings, add:
- `EMAIL_ADDRESS`
- `EMAIL_PASSWORD`
- `TWILIO_SID`
- `TWILIO_TOKEN`
- `TWILIO_PHONE`

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
# Build Docker image
docker build -t medical-scheduler .

# Run container
docker run -p 8501:8501 medical-scheduler
```

## 🌐 Heroku Deployment

### Step 1: Prepare Files
Create `Procfile`:
```
web: sh setup.sh && streamlit run main.py
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
```

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set buildpacks
heroku buildpacks:set heroku/python

# Deploy
git push heroku main
```

## 🔧 Production Considerations

### Security
- Use environment variables for all credentials
- Enable HTTPS in production
- Implement proper authentication
- Sanitize all user inputs

### Scalability
- Consider using a proper database (PostgreSQL, MySQL)
- Implement caching for better performance
- Add load balancing for high traffic
- Use Redis for session management

### Monitoring
- Set up application logging
- Monitor system performance
- Track appointment booking metrics
- Implement error alerting

### Backup
- Regular database backups
- Version control for configurations
- Disaster recovery procedures

## 🧪 Testing

### Automated Testing
```bash
# Run system tests
python test_system.py

# Test individual components
python -m pytest tests/  # (if you create test files)
```

### Manual Testing Checklist
- [ ] Patient registration flow
- [ ] Appointment booking process
- [ ] Doctor availability display
- [ ] Email notifications (if configured)
- [ ] Excel report generation
- [ ] Admin panel functionality

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt
```

**Streamlit won't start**
```bash
# Check if streamlit is installed
streamlit --version

# Kill existing streamlit processes
pkill -f streamlit
```

**Data files not found**
- Ensure CSV files are in the same directory as main.py
- Check file permissions

**Email notifications not working**
- Verify email credentials in .env
- Check spam folder
- Enable "Less secure apps" for Gmail (or use app passwords)

### Performance Issues
- Check available memory
- Monitor CPU usage
- Optimize database queries
- Consider data pagination

## 📊 Monitoring & Analytics

### Key Metrics to Track
- Number of appointments booked
- Patient satisfaction ratings
- System uptime
- Response times
- Error rates

### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🔄 Updates and Maintenance

### Regular Tasks
- Update patient database
- Refresh doctor schedules
- Clear old appointment slots
- Update system dependencies
- Review error logs

### Version Control
```bash
# Tag releases
git tag -a v1.0.0 -m "Initial release"

# Keep track of changes
git log --oneline
```

---

**Need Help?**
- Check the README.md for detailed documentation
- Review code comments for implementation details
- Test system components individually
- Ensure all dependencies are properly installed
