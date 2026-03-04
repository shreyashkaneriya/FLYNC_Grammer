"""Input models for Ethernet signal to SOME/IP mapping scenarios.

These models are intentionally shaped after integration-style input files
(e.g., ``input_signal.yaml``) so they can be validated in isolation before
being transformed into canonical FLYNC SOME/IP service/deployment models.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class TransformerChain(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    protocol: Literal["SOMEIP"]
    header_length_bits: int = Field(ge=0)
    in_place: bool


class DataTransformation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transformation_ref: str
    execute_despite_data_unavailability: bool
    transformer_chain: TransformerChain


class TransformationProps(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transformer_ref: str
    interface_version: str
    message_type: Literal["NOTIFICATION", "REQUEST", "RESPONSE"]
    size_of_array_length_fields: int = Field(ge=0)
    size_of_struct_length_fields: int = Field(ge=0)


class ISignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    system_signal_ref: str
    data_transformations: DataTransformation
    transformation_props: TransformationProps


class Mapping(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    i_signal_ref: str
    start_position_bits: int = Field(ge=0)
    packing_byte_order: str
    transfer_property: str


class ISignalIPDU(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    length_bytes: int = Field(gt=0)
    unused_bit_pattern: str
    mapping: Mapping


class PDUTriggering(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    i_pdu_ref: str
    i_pdu_port_refs: List[str] = Field(default_factory=list)
    i_signal_triggerings: List[str] = Field(default_factory=list)


class IPDUIdentifier(BaseModel):
    model_config = ConfigDict(extra="forbid")

    header_id: str
    service_id: str
    event_id: str
    message_type: Literal["NOTIFICATION", "REQUEST", "RESPONSE"]


class SocketConnection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bundle_name: str
    client_port_ref: str
    pdu_collection_max_buffer_size: int = Field(gt=0)
    pdu_collection_timeout: float = Field(ge=0)
    ipdu_identifier: IPDUIdentifier
    pdu_triggering_ref: str
    routing_group_ref: str


class RoutingGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    event_group_control_type: str


class EthernetConnector(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    signal_ports: List[str] = Field(default_factory=list)
    pdu_ports: List[str] = Field(default_factory=list)


class Connectors(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ethernet_connector: EthernetConnector


class ECUInstance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    associated_pdu_groups: List[str] = Field(default_factory=list)
    communication_controllers: dict[str, List[str]]
    connectors: Connectors


class ApplicationEndpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    network_endpoint_ref: str
    udp_tp_port: int = Field(ge=1, le=65535)


class SocketAddress(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    application_endpoint: ApplicationEndpoint
    connector_ref: str


class IPv4Configuration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ip_address: str
    address_source: str
    network_mask: str


class NetworkEndpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    ipv4_configuration: IPv4Configuration


class NetworkConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    socket_address: SocketAddress
    network_endpoint: NetworkEndpoint


class EthernetSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal_name: str
    description: str
    dynamic_length: bool
    length_bits: int = Field(gt=0)
    length_bytes: int = Field(gt=0)
    data_type_policy: str

    i_signal: ISignal
    i_signal_i_pdu: ISignalIPDU
    pdu_triggering: PDUTriggering
    socket_connection: SocketConnection
    routing_group: RoutingGroup
    ecu_instance: ECUInstance
    network_configuration: NetworkConfiguration


class EthernetSignalsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ethernet_signals: List[EthernetSignal] = Field(
        default_factory=list,
        alias="EthernetSignals",
        validation_alias="EthernetSignals",
        serialization_alias="EthernetSignals",
    )