Monasca plugin for OpenStack Heat
================================

This plugin enables using Monasca resources in a Heat template.
## Cloud setup with monasca and heat
Below steps provides the detail on how to setup a demo environment
by using monasca-vagrant and standalone heat.

### Install Monasca-vagrant
Monasca provides the monasca-vagrant installer to setup a
devstack with monasca server at the below url:

https://github.com/stackforge/monasca-vagrant

Here devstack will be created without heat service. so either
upgrade this devstack with heat service or follow the below step
to install heat in standalone mode.

At the end of installation, devstack will be running on 192.168.10.5
and monasca server will be running on 192.168.10.4.

NOTE: Please update the user to mini-mon instead of monasca-agent in
/etc/monasca/agent/agent.yaml, if libvirt moinitoring is failed.

### Install standalone heat
Create a vm with ubuntu 14.04 on the same virtual box where monasca-vagrant
is created and assign the IP 192.168.10.10. Then follow the below guidelines
to install heat in standalone mode, by using 192.168.10.5 devstack as remote cloud.

http://docs.openstack.org/developer/heat/getting_started/standalone.html

Once the heat is installed, below environment variables would help to run
heat and moasca commands.

``export OS_TENANT_NAME=mini-mon
export OS_PROJECT_NAME=mini-mon
export HEAT_URL=http://192.168.10.10:8004/v1/<mini-mon project id>
export OS_USERNAME=mini-mon
export OS_PASSWORD=password
export OS_AUTH_URL=http://192.168.10.5:35357/v2.0``

### Install the Monasca plugin in Heat

NOTE: Update /etc/heat/heat.conf plugin_dirs to include the
default directory /usr/lib/heat.

To install the plugin, from this directory run:
    sudo python ./setup.py install

### Restart heat

Only the process "heat-engine" needs to be restarted to load the newly installed
plugin.

After heat-engine is started, verify the availability of monasca resource plugin
by running heat resource-type-list

## To test the sample auto-scaling feature, run the following command
heat stack-create -f template/cirros-scale-up.yaml cirros-1

It will create cirros instance initially with 2 no.s then once the occurance of
the alarm, one more instance will be added.
