FROM python:3.12.3
WORKDIR /usr/src
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/
RUN pip install -r requirements.txt
COPY /src/ /usr/src/
CMD python application/main.py