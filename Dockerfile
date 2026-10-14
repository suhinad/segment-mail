
FROM python:3.9-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Системні залежності та інструменти для додавання репозиторію
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    gnupg \
    curl \
    ca-certificates \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Додаємо ключ Microsoft без застарілого apt-key
RUN install -d -m 0755 /etc/apt/keyrings && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg && \
    chmod a+r /etc/apt/keyrings/microsoft.gpg

# Репозиторій Microsoft для Debian 12 (Bookworm)
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/microsoft-prod.list

# Встановлюємо Microsoft ODBC Driver 17 та MSSQL Tools
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql17 \
        mssql-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/opt/mssql-tools/bin"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
