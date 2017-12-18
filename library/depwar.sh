#!/bin/bash
source $1

if [ [ -z $username ] || [ -z $password ] || [ -z $war ] || [ -z $url ] ]; then
	printf '{"failed": true, "msg": "Not all varibles defened! Need 4 variables!"}'
        exit 1
fi


curl -v --user $username:$password --upload-file /vagrant/target/mnt-exam.war "http://127.0.0.1:8080/manager/text/deploy?path=/$url&update=true" 2&>1

 
sudo mkdir -p /var/lib/tomcat/webapps/
sudo touch /var/lib/tomcat/webapps/deploy-info.txt
sudo chmod 0777 /var/lib/tomcat/webapps/deploy-info.txt
sudo echo `date` >> /var/lib/tomcat/webapps/deploy-info.txt
sudo echo `whoami` >> /var/lib/tomcat/webapps/deploy-info.txt



cat <<EOF
{
  "time": "$(date +'%Y-%m-%d %T')"
}
EOF
