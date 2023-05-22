# . ./openrc.sh ; ansible-playbook -i hosts mrc.yml -v
ansible-playbook -i hosts reset.yml -vvv
ansible-playbook -i hosts main.yml -vvv