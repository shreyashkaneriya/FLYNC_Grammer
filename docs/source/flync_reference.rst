.. _flync_reference:

================
FLYNC Reference
================

The source is structured in 3 main parts:

.. toctree::
   :hidden:
   :caption: this toctree is needed for the sidepanel structure.

   flync_reference/core
   flync_reference/model
   flync_reference/sdk

- :doc:`flync_reference/core`  -   Additional functionalities for the model, such as utils, field annotations and validators.
- :doc:`flync_reference/model`  -   The heart of FLYNC is a pydantic model. Find a comprehensive reference of the model in this section.
- :doc:`flync_reference/sdk`  -  Pythonic API for developers to interact with the project modules and integrating FLYNC capabilities into applications.


.. _writing_flync_config:

***********************
Writing a FLYNC config
***********************

Authoring configurations with FLYNC is fully YAML-based using the extension ``.flync.yaml``.

The built-in loaders and validators expect a specific repository structure that we'll explore in this next section.


Repository Structure for FLYNC configs
############################################

The root of a FLYNC config repository holds four main parts: System Metadata, Topology, ECUs, and General.

.. rubric:: Guidelines

- For better usability of any FLYNC configuration, the **📂directories**, and **📄files** are expected to follow a certain structure.
- In this section any directory or file with ❗is **mandatory**.
- Certain files should adhere to naming conventions, so make sure to follow the checklists below. ✔


System Metadata
****************

The system metadata file defines the system context for the configuration, such as platform, system variant, and config release.

.. code-block::

   📄❗ system_metadata.flync.yaml

.. important::

   ✔ The file name **system_metadata** must be respected.

   ✔ The file is placed in the root of the config repo.


.. seealso::

   :ref:`SystemMetadata <system_meta>`

Topology
********

This directory describes the interconnections between nodes of the system.

.. code-block::

   📂 topology
   │
   ├── 📄 multicast_paths.flync.yaml
   └── 📄(❗) system_topology.flync.yaml

.. important::

   ✔ The file names **system_topology** and **multicast_paths** must be respected.

   ✔ The files are placed in a directory named **topology** .

   ✔  A system_topology must be defined, if there is more than one ECU in the system.

.. seealso::

   :ref:`System Topology <topology>`


ECUs
****

The ecus directory contains several sub-directories describing all the ECUs in the system and their configuration.
This includes controllers of the ECU, Port configuration, switches, and sockets.
All components inside the ECU are then described in an internal_topology where the structure inside an ECU is described.

.. code-block::

   📂❗ ecus
   │
   ├── 📂 ecu_1_name
   │   |
   │   ├── 📄❗ ports.flync.yaml
   │   ├── 📄❗ topology.flync.yaml
   │   ├── 📄❗ ecu_metadata.flync.yaml
   │   |
   │   ├── 📂❗ controllers
   │   │   ├── 📄❗ ecu_1_controller_1.flync.yaml
   │   │   ├── 📄❗ ecu_1_controller_n.flync.yaml
   │   │   └── 📄 ...
   │   |
   │   ├── 📂 sockets
   │   │   ├── 📄 socket_someip.flync.yaml
   │   │   └── 📄 ...
   │   |
   │   └── 📂 switches
   │       ├── 📄 switch1.flync.yaml
   │       └── 📄 switch2.flync.yaml
   │
   └── 📂 ecu_n_name
      └── ...

.. important::

   ✔ The directory names ``ecus/``, ``controllers/``, ``sockets/``, and ``switches/`` must be respected.

   ✔ The file names ``ports``, ``topology``, and ``ecu_metadata`` must be respected.
   All others are suggested.


.. seealso::

   Explore the whole ECU config further:

   - :ref:`ECU Config <ecu>`
   - :ref:`ECU Ports Config <ecu_ports>`
   - :ref:`Controller Config <controller>`
   - :ref:`Switch Config <switch>`
   - :ref:`internal_topology`
   - :ref:`ECU Metadata <ecu_meta>`



General
*******

This directory contains several sub-directories and files that describe assets and configurations for the whole system, such as TCP profiles or SOME/IP services.
This is a **non-mandatory** directory for the FLYNC configuration.

.. code-block::

   📂 general
   │
   ├── 📄 tcp_profiles.flync.yaml
   │
   └── 📂 someip
      |
      ├── 📂 services
      │   ├── 📄 someip_service.flync.yaml
      │   └── 📄 ...
      |
      └── 📄 sd_config.flync.yaml

.. important::

   ✔ If this directory is added, namings of sub-directories must be respected.

.. seealso::

   Explore the whole ECU config further:

   - :ref:`General Config <general>`
   - :ref:`TCPOptions <tcp_option>`
   - :ref:`SOME/IP Config <someip>`
   - :ref:`ServiceInterface <someip_serviceinterface>`


****************************
Validate your configuration
****************************

After writing your FLYNC config you can use this helper script from the FLYNC SDK to **validate** it.

.. code-block::

   python3 src/flync/sdk/helpers/validate_workspace.py --help
