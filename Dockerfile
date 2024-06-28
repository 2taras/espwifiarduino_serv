FROM python:3

WORKDIR /code

RUN git clone https://github.com/2taras/espwifiarduino_serv.git /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "80", "--proxy-headers"]

EXPOSE 80
