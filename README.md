# Introduction 
Backend service of COMP90024 2023 Semester 1 Group 70 written in Django. This service handles connection with CouchDB service, retrieves MapReduce results from the given design document and returns calculated results to the frontend.
# Deployment
Simply run
```bash
cd playbook/deploy
```
will go to the Ansible playbook directory. Then, you may need to specify private key in **hosts** and server address in **group_vars/vars.yml**.  You also need to specify **local_path** variable in **group_vars/vars.yml**. This is important since there is a .py file called trigger.py which is executed when the playbook is executed to reset the Masodon database. 
Type
```bash
./run.sh
```
to start deploying the whole service onto the specified host.
> Note that if those CouchDB databases are already in clustered mode, you must comment the role task in **main.yml** to avoid errors.
# Scale
Change your working directory 
```bash
cd playbook/scale
```
will go to the Ansible scale playbook directory. Then, you may repeat the same steps as mentioned above. Specify private key file in **hosts** and server address in **group_vars/vars.yml**. Type
```bash
ansible-playbook -i hosts master.yml
ansible-playbook -i hosts master.yml
```
will start the instances in the docker swarm mode. Type
```bash
ansible-playbook -i hosts main.yml
```
will deploy two new Mastodon clients onto another two servers called **swarm_workers**.
# Author(s)
Zian Wang
