FROM pymesh/pymesh

RUN apt-get update && apt-get install -y zip imagemagick 
RUN pip3 install numpy && pip3 install click scipy numpy stl_tools matplotlib peewee python-dateutil

WORKDIR /code/wab
