FROM registry.zjvis.org/xiongkai/pgdw:Somnus_Morpheus
# FROM python:3.7

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Flask-Cors pandas requests
# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask

WORKDIR /PG4DT
COPY ./ /PG4DT

# expose 80

# COPY ./backend/useMorpheus.py /root/morpheus/useMorpheus.py

# RUN nohup python /root/morpheus/useMorpheus.py &
RUN chmod 777 start.sh

CMD ["bash", "start.sh"]
