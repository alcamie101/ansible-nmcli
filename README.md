```
 (c) 2015, Chris Long <alcamie@gmail.com> <chlong@redhat.com>

This file is a module for Ansible that interacts with Network Manager

 Ansible is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Ansible is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Ansible.    If not, see <http://www.gnu.org/licenses/>.
```
Table of Contents
=================

  * [Table of Contents](#table-of-contents)
  * [This documentation is a work in progress.](#this-documentation-is-a-work-in-progress)
  * [Why did I write an Ansible module for NetworkManager?](#why-did-i-write-an-ansible-module-for-networkmanager)
  * [DOCUMENTATION](#documentation)
      * [options](#options)
        * [state](#state)
        * [enabled](#enabled)
        * [action](#action)
        * [cname](#cname)
        * [ifname](#ifname)
        * [type](#type)
        * [mode](#mode)
        * [master](#master)
        * [ip4](#ip4)
        * [gw4](#gw4)
        * [dns4](#dns4)
        * [ip6](#ip6)
        * [gw6](#gw6)
        * [dns6](#dns6)
        * [mtu](#mtu)
 * [bond specific](#bond-specific)
        * [primary](#primary)
        * [miimon](#miimon)
        * [downdelay](#downdelay)
        * [updelay](#updelay)
        * [arp_interval](#arp_interval)
        * [arp_ip_target](#arp_ip_target)
 * [bridge specific](#bridge-specific)
        * [stp](#stp)
        * [priority](#priority)
        * [forwarddelay](#forwarddelay)
        * [hellotime](#hellotime)
        * [maxage](#maxage)
        * [ageingtime](#ageingtime)
        * [mac](#mac)
        * [slavepriority](#slavepriority)
        * [path_cost](#path_cost)
        * [hairpin](#hairpin)
 * [vlan specific](#vlan-specific)
        * [vlanid](#vlanid)
        * [vlandev](#vlandev)
        * [flags](#flags)
        * [ingress](#ingress)
        * [egress](#egress)
  * [EXAMPLES](#examples)
    * [inventory examples](#inventory-examples)
      * [groups_vars](#groups_vars)
      * [host_vars](#host_vars)
    * [playbook-add.yml example](#playbook-addyml-example)
    * [playbook-del.yml example](#playbook-delyml-example)
  * [Exit Statuses](#exit-statuss)

# This documentation is a work in progress. 
I will be trying to document as I code but there might be some instances where the documentation is slightly out of sync. I apologise in advance for that but my attempts to stay synced are closely aligned with me getting the code to a working state. So fingers crossed, it should stay interpretable enough.

# Why did I write an Ansible module for NetworkManager?
 The main reason I started writing this module was because I was building or should I say rebuilding an OpenStack undercloud the N'th time and I was sick of having to write Jinja templates for configuring the interfaces and then write all of the supporting playbook guff to manage deployment and consequent network management shell cmds for one type of interface and then rewrite it again for another type of interface.

 This makes things simple, quick and extremely flexible. E.g. You can build multiple bond interfaces with assorted NIC configurations and deploy them within a couple of minutes. If you're not happy with bonding, you can, in a few seconds, change the configuration to team and team-slaves and redeploy that in a couple of minutes just by changing the 'type'. 
 At the moment, the playbook process here would be:

1. Create bond
2. create bond-slave
3. deploy 'playbook-add.yml'
4. decide you want teams not bonds
5. Remove above connection 'playbook-del.yml' 
6. in 'playbook-add.yml' change bond to team and bond-slave to team-slave
7. deploy 'playbook-add.yml' and voila, you now have teams rather than bonds.
 
> **Warning. Make sure that you do not change your "management NIC" or add it to one of the new connections as you could lose connectivity to your remote machine**

# DOCUMENTATION:

**module:** *nmcli*
**author:** Chris Long  
**short_description:** Manage Networking  
**requirements:** [ nmcli, dbus ]  
**description:**
Manage the network devices. Create, modify, and manage, ethernet, teams, bonds, vlans etc.  
###options:
#### state:
**required:** True  
**default:** "present"  
**choices:** [ present, absent ]  
**description:**
- Whether the device should exist or not, taking action if the state is different from what is stated.  

#### enabled:
**required:** False  
**default:** "yes"  
**choices:** [ "yes", "no" ]  
**description:**
- Whether the service should start on boot. B(At least one of state and enabled are required.)
- Whether the connection profile can be automatically activated ( default: yes)  

#### action:
**required:** False  
**default:** None  
**choices:** [ add, modify, show, up, down ]  
**description:**
- Set to **'add'** if you want to add a connection.
- Set to **'modify'** if you want to modify a connection. Modify one or more properties in the connection profile.
- Set to **'delete'** if you want to delete a connection. Delete a configured connection. The connection to be deleted is identified by its name ***'cfname'***.
- Set to **'show'** if you want to show a connection. Will show all devices unless ***'cfname'*** is set.
- Set to **'up'** if you want to bring a connection up. Requires ***'cfname'*** to be set.
- Set to **'down'** if you want to bring a connection down. Requires ***'cfname'*** to be set.  

#### cname:
**required:** True  
**default:** None  
**description:**
- Where CNAME will be the name used to call the connection. when not provided a default name is generated: <type>[-<ifname>][-<num>]  

#### ifname:
**required:** False  
**default:** cname  
**description:**  
- Where INAME will be the what we call the interface name. Required with ***'up', 'down'*** modifiers.
- interface to bind the connection to. The connection will only be applicable to this interface name.
- A special value of "*" can be used for interface-independent connections.
- The ifname argument is mandatory for all connection types except bond, team, bridge and vlan.  

#### type:
**required:** False  
**default:** None  
**choices:** [ ethernet, team, team-slave, bond, bond-slave, bridge, vlan ]  
**description:**
- This is the type of device or network connection that you wish to create.  

#### mode:
**required:** False  
**choices:** [ "balance-rr", "active-backup", "balance-xor", "broadcast", "802.3ad", "balance-tlb", "balance-alb" ]  
**default:** None  
**description:**
- This is the type of device or network connection that you wish to create for a bond, team or bridge. (NetworkManager default: balance-rr)  

#### master:
**required:** False  
**default:** None  
**description:**
- master <master (ifname, or connection UUID or cname) of bridge, team, bond master connection profile.  

#### ip4:
**required:** False  
**default:** None  
**description:**
- The IPv4 address to this interface using this format ie: "192.168.1.24/24"  

#### gw4:
**required:** False  
**default:** None  
**description:**
- The IPv4 gateway for this interface using this format ie: "192.168.100.1"  

#### dns4:
**required:** False  
**default:** None  
**description:**
- A list of upto 3 dns servers, ipv4 format e.g. To add two IPv4 DNS server addresses: ['"8.8.8.8 8.8.4.4"']  

#### ip6:
**required:** False  
**default:** None  
**description:**
- The IPv6 address to this interface using this format ie: "abbe::cafe"  

#### gw6:
**required:** False  
**default:** None  
**description:**
- The IPv6 gateway for this interface using this format ie: "2001:db8::1"  

#### dns6:
**required:** False  
**default:** None  
**description:**
- A list of upto 3 dns servers, ipv6 format e.g. To add two IPv6 DNS server addresses: ['"2001:4860:4860::8888 2001:4860:4860::8844"']  

#### mtu:
**required:** False  
**default:** None  
**description:**
- The connection MTU, e.g. 9000. This can't be applied when creating the interface and is done once the interface has been created. (NetworkManager default: 1500)
- Can be used when modifying Team, VLAN, Ethernet (Future plans to implement wifi, pppoe, infiniband)  

###***Bond specific***  
___

#### primary:
**required:** False  
**default:** None  
**description:**
- This is only used with bond and is the primary interface name (for "active-backup" mode), this is the usually the 'ifname'  

#### miimon:
**required:** False  
**default:** None  
**description:**
- This is only used with bond - miimon (NetworkManager default: 100)  

#### downdelay:
**required:** False  
**default:** None  
**description:**
- This is only used with bond - downdelay (NetworkManager default: 0)  

#### updelay:
**required:** False  
**default:** None  
**description:**
- This is only used with bond - updelay (NetworkManager default: 0)  

#### arp_interval:
**required:** False  
**default:** None  
**description:**
- This is only used with bond - ARP interval (NetworkManager default: 0)  

#### arp_ip_target:
**required:** False  
**default:** None  
**description:**
- This is only used with bond - ARP IP target  

###***Bridge specific***  
___
#### stp:
**required:** False  
**default:** None  
**description:**
- This is only used with bridge and controls whether Spanning Tree Protocol (STP) is enabled for this bridge  

#### priority:
**required:** False  
**default:** None  
**description:**
- This is only used with bridge - sets STP priority (NetworkManager default: 128)  

#### forwarddelay:
**required:** False  
**default:** None  
**description:**
- This is only used with bridge - [forward-delay <2-30>] STP forwarding delay, in seconds (NetworkManager default: 15)  

#### hellotime:
**required:** False  
**default:** None  
**description:**
- This is only used with bridge - [hello-time <1-10>] STP hello time, in seconds (NetworkManager default: 2)  

#### maxage:
**required:** False  
**default:** None  
**description:**
- This is only used with bridge - [max-age <6-42>] STP maximum message age, in seconds (NetworkManager default: 20)  

#### ageingtime:
**required:** False  
**default:** None  
**description:**
- This is only used with bridge - [ageing-time <0-1000000>] the Ethernet MAC address aging time, in seconds (NetworkManager default: 300)  

#### mac:
**required:** False  
**default:** None  
**description:**
- This is only used with bridge - MAC address of the bridge (note: this requires a recent kernel feature, originally introduced in 3.15 upstream kernel)  

#### slavepriority:
**required:** False  
**default:** None  
**description:**
- This is only used with 'bridge-slave' - [<0-63>] - STP priority of this slave (default: 32)  

#### path_cost:
**required:** False  
**default:** None  
**description:**
- This is only used with 'bridge-slave' - [<1-65535>] - STP port cost for destinations via this slave (NetworkManager default: 100)  

#### hairpin:
**required:** False  
**default:** None  
**description:**
- This is only used with 'bridge-slave' - 'hairpin mode' for the slave, which allows frames to be sent back out through the slave the frame was received on. (NetworkManager default: yes)  

###***VLAN specific***  
___
#### vlanid:
**required:** False  
**default:** None  
**description:**
- This is only used with VLAN - VLAN ID in range <0-4095>  

#### vlandev:
**required:** False  
**default:** None  
**description:**
- This is only used with VLAN - parent device this VLAN is on, can use ifname  

#### flags:
**required:** False  
**default:** None  
**description:**
- This is only used with VLAN - flags  

#### ingress:
**required:** False  
**default:** None  
**description:**
- This is only used with VLAN - VLAN ingress priority mapping  

#### egress:
**required:** False  
**default:** None  
**description:**
- This is only used with VLAN - VLAN egress priority mapping  

# EXAMPLES
The following examples are working examples that I have run in the field. I followed follow the structure:  
```
|_/inventory/cloud-hosts
|           /group_vars/openstack-stage.yml
|           /host_vars/controller-01.openstack.host.com
|           /host_vars/controller-02.openstack.host.com
|_/playbook/library/nmcli.py
|          /playbook-add.yml
|          /playbook-del.yml
```

## inventory examples
### groups_vars
```yml
---
#devops_os_define_network
storage_gw: "192.168.0.254"
external_gw: "10.10.0.254"
tenant_gw: "172.100.0.254"

#Team vars
nmcli_team:
    - {cname: 'tenant', ip4: "{{tenant_ip}}", gw4: "{{tenant_gw}}"}
    - {cname: 'external', ip4: "{{external_ip}}", gw4: "{{external_gw}}"}
    - {cname: 'storage', ip4: "{{storage_ip}}", gw4: "{{storage_gw}}"}
nmcli_team_slave:
    - {cname: 'em1', ifname: 'em1', master: 'tenant'}
    - {cname: 'em2', ifname: 'em2', master: 'tenant'}
    - {cname: 'p2p1', ifname: 'p2p1', master: 'storage'}
    - {cname: 'p2p2', ifname: 'p2p2', master: 'external'}

#bond vars
nmcli_bond:
    - {cname: 'tenant', ip4: "{{tenant_ip}}", gw4: '', mode: 'balance-rr'}
    - {cname: 'external', ip4: "{{external_ip}}", gw4: '', mode: 'balance-rr'}
    - {cname: 'storage', ip4: "{{storage_ip}}", gw4: "{{storage_gw}}", mode: 'balance-rr'}
nmcli_bond_slave:
    - {cname: 'em1', ifname: 'em1', master: 'tenant'}
    - {cname: 'em2', ifname: 'em2', master: 'tenant'}
    - {cname: 'p2p1', ifname: 'p2p1', master: 'storage'}
    - {cname: 'p2p2', ifname: 'p2p2', master: 'external'}

#ethernet vars
nmcli_ethernet:
    - {cname: 'em1', ifname: 'em1', ip4: "{{tenant_ip}}", gw4: "{{tenant_gw}}"}
    - {cname: 'em2', ifname: 'em2', ip4: "{{tenant_ip1}}", gw4: "{{tenant_gw}}"}
    - {cname: 'p2p1', ifname: 'p2p1', ip4: "{{storage_ip}}", gw4: "{{storage_gw}}"}
    - {cname: 'p2p2', ifname: 'p2p2', ip4: "{{external_ip}}", gw4: "{{external_gw}}"}
```

### host_vars
```yml
---
storage_ip: "192.168.160.21/23"
external_ip: "10.10.152.21/21"
tenant_ip: "192.168.200.21/23"
```



## playbook-add.yml example

```yml
---
- hosts: openstack-stage
  remote_user: root
  tasks:

- name: install needed network manager libs
  yum: name={{ item }} state=installed
  with_items:
    - libnm-qt-devel.x86_64
    - nm-connection-editor.x86_64
    - libsemanage-python
    - policycoreutils-python

##### Working with all cloud nodes - Teaming
  - name: try nmcli add team - cname only & ip4 gw4
    nmcli: type=team cname={{item.cname}} ip4={{item.ip4}} gw4={{item.gw4}} state=present
    with_items:
      - "{{nmcli_team}}"

  - name: try nmcli add teams-slave
    nmcli: type=team-slave cname={{item.cname}} ifname={{item.ifname}} master={{item.master}} state=present
    with_items:
      - "{{nmcli_team_slave}}"

###### Working with all cloud nodes - Bonding
#  - name: try nmcli add bond - cname only & ip4 gw4 mode
#    nmcli: type=bond cname={{item.cname}} ip4={{item.ip4}} gw4={{item.gw4}} mode={{item.mode}} state=present
#    with_items:
#      - "{{nmcli_bond}}"
#
#  - name: try nmcli add bond-slave
#    nmcli: type=bond-slave cname={{item.cname}} ifname={{item.ifname}} master={{item.master}} state=present
#    with_items:
#      - "{{nmcli_bond_slave}}"

##### Working with all cloud nodes - Ethernet
#  - name: nmcli add Ethernet - cname only & ip4 gw4
#    nmcli: type=ethernet cname={{item.cname}} ip4={{item.ip4}} gw4={{item.gw4}} state=present
#    with_items:
#      - "{{nmcli_ethernet}}"
```

## playbook-del.yml example

```yml
---
- hosts: openstack-stage
  remote_user: root
  tasks:

  - name: try nmcli del team - multiple
    nmcli: cname={{item.cname}} state=absent
    with_items:
      - { cname: 'em1'}
      - { cname: 'em2'}
      - { cname: 'p1p1'}
      - { cname: 'p1p2'}
      - { cname: 'p2p1'}
      - { cname: 'p2p2'}
      - { cname: 'tenant'}
      - { cname: 'storage'}
      - { cname: 'external'}
      - { cname: 'team-em1'}
      - { cname: 'team-em2'}
      - { cname: 'team-p1p1'}
      - { cname: 'team-p1p2'}
      - { cname: 'team-p2p1'}
      - { cname: 'team-p2p2'}
```

#Exit Status's:
**nmcli exits with status 0 if it succeeds, a value greater than 0 is returned if an error occurs.**  
- **0** Success - indicates the operation succeeded
- **1** Unknown or unspecified error
- **2** Invalid user input, wrong nmcli invocation
- **3** Timeout expired (see --wait option)
- **4** Connection activation failed
- **5** Connection deactivation failed
- **6** Disconnecting device failed
- **7** Connection deletion failed
- **8** NetworkManager is not running
- **9** nmcli and NetworkManager versions mismatch
- **10** Connection, device, or access point does not exist.
