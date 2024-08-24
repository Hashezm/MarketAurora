FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK stopwords
RUN python -c "import nltk; nltk.download('stopwords')"

## Expose port 8000
#EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8000"]
