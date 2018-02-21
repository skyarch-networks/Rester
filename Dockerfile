FROM python:2.7
RUN pip install git+https://github.com/skyarch-networks/Rester.git@master
ADD rester/examples examples
