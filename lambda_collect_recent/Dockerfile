FROM amazonlinux:2018.03
RUN yum update -y
RUN yum install -y \
    gcc \
    openssl-devel \
    zlib-devel \
    libffi-devel \
    wget && \
    yum -y clean all

WORKDIR usr/src
# Install Python 3.7
RUN wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
RUN tar xzf Python-3.7.4.tgz
RUN cd Python-3.7.4 ; ./configure --enable-optimizations; make altinstall
RUN rm Python-3.7.4.tgz
RUN rm -rf Python-3.7.4
RUN python3.7 -V
# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.7 get-pip.py
RUN rm get-pip.py
RUN pip -V

# RUN yum -y install python-devel mysql-devel
# RUN yum -y install python3-devel

# COPY requirements.txt .
# ENV PKG_CONFIG_PATH=/usr/local/lib64/pkgconfig/:$PKG_CONFIG_PATH

# RUN pip install -t ./lib mysqlclient

# RUN pip install -t ./lib -r requirements.txt
