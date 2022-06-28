# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Authorizations(object):
    """NOTE: This class is auto generated by OpenAPI Generator.

    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'links': 'Links',
        'authorizations': 'list[Authorization]'
    }

    attribute_map = {
        'links': 'links',
        'authorizations': 'authorizations'
    }

    def __init__(self, links=None, authorizations=None):  # noqa: E501,D401,D403
        """Authorizations - a model defined in OpenAPI."""  # noqa: E501
        self._links = None
        self._authorizations = None
        self.discriminator = None

        if links is not None:
            self.links = links
        if authorizations is not None:
            self.authorizations = authorizations

    @property
    def links(self):
        """Get the links of this Authorizations.

        :return: The links of this Authorizations.
        :rtype: Links
        """  # noqa: E501
        return self._links

    @links.setter
    def links(self, links):
        """Set the links of this Authorizations.

        :param links: The links of this Authorizations.
        :type: Links
        """  # noqa: E501
        self._links = links

    @property
    def authorizations(self):
        """Get the authorizations of this Authorizations.

        :return: The authorizations of this Authorizations.
        :rtype: list[Authorization]
        """  # noqa: E501
        return self._authorizations

    @authorizations.setter
    def authorizations(self, authorizations):
        """Set the authorizations of this Authorizations.

        :param authorizations: The authorizations of this Authorizations.
        :type: list[Authorization]
        """  # noqa: E501
        self._authorizations = authorizations

    def to_dict(self):
        """Return the model properties as a dict."""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Return the string representation of the model."""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`."""
        return self.to_str()

    def __eq__(self, other):
        """Return true if both objects are equal."""
        if not isinstance(other, Authorizations):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other