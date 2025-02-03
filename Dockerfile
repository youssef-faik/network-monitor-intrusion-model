FROM python:3.12

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install -r requirements.txt

# RUN pip install pytest pytest-cov black flake8 ipython

COPY . .

EXPOSE 5000

CMD [ "python" , "app/run.py" ]
