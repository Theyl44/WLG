FROM python:3.9-alpine3.15

WORKDIR /usr/src/wlg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python3", "./server.py"] 