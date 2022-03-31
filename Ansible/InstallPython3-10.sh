set -e

sudo yum update -y
sudo yum groupinstall "Development Tools" -y
sudo yum install openssl11-devel libffi-devel bzip2-devel wget -y

wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar -xf Python-3.10.0.tgz
cd Python-3.10.0

sudo ./configure --enable-optimizations
sudo make -j $(nproc)
sudo make install
