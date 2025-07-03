FROM zauberzeug/nicegui:1.4.22

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .


# Expose the port NiceGUI runs on
EXPOSE 8080

# Set environment variables

ENV PORT=8080

# Run the application
CMD ["python", "main.py"] 