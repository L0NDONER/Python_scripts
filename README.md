Ansible Desktop Configuration
This repository contains an Ansible configuration file to simplify the process of updating multiple computers. By using this configuration, you can easily manage updates for your desktops and laptops in a centralized manner.

Overview
This README provides step-by-step instructions on how to use the Ansible configuration file to update all of your computers.

Requirements
Ansible: Ensure Ansible is installed on your system.
Inventory file: Create an inventory file that lists the computers you want to update.
Getting Started

pip install ansible

Create Inventory File:


<pre>
```ini
[all]
localhost

[desktops]
desktop1
desktop2

[laptops]
laptop1
laptop2
```
</pre>
# update.yml
<pre>
---
- hosts: all
  become: yes

  tasks:
    - name: Update all packages
      apt:
        update_cache: yes
        upgrade: yes

  handlers:
    - name: Clean up
      file:
        state: absent
        path: /var/cache/apt/archives/_
</pre>
