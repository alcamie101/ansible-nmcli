# (c) 2015, Chris Long <alcamie@gmail.com> <chlong@redhat.com>
#
# This file is a module for Ansible that interacts with Network Manager
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.    If not, see <http://www.gnu.org/licenses/>.


DOCUMENTATION='''
---
module: nmcli
author: Chris Long
short_description: Manage Networking
requirements: [ nmcli, dbus ]
description:
    - Manage the network devices. Create, modify, and manage, ethernet, teams, bonds, vlans etc.
options:
    state:
        required: True
        default: "present"
        choices: [ present, absent ]
    description:
        - Whether the device should exist or not, taking action if the state is different from what is stated.
    enabled:
        required: False
        default: "yes"
        choices: [ "yes", "no" ]
        description:
            - Whether the service should start on boot. B(At least one of state and enabled are required.)
            - Whether the connection profile can be automatically activated ( default: yes)
    action:
        required: False
        default: None
        choices: [ add, modify, show, up, down ]
        description:
            - Set to 'add' if you want to add a connection.
            - Set to 'modify' if you want to modify a connection. Modify one or more properties in the connection profile.
            - Set to 'delete' if you want to delete a connection. Delete a configured connection. The connection to be deleted is identified by its name 'cfname'.
            - Set to 'show' if you want to show a connection. Will show all devices unless 'cfname' is set.
            - Set to 'up' if you want to bring a connection up. Requires 'cfname' to be set.
            - Set to 'down' if you want to bring a connection down. Requires 'cfname' to be set.
    cname:
        required: True
        default: None
        description:
            - Where CNAME will be the name used to call the connection. when not provided a default name is generated: <type>[-<ifname>][-<num>]
    ifname:
        required: False
        default: cname
        description:
            - Where INAME will be the what we call the interface name. Required with 'up', 'down' modifiers.
            - interface to bind the connection to. The connection will only be applicable to this interface name.
            - A special value of "*" can be used for interface-independent connections.
            - The ifname argument is mandatory for all connection types except bond, team, bridge and vlan.
    type:
        required: False
        choices: [ ethernet, team, team-slave, bond, bond-slave, bridge, vlan ]
        description:
            - This is the type of device or network connection that you wish to create.
    mode:
        required: False
        choices: [ "balance-rr", "active-backup", "balance-xor", "broadcast", "802.3ad", "balance-tlb", "balance-alb" ]
        default: None
        description:
            - This is the type of device or network connection that you wish to create for a bond, team or bridge. (NetworkManager default: balance-rr)
    master:
        required: False
        default: None
        description:
            - master <master (ifname, or connection UUID or cname) of bridge, team, bond master connection profile.
    ip4:
        required: False
        default: None
        description: The IPv4 address to this interface using this format ie: "192.168.1.24/24"
    gw4:
        required: False
        description: The IPv4 gateway for this interface using this format ie: "192.168.100.1"
    dns4:
        required: False
        default: None
        description: A list of upto 3 dns servers, ipv4 format e.g. To add two IPv4 DNS server addresses: ['"8.8.8.8 8.8.4.4"']
    ip6:
        required: False
        default: None
        description:
            - The IPv6 address to this interface using this format ie: "abbe::cafe"
    gw6:
        required: False
        default: None
        description: The IPv6 gateway for this interface using this format ie: "2001:db8::1"
    dns6:
        required: False
        description: A list of upto 3 dns servers, ipv6 format e.g. To add two IPv6 DNS server addresses: ['"2001:4860:4860::8888 2001:4860:4860::8844"']
    mtu:
        required: False
        default: None
        description:
            - The connection MTU, e.g. 9000. This can't be applied when creating the interface and is done once the interface has been created. (NetworkManager default: 1500)
            - Can be used when modifying Team, VLAN, Ethernet (Future plans to implement wifi, pppoe, infiniband)
    primary:
        required: False
        default: None
        description:
            - This is only used with bond and is the primary interface name (for "active-backup" mode), this is the usually the 'ifname'
    miimon:
        required: False
        default: None
        description:
            - This is only used with bond - miimon (NetworkManager default: 100)
    downdelay:
        required: False
        default: None
        description:
            - This is only used with bond - downdelay (NetworkManager default: 0)
    updelay:
        required: False
        default: None
        description:
            - This is only used with bond - updelay (NetworkManager default: 0)
    arp_interval:
        required: False
        default: None
        description:
            - This is only used with bond - ARP interval (NetworkManager default: 0)
    arp_ip_target:
        required: False
        default: None
        description:
            - This is only used with bond - ARP IP target
    stp:
        required: False
        default: None
        description:
            - This is only used with bridge and controls whether Spanning Tree Protocol (STP) is enabled for this bridge
    priority:
        required: False
        default: None
        description:
            - This is only used with 'bridge' - sets STP priority (NetworkManager default: 128)
    forwarddelay:
        required: False
        default: None
        description:
            - This is only used with bridge - [forward-delay <2-30>] STP forwarding delay, in seconds (NetworkManager default: 15)
    hellotime:
        required: False
        default: None
        description:
            - This is only used with bridge - [hello-time <1-10>] STP hello time, in seconds (NetworkManager default: 2)
    maxage:
        required: False
        default: None
        description:
            - This is only used with bridge - [max-age <6-42>] STP maximum message age, in seconds (NetworkManager default: 20)
    ageingtime:
        required: False
        default: None
        description:
            - This is only used with bridge - [ageing-time <0-1000000>] the Ethernet MAC address aging time, in seconds (NetworkManager default: 300)
    mac:
        required: False
        default: None
        description:
            - This is only used with bridge - MAC address of the bridge (note: this requires a recent kernel feature, originally introduced in 3.15 upstream kernel)
    slavepriority:
        required: False
        default: None
        description:
            - This is only used with 'bridge-slave' - [<0-63>] - STP priority of this slave (default: 32)
    path_cost:
        required: False
        default: None
        description:
            - This is only used with 'bridge-slave' - [<1-65535>] - STP port cost for destinations via this slave (NetworkManager default: 100)
    hairpin:
        required: False
        default: None
        description:
            - This is only used with 'bridge-slave' - 'hairpin mode' for the slave, which allows frames to be sent back out through the slave the frame was received on. (NetworkManager default: yes)
    vlanid:
        required: False
        default: None
        description:
            - This is only used with VLAN - VLAN ID in range <0-4095>
    vlandev:
        required: False
        default: None
        description:
            - This is only used with VLAN - parent device this VLAN is on, can use ifname
    flags:
        required: False
        default: None
        description:
            - This is only used with VLAN - flags
    ingress:
        required: False
        default: None
        description:
            - This is only used with VLAN - VLAN ingress priority mapping
    egress:
        required: False
        default: None
        description:
            - This is only used with VLAN - VLAN egress priority mapping

'''

EXAMPLES='''
# To add an Ethernet connection with static IP configuration, issue a command as follows
- nmcli: name=add cname=my-eth1 ifname=eth1 type=ethernet ip4=192.168.100.100/24 gw4=192.168.100.1 state=present

# To add an Team connection with static IP configuration, issue a command as follows
- nmcli: name=add cname=my-team1 ifname=my-team1 type=team ip4=192.168.100.100/24 gw4=192.168.100.1 state=present enabled=yes

# Optionally, at the same time specify IPv6 addresses for the device as follows:
- nmcli: name=add cname=my-eth1 ifname=eth1 type=ethernet ip4=192.168.100.100/24 gw4=192.168.100.1 ip6=abbe::cafe gw6=2001:db8::1 state=present

# To add two IPv4 DNS server addresses:
-nmcli: name=mod cname=my-eth1 dns4=["8.8.8.8", "8.8.4.4"]

# To bring up the new connection, issue a command as follows
- nmcli: name=up cname=my-eth1 ifname=eth1 enabled=yes state=present

# To lock a profile to a specific interface, issue a command as follows
- nmcli: name=add ctype=ethernet name=my-eth1 ifname=eth1 state=present

# To make a profile usable for all compatible Ethernet interfaces, issue a command as follows
- nmcli: name=add ctype=ethernet name=my-eth1 ifname="*" state=present

# To change the property of a setting e.g. MTU, issue a command as follows:
- nmcli: name=modify cname=my-eth1 mtu=9000

    Exit Status's:
        - nmcli exits with status 0 if it succeeds, a value greater than 0 is
        returned if an error occurs.
        - 0 Success - indicates the operation succeeded
        - 1 Unknown or unspecified error
        - 2 Invalid user input, wrong nmcli invocation
        - 3 Timeout expired (see --wait option)
        - 4 Connection activation failed
        - 5 Connection deactivation failed
        - 6 Disconnecting device failed
        - 7 Connection deletion failed
        - 8 NetworkManager is not running
        - 9 nmcli and NetworkManager versions mismatch
        - 10 Connection, device, or access point does not exist.
'''