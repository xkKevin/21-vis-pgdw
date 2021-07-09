mv ./backend/useMorpheus.py /root/morpheus/useMorpheus.py
cd /root/morpheus/
nohup python useMorpheus.py &
cd /PG4DT/
python backend/app.py