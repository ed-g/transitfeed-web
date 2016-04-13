FROM centos
MAINTAINER Ed Groth <info@groth-geodata.com>
RUN yum -y install epel-release
RUN yum -y update 
RUN yum -y install python-pip
# RUN pip install transitfeed
# RUN pip install flask
RUN pip install .
RUN useradd tfeedweb
RUN mkdir /home/tfeedweb/transitfeed-web/

COPY Dockerfile /home/tfeedweb/transitfeed-web/
COPY LICENSE /home/tfeedweb/transitfeed-web/
COPY *.md /home/tfeedweb/transitfeed-web/
COPY *.py  /home/tfeedweb/transitfeed-web/
COPY transitfeed_submodule  /home/tfeedweb/transitfeed-web/transitfeed_submodule

RUN chown -R tfeedweb:tfeedweb /home/tfeedweb
