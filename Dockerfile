FROM python:3

RUN pip install --upgrade pip && \
    pip install --no-cache-dir pymysql \
    pip install --no-cache-dir meross_iot==0.4.0.3 \
    pip install --no-cache-dir paho-mqtt==1.5.0
