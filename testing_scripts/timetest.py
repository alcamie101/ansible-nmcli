#!/usr/bin/python

import datetime
import json
import sys
import os
import shlex

# read the arg string from the args file
args_file = sys.argv[1]
args_data = file(args_file).read()

#for this module, we're going to do key=value style arguments
# this is up to each module to decide what it wants, but all
#core modules besides 'command' and 'shell' take key=value
# so this is highly recommended

arguments = shlex.split(args_data)
for arg in arguments:

    #ignore any arguments without = in it
    if "=" in arg:

        (key, value) = arg.split("=")

        # if setting the time, the key 'time'
        # will contain the value we want to set the time to

        if key == "time":

            # now we'll affect the change. Many modules
            # will strive to be idempotent, meaning they
            # will only make changes when the desired state
            # expressed to the module does not match the
            # the current state. Look at Service
            # or yum in the main git tree for an example
            # of how that might look

            rc = os.system("date -s \"%s\"" % value)

            # always handle all possible errors
            #
            # when returning failure, include "failed"
            # in the return data, and explain the failure
            # in 'msg'. Both of these conventions are
            # required, however additional keys and values
            # can be added.

            if rc != 0:
                print json.dumps({
                    "failed" : True,
                    "msg"    : "failed setting the time"
                })
                sys.exit(1)

                # When things do not fail, we do not
                # have any restrictions on what kinds of
                # data are returned, but it's always a
                # good idea to include wether or not
                # a change was made, as that will allow
                # notifiers to be used in playbooks.

            date = str(datetime.datetime.now())
            print json.dumps({
                "time"  : date,
                "changed": True
            })
            sys.exit(0)

# if no parameters are sent, the module may or
# may not error out, this one will just
# return the line

date = str(datetime.datetime.now())
print json.dumps({
    "time" : date
})