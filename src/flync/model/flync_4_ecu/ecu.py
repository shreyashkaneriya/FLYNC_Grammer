from typing import Annotated, List, Optional

from pydantic import Field, model_validator

from flync.core.annotations import (
    External,
    Implied,
    ImpliedStrategy,
    NamingStrategy,
    OutputStrategy,
)
from flync.core.base_models import UniqueName
from flync.model.flync_4_ecu.controller import Controller, ControllerInterface
from flync.model.flync_4_ecu.internal_topology import InternalTopology
from flync.model.flync_4_ecu.port import ECUPort
from flync.model.flync_4_ecu.socket_container import SocketContainer
from flync.model.flync_4_ecu.switch import Switch, SwitchPort
from flync.model.flync_4_metadata import ECUMetadata


def RESET_unique_name_cache():
    ControllerInterface.NAMES = set()
    SwitchPort.NAMES = set()


class ECU(UniqueName):
    """
    Represents an Electronic Control Unit (ECU) in the network.

    Parameters
    ----------
    name : str
        Name of the ECU.

    ports : list of :class:`~flync.model.flync_4_ecu.port.ECUPort`
        List of physical ECU ports.
        At least one port must be provided.

    controllers : list of \
    :class:`~flync.model.flync_4_ecu.controller.Controller`
        Controllers associated with this ECU.

    switches : list of \
    :class:`~flync.model.flync_4_ecu.switch.Switch`, optional
        Switches integrated within the ECU. If not provided, the ECU
        contains no internal switches.

    sockets : list of \
    :class:`~flync.model.flync_4_ecu.socket_container.SocketContainer`, \
    optional
        Socket containers within the ECU. If not provided, the ECU
        has no socket deployments configured.

    topology : \
    :class:`~flync.model.flync_4_ecu.internal_topology.InternalTopology`
        Internal topology defining the connectivity between
        ECU components.

    ecu_metadata : :class:`~flync.model.flync_4_metadata.metadata.ECUMetadata`
        Metadata information describing the ECU.
    """

    name: Annotated[
        str,
        Implied(
            strategy=ImpliedStrategy.FOLDER_NAME,
        ),
    ] = Field()
    ports: Annotated[
        List["ECUPort"],
        External(
            output_structure=OutputStrategy.SINGLE_FILE,
            naming_strategy=NamingStrategy.FIELD_NAME,
        ),
    ] = Field(min_length=1, default_factory=list)
    controllers: Annotated[
        List["Controller"],
        External(
            output_structure=OutputStrategy.FOLDER,
            naming_strategy=NamingStrategy.FIELD_NAME,
        ),
    ] = Field()
    switches: Annotated[
        Optional[List["Switch"]],
        External(
            output_structure=OutputStrategy.FOLDER,
            naming_strategy=NamingStrategy.FIELD_NAME,
        ),
    ] = Field(default_factory=list)
    topology: Annotated[
        "InternalTopology",
        External(
            output_structure=OutputStrategy.SINGLE_FILE
            | OutputStrategy.OMMIT_ROOT,
            naming_strategy=NamingStrategy.FIELD_NAME,
        ),
    ] = Field()
    ecu_metadata: Annotated[
        "ECUMetadata",
        External(
            output_structure=OutputStrategy.SINGLE_FILE
            | OutputStrategy.OMMIT_ROOT
        ),
    ] = Field()
    sockets: Annotated[
        Optional[List[SocketContainer]],
        External(
            output_structure=OutputStrategy.FOLDER,
            naming_strategy=NamingStrategy.FIELD_NAME,
        ),
    ] = Field(default_factory=list)

    @model_validator(mode="after")
    def post_validation(self):
        """
        allows the children attributes to access ._ecu
        """
        RESET_unique_name_cache()
        [setattr(p, "_ecu", self) for p in self.ports]  # noqa
        [setattr(c, "_ecu", self) for c in self.topology.connections]  # noqa
        return self

    def get_all_controllers(self):
        """Return a list of all controllers of the ECU."""
        return self.controllers

    def get_all_ports(self):
        """Return a list of all ports of the ECU."""
        return self.ports

    def get_all_switches(self):
        """Return a list of all switches of the ECU."""
        return self.switches

    def get_internal_topology(self):
        """Return a list of all switches of the ECU."""
        return self.topology

    def get_all_interfaces(self):
        """Return a list of all physical interfaces of the ECU."""
        interfaces = []
        for controller in self.controllers:
            for iface in controller.interfaces:
                if iface:
                    interfaces.append(iface)
        return interfaces if interfaces else None

    def get_all_switch_ports(self) -> List["SwitchPort"]:
        """Return a list of all ports of the ECU switch."""
        ports = []
        if self.switches is not None:
            for switch in self.switches:
                for port in switch.ports:
                    if port:
                        ports.append(port)
        return ports

    def get_switch_by_name(self, switch_name: str):
        """Retrieve a Switch of the ECU by name."""
        if self.switches is not None:
            for switch in self.switches:
                if switch.name == switch_name:
                    return switch
        return None  # Return None if not found

    def get_all_ips(self):
        """
        Get all IPs in a ECU
        """
        ip_lists = []
        for ctrl in self.get_all_controllers():
            ip_lists.extend(ctrl.get_all_ips())
        return ip_lists
