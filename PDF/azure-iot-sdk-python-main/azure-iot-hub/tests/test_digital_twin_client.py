# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import pytest
from azure.iot.hub.protocol.models import AuthenticationMechanism
from azure.iot.hub.digital_twin_client import DigitalTwinClient
from azure.iot.hub.auth import ConnectionStringAuthentication
from azure.iot.hub.protocol.iot_hub_gateway_service_ap_is import IotHubGatewayServiceAPIs

"""---Constants---"""

fake_hostname = "beauxbatons.academy-net"
fake_device_id = "MyPensieve"
fake_shared_access_key_name = "alohomora"
fake_shared_access_key = "Zm9vYmFy"
fake_digital_twin_id = "fake_digital_twin_id"
fake_digital_twin_patch = "fake_digital_twin_patch"
fake_etag = "fake_etag"
fake_component_path = "fake_component_path"
fake_component_name = "fake_component_name"
fake_payload = "fake_payload"
fake_model_id = "fake_model_id"
fake_conn_timeout = 42
fake_resp_timeout = 72


"""----Shared fixtures----"""


@pytest.fixture(scope="function", autouse=True)
def mock_digital_twin_operations(mocker):
    mock_digital_twin_operations_init = mocker.patch(
        "azure.iot.hub.protocol.iot_hub_gateway_service_ap_is.DigitalTwinOperations"
    )
    return mock_digital_twin_operations_init.return_value


@pytest.fixture(scope="function")
def digital_twin_client():
    connection_string = "HostName={hostname};DeviceId={device_id};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
        hostname=fake_hostname,
        device_id=fake_device_id,
        skn=fake_shared_access_key_name,
        sk=fake_shared_access_key,
    )
    digital_twin_client = DigitalTwinClient.from_connection_string(connection_string)
    return digital_twin_client


@pytest.mark.describe("DigitalTwinClient - .from_connection_string()")
class TestFromConnectionString:
    @pytest.mark.parametrize(
        "connection_string",
        [
            pytest.param(
                "HostName={hostname};DeviceId={device_id};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
                    hostname=fake_hostname,
                    device_id=fake_device_id,
                    skn=fake_shared_access_key_name,
                    sk=fake_shared_access_key,
                ),
                id="connection string with HostName, DeviceId, SharedAccessKeyName, and SharedAccessKey",
            ),
            pytest.param(
                "HostName={hostname};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
                    hostname=fake_hostname,
                    skn=fake_shared_access_key_name,
                    sk=fake_shared_access_key,
                ),
                id="connection string without DeviceId",
            ),
            pytest.param(
                "HostName={hostname};DeviceId={device_id};SharedAccessKey={sk}".format(
                    hostname=fake_hostname, device_id=fake_device_id, sk=fake_shared_access_key
                ),
                id="connection string without SharedAccessKeyName",
            ),
        ],
    )
    @pytest.mark.it(
        "Creates an instance of ConnectionStringAuthentication and passes it to IotHubGatewayServiceAPIs constructor"
    )
    def test_connection_string_auth(self, connection_string):
        client = DigitalTwinClient.from_connection_string(connection_string=connection_string)

        assert repr(client.auth) == connection_string
        assert client.protocol.config.base_url == "https://" + client.auth["HostName"]
        assert client.protocol.config.credentials == client.auth

    @pytest.mark.it("Sets the auth and protocol attributes")
    def test_instantiates_auth_and_protocol_attributes(self, digital_twin_client):
        assert isinstance(digital_twin_client.auth, ConnectionStringAuthentication)
        assert isinstance(digital_twin_client.protocol, IotHubGatewayServiceAPIs)

    @pytest.mark.it(
        "Raises a ValueError exception when instantiated with an empty connection string"
    )
    def test_instantiates_with_empty_connection_string(self):
        with pytest.raises(ValueError):
            DigitalTwinClient.from_connection_string("")

    @pytest.mark.it(
        "Raises a ValueError exception when instantiated with a connection string without HostName"
    )
    def test_instantiates_with_connection_string_no_host_name(self):
        connection_string = (
            "DeviceId={device_id};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
                device_id=fake_device_id, skn=fake_shared_access_key_name, sk=fake_shared_access_key
            )
        )
        with pytest.raises(ValueError):
            DigitalTwinClient.from_connection_string(connection_string)

    @pytest.mark.it("Instantiates with an connection string without DeviceId")
    def test_instantiates_with_connection_string_no_device_id(self):
        connection_string = (
            "HostName={hostname};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
                hostname=fake_hostname, skn=fake_shared_access_key_name, sk=fake_shared_access_key
            )
        )
        obj = DigitalTwinClient.from_connection_string(connection_string)
        assert isinstance(obj, DigitalTwinClient)

    @pytest.mark.it("Instantiates with an connection string without SharedAccessKeyName")
    def test_instantiates_with_connection_string_no_shared_access_key_name(self):
        connection_string = "HostName={hostname};DeviceId={device_id};SharedAccessKey={sk}".format(
            hostname=fake_hostname, device_id=fake_device_id, sk=fake_shared_access_key
        )
        obj = DigitalTwinClient.from_connection_string(connection_string)
        assert isinstance(obj, DigitalTwinClient)

    @pytest.mark.it(
        "Raises a ValueError exception when instantiated with a connection string without SharedAccessKey"
    )
    def test_instantiates_with_connection_string_no_shared_access_key(self):
        connection_string = (
            "HostName={hostname};DeviceId={device_id};SharedAccessKeyName={skn}".format(
                hostname=fake_hostname, device_id=fake_device_id, skn=fake_shared_access_key_name
            )
        )
        with pytest.raises(ValueError):
            DigitalTwinClient.from_connection_string(connection_string)


@pytest.mark.describe("DigitalTwinClient - .from_token_credential()")
class TestFromTokenCredential:
    @pytest.mark.it(
        "Creates an instance of AzureIdentityCredentialAdapter and passes it to IotHubGatewayServiceAPIs constructor"
    )
    def test_token_credential_auth(self, mocker):
        mock_azure_identity_TokenCredential = mocker.MagicMock()

        client = DigitalTwinClient.from_token_credential(
            fake_hostname, mock_azure_identity_TokenCredential
        )

        assert client.auth._policy._credential == mock_azure_identity_TokenCredential
        assert client.protocol.config.base_url == "https://" + fake_hostname
        assert client.protocol.config.credentials == client.auth


@pytest.mark.describe("DigitalTwinClient - .get_digital_twin()")
class TestGetDigitalTwin(object):
    @pytest.mark.it("Uses protocol layer DigitalTwin Client runtime to get a digital twin")
    def test_get_digital_twin(self, mocker, mock_digital_twin_operations, digital_twin_client):
        ret_val = digital_twin_client.get_digital_twin(fake_digital_twin_id)
        assert mock_digital_twin_operations.get_digital_twin.call_count == 1
        assert mock_digital_twin_operations.get_digital_twin.call_args == mocker.call(
            fake_digital_twin_id
        )
        assert ret_val == mock_digital_twin_operations.get_digital_twin()


@pytest.mark.describe("DigitalTwinClient - .update_digital_twin()")
class TestUpdateDigitalTwin(object):
    @pytest.mark.it("Uses protocol layer DigitalTwin Client runtime to update a digital twin")
    def test_update_digital_twin(self, mocker, mock_digital_twin_operations, digital_twin_client):
        ret_val = digital_twin_client.update_digital_twin(
            fake_digital_twin_id, fake_digital_twin_patch, fake_etag
        )
        assert mock_digital_twin_operations.update_digital_twin.call_count == 1
        assert mock_digital_twin_operations.update_digital_twin.call_args == mocker.call(
            fake_digital_twin_id, fake_digital_twin_patch, fake_etag
        )
        assert ret_val == mock_digital_twin_operations.update_digital_twin()


@pytest.mark.describe("DigitalTwinClient - .update_digital_twin()")
class TestUpdateDigitalTwinNoEtag(object):
    @pytest.mark.it(
        "Uses protocol layer DigitalTwin Client runtime to update a digital twin without etag"
    )
    def test_update_digital_twin(self, mocker, mock_digital_twin_operations, digital_twin_client):
        ret_val = digital_twin_client.update_digital_twin(
            fake_digital_twin_id, fake_digital_twin_patch
        )
        assert mock_digital_twin_operations.update_digital_twin.call_count == 1
        assert mock_digital_twin_operations.update_digital_twin.call_args == mocker.call(
            fake_digital_twin_id, fake_digital_twin_patch, None
        )
        assert ret_val == mock_digital_twin_operations.update_digital_twin()


@pytest.mark.describe("DigitalTwinClient - .invoke_component_command()")
class TestInvokeComponentCommand(object):
    @pytest.mark.it("Uses protocol layer DigitalTwin Client runtime to invoke a component command")
    def test_invoke_component_command(
        self, mocker, mock_digital_twin_operations, digital_twin_client
    ):
        ret_val = digital_twin_client.invoke_component_command(
            fake_digital_twin_id, fake_component_path, fake_component_name, fake_payload
        )
        assert mock_digital_twin_operations.invoke_component_command.call_count == 1
        assert mock_digital_twin_operations.invoke_component_command.call_args == mocker.call(
            fake_digital_twin_id, fake_component_path, fake_component_name, fake_payload, None, None
        )
        assert ret_val == mock_digital_twin_operations.invoke_component_command()


@pytest.mark.describe("DigitalTwinClient - .invoke_component_command() - optional parameters")
class TestInvokeComponentCommandWithOptionalParameters(object):
    @pytest.mark.it("Uses protocol layer DigitalTwin Client runtime to invoke a component command")
    def test_invoke_component_command(
        self, mocker, mock_digital_twin_operations, digital_twin_client
    ):
        ret_val = digital_twin_client.invoke_component_command(
            fake_digital_twin_id,
            fake_component_path,
            fake_component_name,
            fake_payload,
            fake_conn_timeout,
            fake_resp_timeout,
        )
        assert mock_digital_twin_operations.invoke_component_command.call_count == 1
        assert mock_digital_twin_operations.invoke_component_command.call_args == mocker.call(
            fake_digital_twin_id,
            fake_component_path,
            fake_component_name,
            fake_payload,
            fake_conn_timeout,
            fake_resp_timeout,
        )
        assert ret_val == mock_digital_twin_operations.invoke_component_command()


@pytest.mark.describe("DigitalTwinClient - .invoke_command()")
class TestInvokeCommand(object):
    @pytest.mark.it("Uses protocol layer DigitalTwin Client runtime to invoke a component command")
    def test_invoke_command(self, mocker, mock_digital_twin_operations, digital_twin_client):
        ret_val = digital_twin_client.invoke_command(
            fake_digital_twin_id, fake_component_name, fake_payload
        )
        assert mock_digital_twin_operations.invoke_root_level_command.call_count == 1
        assert mock_digital_twin_operations.invoke_root_level_command.call_args == mocker.call(
            fake_digital_twin_id, fake_component_name, fake_payload, None, None
        )
        assert ret_val == mock_digital_twin_operations.invoke_root_level_command()


@pytest.mark.describe("DigitalTwinClient - .invoke_command()")
class TestInvokeCommandWithOptionalParameters(object):
    @pytest.mark.it("Uses protocol layer DigitalTwin Client runtime to invoke a component command")
    def test_invoke_command(self, mocker, mock_digital_twin_operations, digital_twin_client):
        ret_val = digital_twin_client.invoke_command(
            fake_digital_twin_id,
            fake_component_name,
            fake_payload,
            fake_conn_timeout,
            fake_resp_timeout,
        )
        assert mock_digital_twin_operations.invoke_root_level_command.call_count == 1
        assert mock_digital_twin_operations.invoke_root_level_command.call_args == mocker.call(
            fake_digital_twin_id,
            fake_component_name,
            fake_payload,
            fake_conn_timeout,
            fake_resp_timeout,
        )
        assert ret_val == mock_digital_twin_operations.invoke_root_level_command()
