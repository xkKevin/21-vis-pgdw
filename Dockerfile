FROM registry.zjvis.org/xiongkai/pgdw:Somnus_Morpheus
# FROM python:3.7

WORKDIR /PG4DT
COPY ./ /PG4DT

expose 80

COPY ./backend/useMorpheus.py /root/morpheus/useMorpheus.py

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Flask-Cors pandas requests
# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask

# RUN nohup python /root/morpheus/useMorpheus.py &
RUN echo 'nohup python /root/morpheus/useMorpheus.py &' >> start.sh \
    && echo 'python backend/app.py' >> start.sh \
    && chmod 777 start.sh

CMD ["bash", "start.sh"]
