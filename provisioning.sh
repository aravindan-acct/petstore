#! /bin/bash -xe

touch /home/labuser/testfile.txt
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
sudo apt-get -y update
sudo  apt-get -y install php php-mysql mariadb-server git python3 python-pip python3-pip
sudo systemctl enable mariadb
sudo systemctl start  mariadb
sudo mysqladmin -u root password TiUtpgDKlbVJpXpaADrTiSfhkphDznym
sudo mysql -u root --password=TiUtpgDKlbVJpXpaADrTiSfhkphDznym -e "quit"
sudo mysql -u root --password=TiUtpgDKlbVJpXpaADrTiSfhkphDznym  -e  "CREATE DATABASE awsdevdays; CREATE USER  'wafdemodbuser'@'localhost' IDENTIFIED BY 'h6d7GEujNYW06idiNG1qaeuemqZWzZyO';  GRANT ALL ON awsdevdays.* TO  wafdemodbuser@localhost; FLUSH PRIVILEGES;"
export DBUSER=wafdemodbuser
export DBPASSWORD=h6d7GEujNYW06idiNG1qaeuemqZWzZyO
dir=$(pwd)
pip3 install --user -r requirements.txt
pip3 install --user connexion[swagger-ui]
cd $dir/api_server
nohup python3 -m swagger_server &