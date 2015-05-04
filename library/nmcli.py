#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Chris Long <alcamie@gmail.com>
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
version_added: "0.1"
short_description: Manage Networking
requirements: [ conadd, condel, conmod, conup, condown, constatus, conshow ]
description:
    - Manage the network devices. Create, modify, and manage, ethernet, teams, bonds, vlans etc.
options:
    name:
        required: true
        version_added: "0.1"
        required: False
        choices: [ add, modify, show, up, down ]
        description:
            - Set to 'add' if you want to add a connection.
            - Set to 'modify' if you want to modify a connection. Modify one or more properties in the connection profile.
            - Set to 'delete' if you want to delete a connection. Delete a configured connection. The connection to be deleted is identified by its name 'cfname'.
            - Set to 'show' if you want to show a connection. Will show all devices unless 'cfname' is set.
            - Set to 'up' if you want to bring a connection up. Requires 'cfname' to be set.
            - Set to 'down' if you want to bring a connection down. Requires 'cfname' to be set.
    cname:
        required: false
        version_added: "0.1"
        description:
            - Where CNAME will be the name used to call the connection. when not provided a default name is generated: <type>[-<ifname>][-<num>]
    autoconnect:
        required: false
        version_added: "0.1"
        default: yes
        choices: [ yes, no ]
        description:
            - Whether the connection profile can be automatically activated ( default: yes)
    ifname:
        required: false
        version_added: "0.1"
        description:
            - Where INAME will be the what we call the interface name. Required with 'up', 'down' modifiers.
            - interface to bind the connection to. The connection will only be applicable to this interface name.
            - A special value of "*" can be used for interface-independent connections.
            - The ifname argument is mandatory for all connection types except bond, team, bridge and vlan.
    type:
        required: false
        version_added: "0.1"
        choices: [ ethernet, team, team-slave, bond, bond-slave, bridge, vlan ]
        description:
            - This is the type of device or network connection that you wish to create.
    bondmode:
        required: false
        version_added: "0.1"
        choices: [ "balance-rr", "active-backup", "balance-xor", "broadcast", "802.3ad", "balance-tlb", "balance-alb" ]
        default: "balance-rr"
        description:
            - This is the type of device or network connection that you wish to create.
    master:
        required: false
        version_added: "0.1"
        description:
            - master <master (ifname, or connection UUID or cname) of bridge, team, bond master connection profile.
    ip4:
        required: false
        version_added: "0.1"
        description: The IPv4 address to this interface using this format ie: "192.168.1.24/24"
    gw4:
        required: false
        version_added: "0.1"
        description: The IPv4 gateway for this interface using this format ie: "192.168.100.1"
    dns4:
        required: false
        version_added: "0.1"
        description: A list of upto 3 dns servers, ipv4 format e.g. To add two IPv4 DNS server addresses: ['"8.8.8.8 8.8.4.4"']
    ip6:
        required: false
        version_added: "0.1"
        description:
            - The IPv6 address to this interface using this format ie: "abbe::cafe"
    gw:
        required: false
        version_added: "0.1"
        aliases: [ "gw6" ]
        description: The IPv6 gateway for this interface using this format ie: "2001:db8::1"
    dns6:
        required: false
        version_added: "0.1"
        description: A list of upto 3 dns servers, ipv6 format e.g. To add two IPv6 DNS server addresses: ['"2001:4860:4860::8888 2001:4860:4860::8844"']
    mtu:
        required: false
        version_added: "0.1"
        description:
            - The connection MTU, e.g. 9000. This can't be applied when creating the interface and is done once the interface has been created.
    stp:
        required: false
        version_added: "0.1"
        default: yes
        description:
            - This is only used with bridge and controls whether Spanning Tree Protocol (STP) is enabled for this bridge
    priority:
        required: false
        version_added: "0.1"
        default: "128"
        description:
            - This is only used with 'bridge' - sets STP priority (default: 128)
    slavepriority:
        required: false
        version_added: "0.1"
        default: "128"
        description:
            - This is only used with 'bridge-slave' - STP priority of this slave (default: 32)
    forwarddelay:
        required: false
        version_added: "0.1"
        default: "15"
        description:
            - This is only used with bridge - [forward-delay <2-30>] STP forwarding delay, in seconds (default: 15)
    hellotime:
        required: false
        version_added: "0.1"
        default: "2"
        description:
            - This is only used with bridge - [hello-time <1-10>] STP hello time, in seconds (default: 2)
    maxage:
        required: false
        version_added: "0.1"
        default: "20"
        description:
            - This is only used with bridge - [max-age <6-42>] STP maximum message age, in seconds (default: 20)
    ageingtime:
        required: false
        version_added: "0.1"
        default: "300"
        description:
            - This is only used with bridge - [ageing-time <0-1000000>] the Ethernet MAC address aging time, in seconds (default: 300)
    mac:
        required: false
        version_added: "0.1"
        default: "300"
        description:
            - This is only used with bridge - MAC address of the bridge (note: this requires a recent kernel feature, originally introduced in 3.15 upstream kernel)
    vlanid:
        required: false
        version_added: "0.1"
        description:
            - This is only used with VLAN - VLAN ID in range <0-4095>
        state:
            required: false
            default: "present"
            choices: [ present, absent ]
        description:
            - Whether the device should exist or not, taking action if the state is different from what is stated.
    enabled:
        required: false
        version_added: "0.1"
        default: "yes"
        choices: [ "yes", "no" ]
        description:
            - Whether the service should start on boot. B(At least one of state and enabled are required.)
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
import ansible.module_utils.basic
import os
import syslog
import sys
import NetworkManager
import dbus


class Nmcli(object):
    """
    This is the generic nmcli manipulation class that is subclassed based on platform.
    A subclass may wish to override the following action methods:-
            - create_connection()
            - delete_connection()
            - modify_connection()
            - show_connection()
            - up_connection()
            - down_connection()
    All subclasses MUST define platform and distribution (which may be None).
    """

    platform='Generic'
    distribution=None

    def __new__(cls, *args, **kwargs):
        return load_platform_subclass(Nmcli, args, kwargs)

    def __init__(self, module):
        self.module=module
        self.state=module.params['state']
        self.enabled=module.params['enabled']
        self.name=module.params['name']
        self.cname=module.params['cname']
        self.master=module.params['master']
        self.autoconnect=module.params['autoconnect']
        self.ifname=module.params['ifname']
        self.type=module.params['type']
        self.ip4=module.params['ip4']
        self.gw4=module.params['gw4']
        self.dns4=module.params['dns4']
        self.ip6=module.params['ip6']
        self.gw6=module.params['gw6']
        self.dns6=module.params['dns6']
        self.mtu=module.params['mtu']
        self.stp=module.params['stp']
        self.priority=module.params['priority']
        self.slavepriority=module.params['slavepriority']
        self.forwarddelay=module.params['forwarddelay']
        self.hellotime=module.params['hellotime']
        self.maxage=module.params['maxage']
        self.ageingtime=module.params['ageingtime']
        self.mac=module.params['mac']
        self.vlanid=module.params['vlanid']
        # The following is going to be used in dbus code
        self.devtypes={1: "Ethernet",
                       2: "Wi-Fi",
                       5: "Bluetooth",
                       6: "OLPC",
                       7: "WiMAX",
                       8: "Modem",
                       9: "InfiniBand",
                       10: "Bond",
                       11: "VLAN",
                       12: "ADSL",
                       13: "Bridge",
                       14: "Generic",
                       15: "Team"
                       }
        self.states={0: "Unknown",
                     10: "Unmanaged",
                     20: "Unavailable",
                     30: "Disconnected",
                     40: "Prepare",
                     50: "Config",
                     60: "Need Auth",
                     70: "IP Config",
                     80: "IP Check",
                     90: "Secondaries",
                     100: "Activated",
                     110: "Deactivating",
                     120: "Failed"}
        # select whether we dump additional debug info through syslog
        self.syslogging=True

    def execute_command(self, cmd, use_unsafe_shell=False, data=None):
        if self.syslogging:
            syslog.openlog('ansible-%s' % os.path.basename(__file__))
            syslog.syslog(syslog.LOG_NOTICE, 'Command %s' % '|'.join(cmd))

        return self.module.run_command(cmd, use_unsafe_shell=use_unsafe_shell, data=data)

    def list_connection_info(self):

        bus=dbus.SystemBus()
        connection_list=[]

        # Get a proxy for the base NetworkManager object
        proxy=bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
        manager=dbus.Interface(proxy, "org.freedesktop.NetworkManager")

        # Get all devices known to NM and list interface names
        devices=manager.GetDevices()
        for d in devices:
            dev_proxy=bus.get_object("org.freedesktop.NetworkManager", d)
            prop_iface=dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
            props=prop_iface.GetAll("org.freedesktop.NetworkManager.Device")
            connection_list.append(props['Interface'])
            # try:
            #     devtype = devtypes[props['DeviceType']]
            # except KeyError:
            #     devtype = "Unknown"
            # print "Type: %s" % devtype
            #
            # print "Driver: %s" % props['Driver']
            #
            # try:
            #     state = states[props['State']]
            # except KeyError:
            #     state = "Unknown"
            # print "State: %s" % state
        return connection_list

    def connection_exists(self):
        # we are going to use name and type in this instance to find if that connection exists and is of type x
        connections=self.list_connection_info()

        for con_item in connections:
            if self.cname==con_item:
                return True
        return False

    def down_connection(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # if self.connection_exists():
        cmd.append('con')
        cmd.append('down')
        cmd.append(self.cname)
        return self.execute_command(cmd)

    def up_connection(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # if self.connection_exists():
        cmd.append('con')
        cmd.append('up')
        cmd.append(self.cname)
        return self.execute_command(cmd)

    def create_connection_team(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # if connection_exists()
        #     self.module.fail_json(msg="this connection exists already")
        # else:
        # format for creating team interface
        cmd.append('con')
        cmd.append('add')
        cmd.append('type')
        cmd.append(self.type)
        cmd.append('con-name')
        if self.cname is not None:
            cmd.append(self.cname)
        elif self.ifname is not None:
            cmd.append(self.ifname)
        else:
            self.module.fail_json(msg="You haven't specified a name for the connection")
            # cmd.append(self.cname)
        cmd.append('ifname')
        if self.ifname is not None:
            cmd.append(self.ifname)
        elif self.cname is not None:
            cmd.append(self.cname)
        if self.ip4 is not None:
            cmd.append('ip4')
            cmd.append(self.ip4)
        if self.gw4 is not None:
            cmd.append('gw4')
            cmd.append(self.gw4)
        # if self.dns4 is not None:
        #     cmd.append('ipv4.dns')
        #     cmd.append(self.dns4)
        # if self.ip6 is not None:
        #     cmd.append('ip6')
        #     cmd.append(self.ip6)
        # if self.gw6 is not None:
        #     cmd.append('gw6')
        #     cmd.append(self.gw4)
        # if self.dns6 is not None:
        #     cmd.append('dns6')
        #     cmd.append(self.dns6)
        if self.enabled is not None:
            cmd.append('autoconnect')
            cmd.append(self.enabled)
        return cmd

    def modify_connection_team(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # if connection_exists()
        #     self.module.fail_json(msg="this connection exists already")
        # else:
        # format for modifying team interface
        cmd.append('con')
        cmd.append('mod')
        if self.cname is not None:
            cmd.append(self.cname)
        else:
            self.module.fail_json(msg="You haven't specified a name for the connection")
        if self.ip4 is not None:
            cmd.append('ip4')
            cmd.append(self.ip4)
        if self.gw4 is not None:
            cmd.append('gw4')
            cmd.append(self.gw4)
        if self.dns4 is not None:
            cmd.append('ipv4.dns')
            cmd.append(self.dns4)
        if self.ip6 is not None:
            cmd.append('ip6')
            cmd.append(self.ip6)
        if self.gw6 is not None:
            cmd.append('gw6')
            cmd.append(self.gw4)
        if self.dns6 is not None:
            cmd.append('ipv6.dns')
            cmd.append(self.dns6)
        if self.enabled is not None:
            cmd.append('autoconnect')
            cmd.append(self.enabled)
        return cmd

    def create_connection_team_slave(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for creating team-slave interface
        cmd.append('connection')
        cmd.append('add')
        cmd.append('type')
        cmd.append(self.type)
        cmd.append('con-name')
        if self.cname is not None:
            cmd.append(self.cname)
        elif self.ifname is not None:
            cmd.append(self.ifname)
        else:
            self.module.fail_json(msg="You haven't specified a name for the connection")
            # cmd.append(self.cname)
        cmd.append('ifname')
        if self.ifname is not None:
            cmd.append(self.ifname)
        elif self.cname is not None:
            cmd.append(self.cname)
        cmd.append('master')
        if self.cname is not None:
            cmd.append(self.master)
        else:
            self.module.fail_json(msg="You haven't specified a name for the master")
        if self.enabled is not None:
            cmd.append('autoconnect')
            cmd.append(self.enabled)
        return cmd

    def modify_connection_team_slave(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for modifying team-slave interface
        cmd.append('con')
        cmd.append('mod')
        if self.cname is not None:
            cmd.append(self.cname)
        else:
            self.module.fail_json(msg="You haven't specified a name for the connection")
        cmd.append('master')
        if self.cname is not None:
            cmd.append(self.master)
        else:
            self.module.fail_json(msg="You haven't specified a name for the master so we're not changing a thing")
        return cmd

    def create_connection_bond(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for creating bond interface
        return cmd

    def modify_connection_bond(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for modifying bond interface
        return cmd

    def create_connection_bond_slave(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for creating bond-slave interface
        return cmd

    def modify_connection_bond_slave(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for modifying bond-slave interface
        return cmd

    def create_connection_ethernet(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for creating ethernet interface
        # To add an Ethernet connection with static IP configuration, issue a command as follows
        # - nmcli: name=add cname=my-eth1 ifname=eth1 type=ethernet ip4=192.168.100.100/24 gw4=192.168.100.1 state=present
        #        nmcli con add con-name my-eth1 ifname eth1 type ethernet ip4 192.168.100.100/24 gw4 192.168.100.1
        # if self.type == 'ethernet':
        #     cmd.append = 'con'
        #     cmd.append = self.name
        #     cmd.append('con-name')
        #     if self.cname is not None:
        #         cmd.append(self.cname)
        #     elif self.cname is None:
        #         if self.ifname is not None:
        #             cmd.append(self.ifname)
        #     cmd.append('ifname')
        #     cmd.append(self.ifname)
        #     cmd.append('type')
        #     cmd.append(self.type)
        #     if self.ip4 is not None:
        #         cmd.append('ip4')
        #         cmd.append(self.ip4)
        #     if self.gw4 is not None:
        #         cmd.append('gw4')
        #         cmd.append(self.gw4)
        #     if self.dns4 is not None:
        #         cmd.append('dns4')
        #         cmd.append(self.dns4)
        #     if self.ip6 is not None:
        #         cmd.append('ip6')
        #         cmd.append(self.ip6)
        #     if self.gw6 is not None:
        #         cmd.append('gw6')
        #         cmd.append(self.gw4)
        #     if self.dns6 is not None:
        #         cmd.append('dns6')
        #         cmd.append(self.dns6)
        return cmd

    def modify_connection_ethernet(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for  modifying ethernet interface
        # To add an Ethernet connection with static IP configuration, issue a command as follows
        # - nmcli: name=add cname=my-eth1 ifname=eth1 type=ethernet ip4=192.168.100.100/24 gw4=192.168.100.1 state=present
        #        nmcli con add con-name my-eth1 ifname eth1 type ethernet ip4 192.168.100.100/24 gw4 192.168.100.1
        # if self.type == 'ethernet':
        #     cmd.append = 'con'
        #     cmd.append = self.name
        #     cmd.append('con-name')
        #     if self.cname is not None:
        #         cmd.append(self.cname)
        #     elif self.cname is None:
        #         if self.ifname is not None:
        #             cmd.append(self.ifname)
        #     cmd.append('ifname')
        #     cmd.append(self.ifname)
        #     cmd.append('type')
        #     cmd.append(self.type)
        #     if self.ip4 is not None:
        #         cmd.append('ip4')
        #         cmd.append(self.ip4)
        #     if self.gw4 is not None:
        #         cmd.append('gw4')
        #         cmd.append(self.gw4)
        #     if self.dns4 is not None:
        #         cmd.append('dns4')
        #         cmd.append(self.dns4)
        #     if self.ip6 is not None:
        #         cmd.append('ip6')
        #         cmd.append(self.ip6)
        #     if self.gw6 is not None:
        #         cmd.append('gw6')
        #         cmd.append(self.gw4)
        #     if self.dns6 is not None:
        #         cmd.append('dns6')
        #         cmd.append(self.dns6)
        return cmd

    def create_connection_bridge(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for creating bridge interface
        return cmd

    def modify_connection_bridge(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for modifying bridge interface
        return cmd

    def create_connection_vlan(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for creating ethernet interface
        return cmd

    def modify_connection_vlan(self):
        cmd=[self.module.get_bin_path('nmcli', True)]
        # format for modifying ethernet interface
        return cmd

    def create_connection(self):
        cmd=[]
        if self.type=='team':
            cmd=self.create_connection_team()
        elif self.type=='team-slave':
            cmd=self.create_connection_team_slave()
        elif self.type=='bond':
            cmd=self.create_connection_bond()
        elif self.type=='bond-slave':
            cmd=self.create_connection_bond_slave()
        elif self.type=='ethernet':
            cmd=self.create_connection_ethernet()
        elif self.type=='bridge':
            cmd=self.create_connection_bridge()
        elif self.type=='vlan':
            cmd=self.create_connection_vlan()
        return self.execute_command(cmd)

    def remove_connection(self):
        # self.down_connection()

        cmd=[self.module.get_bin_path('nmcli', True)]
        cmd.append('con')
        cmd.append('del')
        cmd.append(self.cname)
        return self.execute_command(cmd)

    def modify_connection(self):
        cmd=[]
        if self.type=='team':
            cmd=self.modify_connection_team()
        elif self.type=='team-slave':
            cmd=self.modify_connection_team_slave()
        elif self.type=='bond':
            cmd=self.modify_connection_bond()
        elif self.type=='bond-slave':
            cmd=self.modify_connection_bond_slave()
        elif self.type=='ethernet':
            cmd=self.modify_connection_ethernet()
        elif self.type=='bridge':
            cmd=self.modify_connection_bridge()
        elif self.type=='vlan':
            cmd=self.modify_connection_vlan()
        return self.execute_command(cmd)


def main():
    # Parsing argument file
    module=AnsibleModule(
        argument_spec=dict(
            enabled=dict(required=False, default=None, choices=['yes', 'no'], type='str'),
            name=dict(required=False, default=None, choices=['add', 'mod', 'show', 'up', 'down', 'del'], type='str'),
            state=dict(default=None, choices=['present', 'absent', 'modify'], type='str'),
            cname=dict(required=False, type='str'),
            master=dict(required=False, default=None, type='str'),
            autoconnect=dict(required=False, default=None, choices=['yes', 'no'], type='str'),
            ifname=dict(required=False, default=None, type='str'),
            type=dict(required=False, default=None, choices=['ethernet', 'team', 'team-slave', 'bond', 'bond-slave', 'bridge', 'vlan'], type='str'),
            ip4=dict(required=False, default=None, type='str'),
            gw4=dict(required=False, default=None, type='str'),
            dns4=dict(required=False, default=None, type='str'),
            ip6=dict(required=False, default=None, type='str'),
            gw6=dict(required=False, default=None, type='str'),
            dns6=dict(required=False, default=None, type='str'),
            # general usage
            mtu=dict(required=False, default=None, type='str'),
            mac=dict(required=False, default=None, type='str'),
            # bridge specific vars
            stp=dict(required=False, default='yes', choices=['yes', 'no'], type='str'),
            priority=dict(required=False, default="128", type='str'),
            slavepriority=dict(required=False, default="32", type='str'),
            forwarddelay=dict(required=False, default="15", type='str'),
            hellotime=dict(required=False, default="2", type='str'),
            maxage=dict(required=False, default="20", type='str'),
            ageingtime=dict(required=False, default="300", type='str'),
            # vlan specific vars
            vlanid=dict(required=False, default=None, type='str'),
            # following options are specific to ifnamedel
        ),
        supports_check_mode=True
    )

    # if module.params['state'] is None and module.params['enabled'] is None:
    #     module.fail_json(msg="'Neither state' nor 'enabled' is set")

    nmcli=Nmcli(module)

    if nmcli.syslogging:
        syslog.openlog('ansible-%s' % os.path.basename(__file__))
        syslog.syslog(syslog.LOG_NOTICE, 'Nmcli instantiated - platform %s' % nmcli.platform)
        if nmcli.distribution:
            syslog.syslog(syslog.LOG_NOTICE, 'Nuser instantiated - distribution %s' % nmcli.distribution)

    rc=None
    out=''
    err=''
    result={}
    result['cname']=nmcli.cname
    result['state']=nmcli.state

    if nmcli.state=='absent':
        # if nmcli.connection_exists():
        if module.check_mode:
            module.exit_json(changed=True)
        (rc, out, err)=nmcli.down_connection()
        (rc, out, err)=nmcli.remove_connection()

        # elif not nmcli.connection_exists():
        #     result['Connection']='No Connection named %s exists' % nmcli.cname
        #     (rc, out, err)=nmcli.down_connection()
        #     (rc, out, err)=nmcli.remove_connection()
        #     result['Connection']='Connection %s is being removed' % nmcli.cname
        #     result['Connection']='Yessss. Connection %s exists' % nmcli.cname
        #     result['Connection']='Connection %s is being set to down' % nmcli.cname
        if rc!=0:
            module.fail_json(name =('No Connection named %s exists' % nmcli.cname), msg=err, rc=rc)

    elif nmcli.state=='present':
        if not nmcli.connection_exists():
            result['Connection']=('Connection %s of Type %s is being added' % (nmcli.cname, nmcli.type))
            result['Exists']='Connection dont exist'
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err)=nmcli.create_connection()
            # result['enabled']=nmcli.enabled
            # result['cname']=nmcli.cname
            # result['ifname']=nmcli.ifname
            # result['autoconnect']=nmcli.enabled
            # result['type']=nmcli.type
            # result['ip4']=nmcli.ip4

        elif nmcli.connection_exists():
            result['Connection']=('Connection %s of Type %s is not being added' % (nmcli.cname, nmcli.type))
            result['Exists']='Connections do exist so we can modify them'
    else :
        # modify connection (note: this function is check mode aware)
        result['Exists']='Connections do exist so we care modifying them'
        (rc, out, err)=nmcli.modify_connection()
        result['cname']=nmcli.cname
        result['ipv4']=nmcli.dns4
    # if rc is not None and rc!=0:
    #     module.fail_json(name=nmcli.cname, msg=err, rc=rc)

    if rc is None:
        result['changed']=False
    else:
        result['changed']=True
    if out:
        result['stdout']=out
    if err:
        result['stderr']=err

    # if nmcli.connection_exists():
    #     info = nmcli.connection_info( )
    #     if info == False:
    #         result[ 'msg' ] = "failed to find connection name: %s" % nmcli.cname
    #         result[ 'failed' ] = True
    #     result[ 'cname' ] = info[ 2 ]
    #     result[ 'type' ] = info[ 3 ]
    #     result[ 'changed' ] = True

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *

main()