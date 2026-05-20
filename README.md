[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12


$url = "https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"


Invoke-Expression ((New-Object System.Net.WebClient).DownloadString($url))




# 🚀 Infrastructure Automation Manual: EDR Agent Deployment

**Architecture Overview:**
This setup uses an Ubuntu Server as an **Ansible Control Node** to automatically pull Python EDR agent code from a private GitLab repository and deploy it to multiple **Windows Client VMs** over the network. It is configured to run automatically every hour via a cron job, ensuring all Windows machines are always running the latest version of the code.

# 1. Enable the WinRM service to allow Ansible connections
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $url = "https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString($url))

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $url = "https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString($url))

# 2. Set the Administrator password to 'user'
net user Administrator user

# 3. Activate the built-in Administrator account so network logins are permitted
net user Administrator /active:yes

apt update && apt install python3-winrm ansible git -y

mkdir -p /root/edr-automation
cd /root/edr-automation

nano inventory.ini

[windows]
192.168.100.84
192.168.100.88
192.168.100.162

[windows:vars]
ansible_user=Administrator
ansible_password=user
ansible_connection=winrm
ansible_winrm_server_cert_validation=ignore

nano deploy_agent.yml

---
- name: Fetch and Deploy EDR Python Agent from GitLab
  hosts: all
  gather_facts: false

  vars:
    # 1. Generate a "Deploy Token" in GitLab (Settings -> Repository -> Deploy Tokens)
    gitlab_user: "YOUR_DEPLOY_TOKEN_USERNAME"
    gitlab_token: "YOUR_DEPLOY_TOKEN_STRING"
    # 2. Add your repo URL (Do NOT include https:// at the beginning!)
    gitlab_repo_url: "git.fiw.thws.de/k60644/swprojekt.git" 

  tasks:
    - name: Pull latest agent code from GitLab Private Repository
      delegate_to: localhost
      ansible.builtin.git:
        repo: "https://{{ gitlab_user | urlencode }}:{{ gitlab_token | urlencode }}@{{ gitlab_repo_url }}"
        dest: /root/edr-automation/downloads/
        # 3. CHANGE THE BRANCH HERE! (e.g., main, dev, detection-protocol-analysis)
        version: detection-protocol-analysis
        force: yes 
      run_once: true

    - name: Create the EDR Agent directory on Windows
      ansible.windows.win_file:
        path: C:\EDR_Agent
        state: directory

    - name: Copy the entire EDR agent backend to Windows
      ansible.windows.win_copy:
        # 4. Ensure this path perfectly matches your repository's internal folder structure!
        src: /root/edr-automation/downloads/src/backend/app/
        dest: C:\EDR_Agent\

ansible-playbook -i inventory.ini deploy_agent.yml

crontab -e

0 * * * * cd /root/edr-automation && /usr/bin/ansible-playbook -i inventory.ini deploy_agent.yml >> /var/log/edr-deployment.log 2>&1

cat /var/log/edr-deployment.log

nano /root/edr-automation/deploy_agent.yml

    - name: Pull latest agent code from GitLab Private Repository
      delegate_to: localhost
      ansible.builtin.git:
        repo: "https://{{ gitlab_user | urlencode }}:{{ gitlab_token | urlencode }}@{{ gitlab_repo_url }}"
        dest: /root/edr-automation/downloads/
        version: detection-protocol-analysis  # <-- THIS IS THE LINE!
        force: yes 

        version: main

cd /root/edr-automation && ansible-playbook -i inventory.ini deploy_agent.yml











import requests

class BackendClient:
    def __init__(self, base_url="http://192.168.100.88:8000/api/ingest/json/Client_84"):
        self.base_url = base_url

    def send_log(self, event_dict: dict):
        """Blind-fires the raw log dictionary to the server"""
        try:
            response = requests.post(self.base_url, json=event_dict, timeout=3)
            print(f"[+] Log sent! Server replied: {response.status_code}")
        except Exception as e:
            print(f"[-] Failed to route to backend: {e}")

