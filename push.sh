git add .
commit_message=read -p "Enter commit msg: "
git commit -a -m "$commit_message"
git push
sudo cp exporter.py /opt/redfish-exporter/ -f
sudo chmod 600 /etc/redfish-exporter/env
