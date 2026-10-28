git add .
read -p "Enter commit msg: " commit_message
git commit -m "$commit_message"
git push
sudo cp exporter.py /opt/redfish-exporter/exporter.py -f
sudo chmod 600 /etc/redfish-exporter/env
