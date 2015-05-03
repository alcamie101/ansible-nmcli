import dbus
 
bus = dbus.SystemBus()
 
# Warning: Bus names and interfaces are different terms.
# Just because they contain same format or even same data
# does not mean they are the same thing.
# I used these variables to denote the diffrance where bus names and
# interfaces are used.
NM_BUSNAME = 'org.freedesktop.NetworkManager'
NM_IFACE = 'org.freedesktop.NetworkManager'
 
# Create Python object from /org/freedesktop/NetworkManager instance
# in org.freedesktop.NetworkManager application.
nm = bus.get_object(NM_BUSNAME, '/org/freedesktop/NetworkManager')
 
# Get list of active connections from the properties
# "Get" method is in "org.freedesktop.DBus.Properties" interface
# It takes the interface name which has the property and name of
# the property as arguments.
 
connections = nm.Get(NM_BUSNAME, 'ActiveConnections',
                     dbus_interface=dbus.PROPERTIES_IFACE)

 
# While invoking a method on the object, dbus_interface keyword
# argument is provided to specify which interface has the method.
 
# Now, lets disconnect. This time we are using the NetworkManager
# interface: "org.freedesktop.NetworkManager"
for path in connections:
    # nm.DeactivateConnection(path, dbus_interface=NM_IFACE)
    print(path, NM_IFACE)