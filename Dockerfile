# Use a minimal Python runtime
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the Python script into /app
COPY remove_pdf_security.py .

# Install PyPDF2 and its PyCryptodome dependency
RUN pip install --no-cache-dir PyPDF2 pycryptodome

# When the container runs, execute the script
ENTRYPOINT ["python", "remove_pdf_security.py"]
