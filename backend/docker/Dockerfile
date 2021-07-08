FROM r-base:4.1.0

RUN rm -rf /etc/apt/sources.list.d/*.list \
    && sed -i "s@http://deb.debian.org/debian@http://mirrors.aliyun.com/debian@g" /etc/apt/sources.list \
    && apt update \
    && apt -y install python3
RUN R -e "install.packages('dplyr',dependencies=TRUE, repos='https://mirrors.sjtug.sjtu.edu.cn/cran/')"
RUN R -e "install.packages('tidyr',dependencies=TRUE, repos='https://mirrors.sjtug.sjtu.edu.cn/cran/')"
COPY requirement.txt /tmp/requirement.txt
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple -r /tmp/requirement.txt

WORKDIR /PG4DT
COPY dist/ /PG4DT/

CMD ["python", "backend/app.py"]
