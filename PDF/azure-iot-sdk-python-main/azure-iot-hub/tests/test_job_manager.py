# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import pytest
from azure.iot.hub.protocol.models import AuthenticationMechanism
from azure.iot.hub.iothub_job_manager import IoTHubJobManager
from azure.iot.hub.auth import ConnectionStringAuthentication
from azure.iot.hub.protocol.iot_hub_gateway_service_ap_is import IotHubGatewayServiceAPIs

"""---Constants---"""

fake_hostname = "beauxbatons.academy-net"
fake_device_id = "MyPensieve"
fake_shared_access_key_name = "alohomora"
fake_shared_access_key = "Zm9vYmFy"
fake_job_properties = "fake_job_properties"
fake_job_id = "fake_job_id"
fake_job_request = "fake_job_request"
fake_job_type = "fake_job_type"
fake_job_status = "fake_job_status"


"""----Shared fixtures----"""


@pytest.fixture(scope="function", autouse=True)
def mock_job_client_operations(mocker):
    mock_job_client_operations_init = mocker.patch(
        "azure.iot.hub.protocol.iot_hub_gateway_service_ap_is.JobsOperations"
    )
    return mock_job_client_operations_init.return_value


@pytest.fixture(scope="function")
def iothub_job_manager():
    connection_string = "HostName={hostname};DeviceId={device_id};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
        hostname=fake_hostname,
        device_id=fake_device_id,
        skn=fake_shared_access_key_name,
        sk=fake_shared_access_key,
    )
    iothub_job_manager = IoTHubJobManager.from_connection_string(connection_string)
    return iothub_job_manager


@pytest.mark.describe("IoTHubJobManager - .from_connection_string()")
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
        client = IoTHubJobManager.from_connection_string(connection_string=connection_string)

        assert repr(client.auth) == connection_string
        assert client.protocol.config.base_url == "https://" + client.auth["HostName"]
        assert client.protocol.config.credentials == client.auth

    @pytest.mark.it("Sets the auth and protocol attributes")
    def test_instantiates_auth_and_protocol_attributes(self, iothub_job_manager):
        assert isinstance(iothub_job_manager.auth, ConnectionStringAuthentication)
        assert isinstance(iothub_job_manager.protocol, IotHubGatewayServiceAPIs)

    @pytest.mark.it(
        "Raises a ValueError exception when instantiated with an empty connection string"
    )
    def test_instantiates_with_empty_connection_string(self):
        with pytest.raises(ValueError):
            IoTHubJobManager.from_connection_string("")

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
            IoTHubJobManager.from_connection_string(connection_string)

    @pytest.mark.it("Instantiates with an connection string without DeviceId")
    def test_instantiates_with_connection_string_no_device_id(self):
        connection_string = (
            "HostName={hostname};SharedAccessKeyName={skn};SharedAccessKey={sk}".format(
                hostname=fake_hostname, skn=fake_shared_access_key_name, sk=fake_shared_access_key
            )
        )
        obj = IoTHubJobManager.from_connection_string(connection_string)
        assert isinstance(obj, IoTHubJobManager)

    @pytest.mark.it("Instantiates with an connection string without SharedAccessKeyName")
    def test_instantiates_with_connection_string_no_shared_access_key_name(self):
        connection_string = "HostName={hostname};DeviceId={device_id};SharedAccessKey={sk}".format(
            hostname=fake_hostname, device_id=fake_device_id, sk=fake_shared_access_key
        )
        obj = IoTHubJobManager.from_connection_string(connection_string)
        assert isinstance(obj, IoTHubJobManager)

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
            IoTHubJobManager.from_connection_string(connection_string)


@pytest.mark.describe("IoTHubJobManager - .from_token_credential()")
class TestFromTokenCredential:
    @pytest.mark.it(
        "Creates an instance of AzureIdentityCredentialAdapter and passes it to IotHubGatewayServiceAPIs constructor"
    )
    def test_token_credential_auth(self, mocker):
        mock_azure_identity_TokenCredential = mocker.MagicMock()

        client = IoTHubJobManager.from_token_credential(
            fake_hostname, mock_azure_identity_TokenCredential
        )

        assert client.auth._policy._credential == mock_azure_identity_TokenCredential
        assert client.protocol.config.base_url == "https://" + fake_hostname
        assert client.protocol.config.credentials == client.auth


@pytest.mark.describe("IoTHubJobManager - .create_import_export_job()")
class TestCreateImportExportJob(object):
    @pytest.mark.it("Uses protocol layer Job Client runtime to create an export/import job")
    def test_create_export_import_job(self, mocker, mock_job_client_operations, iothub_job_manager):
        ret_val = iothub_job_manager.create_import_export_job(fake_job_properties)
        assert mock_job_client_operations.create_import_export_job.call_count == 1
        assert mock_job_client_operations.create_import_export_job.call_args == mocker.call(
            fake_job_properties
        )
        assert ret_val == mock_job_client_operations.create_import_export_job()


@pytest.mark.describe("IoTHubJobManager - .get_import_export_jobs()")
class TestGetImportExportJobs(object):
    @pytest.mark.it("Uses protocol layer Job Client runtime to get an export/import jobs")
    def test_get_export_import_jobs(self, mocker, mock_job_client_operations, iothub_job_manager):
        ret_val = iothub_job_manager.get_import_export_jobs()
        assert mock_job_client_operations.get_import_export_jobs.call_count == 1
        assert mock_job_client_operations.get_import_export_jobs.call_args == mocker.call()
        assert ret_val == mock_job_client_operations.get_import_export_jobs()


@pytest.mark.describe("IoTHubJobManager - .get_import_export_job()")
class TestGetImportExportJob(object):
    @pytest.mark.it("Uses protocol layer Job Client runtime to get an export/import job")
    def test_get_export_import_job(self, mocker, mock_job_client_operations, iothub_job_manager):
        ret_val = iothub_job_manager.get_import_export_job(fake_job_id)
        assert mock_job_client_operations.get_import_export_job.call_count == 1
        assert mock_job_client_operations.get_import_export_job.call_args == mocker.call(
            fake_job_id
        )
        assert ret_val == mock_job_client_operations.get_import_export_job()


@pytest.mark.describe("IoTHubJobManager - .cancel_import_export_job()")
class TestCancelImportExportJob(object):
    @pytest.mark.it("Uses protocol layer Job Client runtime to cancel an export/import job")
    def test_cancel_import_export_job(self, mocker, mock_job_client_operations, iothub_job_manager):
        ret_val = iothub_job_manager.cancel_import_export_job(fake_job_id)
        assert mock_job_client_operations.cancel_import_export_job.call_count == 1
        assert mock_job_client_operations.cancel_import_export_job.call_args == mocker.call(
            fake_job_id
        )
        assert ret_val == mock_job_client_operations.cancel_import_export_job()


@pytest.mark.describe("IoTHubJobManager - .create_job()")
class TestCreateScheduledJob(object):
    @pytest.mark.it("Uses protocol layer Job Client runtime to create a job")
    def test_create_scheduled_job(self, mocker, mock_job_client_operations, iothub_job_manager):
        ret_val = iothub_job_manager.create_scheduled_job(fake_job_id, fake_job_request)
        assert mock_job_client_operations.create_scheduled_job.call_count == 1
        assert mock_job_client_operations.create_scheduled_job.call_args == mocker.call(
            fake_job_id, fake_job_request
        )
        assert ret_val == mock_job_client_operations.create_scheduled_job()


@pytest.mark.describe("IoTHubJobManager - .get_job()")
class TestGetScheduledJob(object):
    @pytest.mark.it("Uses protocol layer Job Client runtime to get a job")
    def test_get_scheduled_job(self, mocker, mock_job_client_operations, iothub_job_manager):
        ret_val = iothub_job_manager.get_scheduled_job(fake_job_id)
        assert mock_job_client_operations.get_scheduled_job.call_count == 1
        assert mock_job_client_operations.get_scheduled_job.call_args == mocker.call(fake_job_id)
        assert ret_val == mock_job_client_operations.get_scheduled_job()


@pytest.mark.describe("IoTHubJobManager - .cancel_job()")
class TestCancelScheduledJob(object):
    @pytest.mark.it("Uses protocol layer Job Client runtime to cancel a job")
    def test_cancel_scheduled_job(self, mocker, mock_job_client_operations, iothub_job_manager):
        ret_val = iothub_job_manager.cancel_scheduled_job(fake_job_id)
        assert mock_job_client_operations.cancel_scheduled_job.call_count == 1
        assert mock_job_client_operations.cancel_scheduled_job.call_args == mocker.call(fake_job_id)
        assert ret_val == mock_job_client_operations.cancel_scheduled_job()


@pytest.mark.describe("IoTHubJobManager - .query_jobs()")
class TestQueryScheduledJobs(object):
    @pytest.mark.it("Uses protocol layer Job Client runtime to query a job")
    def test_query_scheduled_jobs(self, mocker, mock_job_client_operations, iothub_job_manager):
        ret_val = iothub_job_manager.query_scheduled_jobs(fake_job_type, fake_job_status)
        assert mock_job_client_operations.query_scheduled_jobs.call_count == 1
        assert mock_job_client_operations.query_scheduled_jobs.call_args == mocker.call(
            fake_job_type, fake_job_status
        )
        assert ret_val == mock_job_client_operations.query_scheduled_jobs()
