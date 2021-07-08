FROM python:3.7.11

COPY requirement.txt /tmp/requirement.txt
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple -r /tmp/requirement.txt

WORKDIR /PG4DT
COPY ./ /PG4DT

CMD ["python", "backend/app.py"]
