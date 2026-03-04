from flync.model.flync_4_someip import EthernetSignalsInput


def _sample_payload():
    return {
        "EthernetSignals": [
            {
                "signal_name": "FrontWiperStateEvent",
                "description": "Dummy Ethernet signal for testing",
                "dynamic_length": False,
                "length_bits": 800,
                "length_bytes": 100,
                "data_type_policy": "NETWORK-REPRESENTATION",
                "i_signal": {
                    "name": "IFrontWiperStateEvent",
                    "system_signal_ref": "/SystemSignals/FrontWiperStateEvent",
                    "data_transformations": {
                        "transformation_ref": "/Transformations/SOME_IP_ONLY",
                        "execute_despite_data_unavailability": True,
                        "transformer_chain": {
                            "name": "SOME_IP_ONLY",
                            "protocol": "SOMEIP",
                            "header_length_bits": 16,
                            "in_place": False,
                        },
                    },
                    "transformation_props": {
                        "transformer_ref": "/Transformers/SOME_IP_ONLY",
                        "interface_version": "1.0",
                        "message_type": "NOTIFICATION",
                        "size_of_array_length_fields": 2,
                        "size_of_struct_length_fields": 100,
                    },
                },
                "i_signal_i_pdu": {
                    "name": "Eth_PDUFrontWiperStateEvent",
                    "length_bytes": 1400,
                    "unused_bit_pattern": "0xFF",
                    "mapping": {
                        "name": "Eth_Mapping_1",
                        "i_signal_ref": "/iSignals/IFrontWiperStateEvent",
                        "start_position_bits": 0,
                        "packing_byte_order": "MOST-SIGNIFICANT-BYTE-FIRST",
                        "transfer_property": "TRIGGERED",
                    },
                },
                "pdu_triggering": {
                    "name": "Eth_PDU_FrontWiperStateEvent",
                    "i_pdu_ref": "/IPDUs/Eth_PDUFrontWiperStateEvent",
                    "i_pdu_port_refs": ["Eth_PDU_Port_1"],
                    "i_signal_triggerings": [
                        "Eth_Signal_FrontWiperStateEvent"
                    ],
                },
                "socket_connection": {
                    "bundle_name": "Eth_Socket_Bundle_1",
                    "client_port_ref": "Eth_Client_Port",
                    "pdu_collection_max_buffer_size": 1400,
                    "pdu_collection_timeout": 0.005,
                    "ipdu_identifier": {
                        "header_id": "0x1234",
                        "service_id": "0x01",
                        "event_id": "0x01",
                        "message_type": "NOTIFICATION",
                    },
                    "pdu_triggering_ref": "Eth_PDU_FrontWiperStateEvent",
                    "routing_group_ref": "Eth_Routing_Group_1",
                },
                "routing_group": {
                    "name": "Eth_Routing_Group_1",
                    "event_group_control_type": "ACTIVATION-MULTICAST",
                },
                "ecu_instance": {
                    "name": "EthernetCluster",
                    "associated_pdu_groups": ["Eth_PDU_Group_1"],
                    "communication_controllers": {
                        "ethernet": ["SOME_IP_Secure_Domain_01"]
                    },
                    "connectors": {
                        "ethernet_connector": {
                            "name": "PCU_CP_1_SOME_IP_Secure_Domain_01",
                            "signal_ports": ["Eth_Signal_Port_1"],
                            "pdu_ports": ["Eth_PDU_Port_1"],
                        }
                    },
                },
                "network_configuration": {
                    "socket_address": {
                        "name": "Eth_Socket_Address_1",
                        "application_endpoint": {
                            "name": "Eth_APP_Endpoint_1",
                            "network_endpoint_ref": "Eth_Network_Endpoint_1",
                            "udp_tp_port": 30509,
                        },
                        "connector_ref": "Eth_Connector_1",
                    },
                    "network_endpoint": {
                        "name": "Eth_Network_Endpoint_1",
                        "ipv4_configuration": {
                            "ip_address": "192.168.178.100",
                            "address_source": "FIXED",
                            "network_mask": "255.255.255.0",
                        },
                    },
                },
            }
        ]
    }


def test_ethernet_signal_input_accepts_image_shape_payload():
    model = EthernetSignalsInput.model_validate(_sample_payload())

    assert len(model.ethernet_signals) == 1
    assert model.ethernet_signals[0].signal_name == "FrontWiperStateEvent"
    assert (
        model.ethernet_signals[0]
        .socket_connection
        .ipdu_identifier
        .message_type
        == "NOTIFICATION"
    )


def test_ethernet_signal_input_keeps_alias_on_dump():
    model = EthernetSignalsInput.model_validate(_sample_payload())
    dumped = model.model_dump(by_alias=True)

    assert "EthernetSignals" in dumped
    assert dumped["EthernetSignals"][0]["routing_group"]["name"] == (
        "Eth_Routing_Group_1"
    )