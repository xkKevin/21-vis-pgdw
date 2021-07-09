FROM grimkirill/r-python:0.0.5

RUN rm -rf /etc/apt/sources.list.d/*.list \
    && sed -i "s@http://deb.debian.org/debian@http://mirrors.aliyun.com/debian@g" /etc/apt/sources.list \
    && apt update \
    && apt -y install python3
RUN R -e "install.packages('dplyr',dependencies=TRUE, repos='https://mirrors.sjtug.sjtu.edu.cn/cran/')"
RUN R -e "install.packages('tidyr',dependencies=TRUE, repos='https://mirrors.sjtug.sjtu.edu.cn/cran/')"
RUN apt install -y python3-pip
COPY dist/requirements.txt /tmp/requirements.txt
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple -r /tmp/requirements.txt --trusted-host mirrors.aliyun.com

WORKDIR /app
COPY dist/data/ /app/data/
COPY dist/src/ /app/backend/

CMD ["python", "backend/app.py"]
