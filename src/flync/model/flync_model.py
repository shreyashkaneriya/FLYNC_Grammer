from typing import Annotated, Dict, List, Optional, Tuple

from pydantic import Field, model_validator

from flync.core.annotations import External, NamingStrategy, OutputStrategy
from flync.core.base_models.base_model import FLYNCBaseModel
from flync.core.utils.exceptions import err_major
from flync.model.flync_4_ecu import (
    ECU,
    ECUPort,
    VirtualControllerInterface,
    VLANEntry,
)
from flync.model.flync_4_general_configuration import FLYNCGeneralConfig
from flync.model.flync_4_metadata import SystemMetadata
from flync.model.flync_4_topology import FLYNCTopology


class FLYNCModel(FLYNCBaseModel):
    """
    Represents the top-level FLYNC configuration model for a system.

    This model aggregates all ECUs, system topology, metadata, and
    general configuration settings for the entire system.

    Parameters
    ----------
    ecus : list of :class:`~flync.model.flync_4_ecu.ecu.ECU`
        List of ECU definitions included in the system.

    topology : :class:`~flync.model.flync_4_topology.FLYNCTopology`
        The system-wide topology including external ECU connections
        and optional multicast paths.

    metadata : :class:`~flync.model.flync_4_metadata.SystemMetadata`
        System-level metadata including OEM, platform, and hardware/software
        information.

    general : \
        :class:`~flync.model.flync_4_general_configuration.FLYNCGeneralConfig`
        , optional
        Optional general configuration settings applicable system-wide.
    """

    general: Annotated[
        Optional[FLYNCGeneralConfig],
        External(
            output_structure=OutputStrategy.FOLDER,
            naming_strategy=NamingStrategy.FIELD_NAME,
        ),
    ] = Field(default=None)
    ecus: Annotated[
        List[ECU],
        External(
            output_structure=OutputStrategy.FOLDER,
            naming_strategy=NamingStrategy.FIELD_NAME,
        ),
    ]
    topology: Annotated[
        FLYNCTopology,
        External(
            output_structure=OutputStrategy.FOLDER,
            naming_strategy=NamingStrategy.FIELD_NAME,
        ),
    ]
    metadata: Annotated[
        SystemMetadata,
        External(
            output_structure=OutputStrategy.SINGLE_FILE
            | OutputStrategy.OMMIT_ROOT,
            naming_strategy=NamingStrategy.FIXED_PATH,
            path="system_metadata",
        ),
    ]

    _EXCLUDED_NAME_CHECK_CLASSES: Tuple[type, ...] = (
        VirtualControllerInterface,
        VLANEntry,
    )

    @model_validator(mode="after")
    def validate_unique_ips(self):
        """
        Validate all IPs are unique system wide
        """
        all_ips = []
        for ecu in self.ecus:
            new_ips = ecu.get_all_ips()
            for ip in new_ips:
                if ip not in all_ips:
                    all_ips.append(ip)
                else:
                    raise err_major(
                        f"The IP {ip} is repeated in ECU {ecu.name}"
                    )
        return self

    def get_all_ecus(self):
        """Return a list of all ECU names."""
        return [ecu.name for ecu in self.ecus]

    def get_ecu_by_name(self, ecu_name: str):
        """Retrieve an ECU by name."""
        for ecu in self.ecus:
            if ecu.name == ecu_name:
                return ecu
        return None

    def get_all_controllers(self):
        """Return a list of all controllers in all ECUs."""
        controllers = []
        for ecu in self.ecus:
            controllers.extend(ecu.controllers)
        return controllers

    def get_all_ecu_ports(self) -> List["ECUPort"]:
        """Return a list of all ECU ports"""
        ecu_ports = []
        for ecu in self.ecus:
            ecu_ports.extend(ecu.get_all_ports())
        return ecu_ports

    def get_all_ecu_ports_by_name(self) -> Dict[str, "ECUPort"]:
        return {e.name: e for e in self.get_all_ecu_ports()}

    def get_interface_by_name(self, name):
        return next(
            (
                interface
                for interface in self.get_all_interfaces()
                if interface.name == name
            ),
            None,
        )

    def get_all_interfaces(self):
        return [
            iface
            for controller in self.get_all_controllers()
            for iface in controller.interfaces
        ]

    def get_all_interfaces_names(self):
        """Return all the controller interface names"""
        all_interfaces = []
        for ecu in self.get_all_ecus():
            all_interfaces.extend(self.get_interfaces_for_ecu(ecu))
        return all_interfaces

    def get_interfaces_for_ecu(self, ecu_name: str):
        """Return a list of all interfaces for a given ECU."""
        ecu = self.get_ecu_by_name(ecu_name)
        if ecu:
            return [
                iface.name
                for controller in ecu.controllers
                for iface in controller.interfaces
            ]
        return []

    def get_system_topology_info(self):
        """Return system topology details."""
        return self.topology.system_topology.model_dump()
