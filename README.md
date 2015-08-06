Monasca plugin for OpenStack Heat
================================

This plugin enables using Monasca resources in a Heat template.

### 0.Pre-requisites
To install heat on the devstack, add the below line in localrc or local.conf
and run stack.sh

enable_service heat,h-api,h-eng,h-api-cfn

### 1. Install the Monasca plugin in Heat

NOTE: Update /etc/heat/heat.conf plugin_dirs to include the
default directory /usr/lib/heat.

To install the plugin, from this directory run:
    sudo python ./setup.py install

### 2. Restart heat

Only the process "heat-engine" needs to be restarted to load the newly installed
plugin.

After heat-engine is started, verify the availability of monasca resource plugin
by running heat resource-type-list

### 3. To test the sample auto-scaling feature, run the following command
heat stack-create -f template/cirros-scale-up.yaml cirros-1

It will create cirros instance initially with 2 no.s then once the occurance of
the alarm, one more instance will be added.
