# . ./openrc.sh ; ansible-playbook -i hosts mrc.yml -v
ansible-playbook -i hosts main.yml -v
ansible-playbook -i hosts reset.yml -v