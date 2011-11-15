==========================
ZenPacks.community.SMISMon
==========================

About
=====

This project is `Zenoss <http://www.zenoss.com/>`_ extension (ZenPack) that
makes it possible to model and monitor all SMI-S (Storage Management Initiative
- Specification) compatible storage devices. It creates a
**/Devices/Storage/SMI-S** Device Class for monitoring these storage devices.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2 and Zenoss 3.2. You can download the free Core version of
Zenoss from http://community.zenoss.org/community/download

ZenPacks
--------

You must first install
`SQLDataSource ZenPack <http://community.zenoss.org/docs/DOC-5913>`_.

Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `SMISMon ZenPack <http://community.zenoss.org/docs/DOC-5867>`_.
Copy this file to your Zenoss server and run the following commands as the
**zenoss** user.

    ::

        zenpack --install ZenPacks.community.SMISMon-1.0.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the SMISMon
ZenPack you should clone the git
`repository <https://github.com/epuzanov/ZenPacks.community.SMISMon>`_, then
install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.SMISMon.git
        zenpack --link --install ZenPacks.community.SMISMon
        zenoss restart


Usage
=====

#. You should now have Storage/SMI-S device class.
#. Click on the SMI-S class and select Details.
#. Click Configuration Properties on the left.
#. In the right pane, scroll to the bottom and in the **zSNIAConnectionString**
   field replace **host** and **namespace** properties with the IP address or
   hostname of the server where SMI-S agent installed and namespace of SMI-S
   agent. The reason for this is that you'ere going to use the SMI-S agent as a
   boker to grab data regarding the storages themselves, hence you request data
   about an storage using it's WWN and that request is fired at the SMI-S agent
   IP/Hostname.
#. In the **zWinPassword** and **zWinUser** add the correct credentials of a
   user account that can access the server.  (possibly create a new user account
   in AD and add this account to the SMI-S agent server).
#. Hit Save.
#. Click on See All at the top of the left pane.
#. Still in the SMI-S class click on the icon at the top of the main pane to add
   a new single device. Enter storage WWN into the Hostname or IP field and
   click **Add**.
#. Give Zenoss a chance to perform the Add Job, when I first added our storage
   the Job service was down and needed starting.
#. Once the device has been added, go into it and from the icon on the bottom
   left select Model Device. At this point I had issues with Zenoss connecting
   to Zenhub and got timeout errors. It eventually reconnected and carried on
   sometimes it didn't, just restart the modelling if it fails but give it a
   chance to retry.
#. Once the modelling has completed you should then see a load of objects in the
   Components menu in the left pane as well as a new hardware tab where the
   graphical disk view can be found.

Graphing should start almost immediately, you may need to soom in to see it
starting. I may have seen an issue involving the renaming of the device from
the WWN where graphing stops after the rename...well that's what appears to
have happened....so rename at your peril!

The following elements are discovered:

- Storage Enclosures (Status Only)
- Storage Controllers (Status Only)
- Hard Disks (Status Only)
- Storage Groups (Status Only)
- Virtual Disks (Status Only)
- FC Ports (Status Only)
