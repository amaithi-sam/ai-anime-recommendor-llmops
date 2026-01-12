# 1. Base Image - 3.12-slim provides a good balance of size and compatibility
FROM python:3.12-slim

# 2. Set Poetry 2.0 & Python Environment Variables
# POETRY_VIRTUALENVS_CREATE=false is mandatory to install globally in Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.0.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 
# POETRY_CACHE_DIR='/tmp/poetry_cache'

# 3. Work Directory
WORKDIR /app

# 4. Install System Dependencies
# libgomp1: Required by FAISS and Sentence-Transformers for parallel processing.
# sqlite3: Required by ChromaDB (needs version >= 3.35.0, which 3.12-slim provides).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    # libgomp1 \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Poetry 2.0
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# 6. Copy ONLY Poetry Files (Caching Strategy)
# This layer stays cached unless you change your dependencies.
COPY pyproject.toml poetry.lock* ./

# 7. Install Dependencies
# Poetry 2.0 automatically reads the [project] table you provided.
# RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR
RUN poetry install --only main --no-root --no-cache

# 8. Copy Application Source Code
# Done after installation so small code changes don't trigger re-installs.
COPY . .

# 9. Expose Streamlit Port
EXPOSE 8501

# 10. Run the App
# Using 'python -m streamlit' fixes the 'ModuleNotFoundError' for your 'src' folder.
CMD ["python", "-m", "streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]