import dbus

# This example asks settings service for all configured connections.

bus = dbus.SystemBus()

def print_connections():
    # Ask the settings service for the list of connections it provides
    service_name = "org.freedesktop.NetworkManager"
    proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager/Settings")
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")
    connection_paths = settings.ListConnections()

    # List each connection's name, UUID, and type
    for path in connection_paths:
        con_proxy = bus.get_object(service_name, path)
        settings_connection = dbus.Interface(con_proxy, "org.freedesktop.NetworkManager.Settings.Connection")
        config = settings_connection.GetSettings()

        # Get the details of the 'connection' setting
        s_con = config['connection']
        print "    name: %s" % s_con['id']
        print "    type: %s" % s_con['type']
        print ""

print_connections()
