# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import datetime
import sys
from typing import Any, AsyncIterable, Callable, Dict, Optional, TypeVar, cast

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.rest import AsyncHttpResponse, HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict

from ...operations._operations import (
    build_metric_definitions_list_request,
    build_metric_namespaces_list_request,
    build_metrics_list_request,
)

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import MutableMapping  # type: ignore  # pylint: disable=ungrouped-imports
JSON = MutableMapping[str, Any]  # pylint: disable=unsubscriptable-object
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class MetricDefinitionsOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~monitor_metrics_client.aio.MonitorMetricsClient`'s
        :attr:`metric_definitions` attribute.
    """

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def list(self, resource_uri: str, *, metricnamespace: Optional[str] = None, **kwargs: Any) -> AsyncIterable[JSON]:
        """Lists the metric definitions for the resource.

        :param resource_uri: The identifier of the resource. Required.
        :type resource_uri: str
        :keyword metricnamespace: Metric namespace to query metric definitions for. Default value is
         None.
        :paramtype metricnamespace: str
        :return: An iterator like instance of JSON object
        :rtype: ~azure.core.async_paging.AsyncItemPaged[JSON]
        :raises ~azure.core.exceptions.HttpResponseError:

        Example:
            .. code-block:: python

                # response body for status code(s): 200
                response == {
                    "category": "str",  # Optional. Custom category name for this metric.
                    "dimensions": [
                        {
                            "value": "str",  # the invariant value. Required.
                            "localizedValue": "str"  # Optional. the locale specific
                              value.
                        }
                    ],
                    "displayDescription": "str",  # Optional. Detailed description of this
                      metric.
                    "id": "str",  # Optional. the resource identifier of the metric definition.
                    "isDimensionRequired": bool,  # Optional. Flag to indicate whether the
                      dimension is required.
                    "metricAvailabilities": [
                        {
                            "retention": "1 day, 0:00:00",  # Optional. the retention
                              period for the metric at the specified timegrain.  Expressed as a
                              duration 'PT1M', 'P1D', etc.
                            "timeGrain": "1 day, 0:00:00"  # Optional. the time grain
                              specifies the aggregation interval for the metric. Expressed as a
                              duration 'PT1M', 'P1D', etc.
                        }
                    ],
                    "metricClass": "str",  # Optional. The class of the metric. Known values are:
                      "Availability", "Transactions", "Errors", "Latency", and "Saturation".
                    "name": {
                        "value": "str",  # the invariant value. Required.
                        "localizedValue": "str"  # Optional. the locale specific value.
                    },
                    "namespace": "str",  # Optional. the namespace the metric belongs to.
                    "primaryAggregationType": "str",  # Optional. the primary aggregation type
                      value defining how to use the values for display. Known values are: "None",
                      "Average", "Count", "Minimum", "Maximum", and "Total".
                    "resourceId": "str",  # Optional. the resource identifier of the resource
                      that emitted the metric.
                    "supportedAggregationTypes": [
                        "str"  # Optional. the collection of what aggregation types are
                          supported.
                    ],
                    "unit": "str"  # Optional. The unit of the metric. Known values are: "Count",
                      "Bytes", "Seconds", "CountPerSecond", "BytesPerSecond", "Percent",
                      "MilliSeconds", "ByteSeconds", "Unspecified", "Cores", "MilliCores", "NanoCores",
                      and "BitsPerSecond".
                }
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2018-01-01"))
        cls: ClsType[JSON] = kwargs.pop("cls", None)

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                request = build_metric_definitions_list_request(
                    resource_uri=resource_uri,
                    metricnamespace=metricnamespace,
                    api_version=api_version,
                    headers=_headers,
                    params=_params,
                )
                request.url = self._client.format_url(request.url)

            else:
                request = HttpRequest("GET", next_link)
                request.url = self._client.format_url(request.url)

            return request

        async def extract_data(pipeline_response):
            deserialized = pipeline_response.http_response.json()
            list_of_elem = deserialized["value"]
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                if _stream:
                    await response.read()  # Load the body in memory and close the socket
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)


class MetricsOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~monitor_metrics_client.aio.MonitorMetricsClient`'s
        :attr:`metrics` attribute.
    """

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace_async
    async def list(
        self,
        resource_uri: str,
        *,
        timespan: Optional[str] = None,
        interval: Optional[datetime.timedelta] = None,
        metricnames: Optional[str] = None,
        aggregation: Optional[str] = None,
        top: Optional[int] = None,
        orderby: Optional[str] = None,
        filter: Optional[str] = None,
        result_type: Optional[str] = None,
        metricnamespace: Optional[str] = None,
        **kwargs: Any
    ) -> JSON:
        """**Lists the metric values for a resource**.

        :param resource_uri: The identifier of the resource. Required.
        :type resource_uri: str
        :keyword timespan: The timespan of the query. It is a string with the following format
         'startDateTime_ISO/endDateTime_ISO'. Default value is None.
        :paramtype timespan: str
        :keyword interval: The interval (i.e. timegrain) of the query. Default value is None.
        :paramtype interval: ~datetime.timedelta
        :keyword metricnames: The names of the metrics (comma separated) to retrieve. Special case: If
         a metricname itself has a comma in it then use %2 to indicate it. Eg: 'Metric,Name1' should be
         **'Metric%2Name1'**. Default value is None.
        :paramtype metricnames: str
        :keyword aggregation: The list of aggregation types (comma separated) to retrieve. Default
         value is None.
        :paramtype aggregation: str
        :keyword top: The maximum number of records to retrieve.
         Valid only if $filter is specified.
         Defaults to 10. Default value is None.
        :paramtype top: int
        :keyword orderby: The aggregation to use for sorting results and the direction of the sort.
         Only one order can be specified.
         Examples: sum asc. Default value is None.
        :paramtype orderby: str
        :keyword filter: The **$filter** is used to reduce the set of metric data returned. Example:
         Metric contains metadata A, B and C. - Return all time series of C where A = a1 and B = b1 or
         b2 **$filter=A eq 'a1' and B eq 'b1' or B eq 'b2' and C eq '*'** - Invalid variant: **$filter=A
         eq 'a1' and B eq 'b1' and C eq '*' or B = 'b2'** This is invalid because the logical or
         operator cannot separate two different metadata names. - Return all time series where A = a1, B
         = b1 and C = c1: **$filter=A eq 'a1' and B eq 'b1' and C eq 'c1'** - Return all time series
         where A = a1 **$filter=A eq 'a1' and B eq '\ *' and C eq '*\ '**. Special case: When dimension
         name or dimension value uses round brackets. Eg: When dimension name is **dim (test) 1**
         Instead of using $filter= "dim (test) 1 eq '\ *' " use **$filter= "dim %2528test%2529 1 eq '*\
         ' "\ ** When dimension name is **\ dim (test) 3\ ** and dimension value is **\ dim3 (test) val\
         ** Instead of using $filter= "dim (test) 3 eq 'dim3 (test) val' " use **\ $filter= "dim
         %2528test%2529 3 eq 'dim3 %2528test%2529 val' "**. Default value is None.
        :paramtype filter: str
        :keyword result_type: Reduces the set of data collected. The syntax allowed depends on the
         operation. See the operation's description for details. Known values are: "Data" and
         "Metadata". Default value is None.
        :paramtype result_type: str
        :keyword metricnamespace: Metric namespace to query metric definitions for. Default value is
         None.
        :paramtype metricnamespace: str
        :return: JSON object
        :rtype: JSON
        :raises ~azure.core.exceptions.HttpResponseError:

        Example:
            .. code-block:: python

                # response body for status code(s): 200
                response == {
                    "timespan": "str",  # The timespan for which the data was retrieved. Its
                      value consists of two datetimes concatenated, separated by '/'.  This may be
                      adjusted in the future and returned back from what was originally requested.
                      Required.
                    "value": [
                        {
                            "id": "str",  # the metric Id. Required.
                            "name": {
                                "value": "str",  # the invariant value. Required.
                                "localizedValue": "str"  # Optional. the locale
                                  specific value.
                            },
                            "timeseries": [
                                {
                                    "data": [
                                        {
                                            "timeStamp": "2020-02-20
                                              00:00:00",  # the timestamp for the metric value in ISO
                                              8601 format. Required.
                                            "average": 0.0,  # Optional.
                                              the average value in the time range.
                                            "count": 0.0,  # Optional.
                                              the number of samples in the time range. Can be used to
                                              determine the number of values that contributed to the
                                              average value.
                                            "maximum": 0.0,  # Optional.
                                              the greatest value in the time range.
                                            "minimum": 0.0,  # Optional.
                                              the least value in the time range.
                                            "total": 0.0  # Optional. the
                                              sum of all of the values in the time range.
                                        }
                                    ],
                                    "metadatavalues": [
                                        {
                                            "name": {
                                                "value": "str",  #
                                                  the invariant value. Required.
                                                "localizedValue":
                                                  "str"  # Optional. the locale specific value.
                                            },
                                            "value": "str"  # Optional.
                                              the value of the metadata.
                                        }
                                    ]
                                }
                            ],
                            "type": "str",  # the resource type of the metric resource.
                              Required.
                            "unit": "str",  # The unit of the metric. Required. Known
                              values are: "Count", "Bytes", "Seconds", "CountPerSecond",
                              "BytesPerSecond", "Percent", "MilliSeconds", "ByteSeconds",
                              "Unspecified", "Cores", "MilliCores", "NanoCores", and "BitsPerSecond".
                            "displayDescription": "str",  # Optional. Detailed
                              description of this metric.
                            "errorCode": "str",  # Optional. 'Success' or the error
                              details on query failures for this metric.
                            "errorMessage": "str"  # Optional. Error message encountered
                              querying this specific metric.
                        }
                    ],
                    "cost": 0,  # Optional. The integer value representing the relative cost of
                      the query.
                    "interval": "1 day, 0:00:00",  # Optional. The interval (window size) for
                      which the metric data was returned in.  This may be adjusted in the future and
                      returned back from what was originally requested.  This is not present if a
                      metadata request was made.
                    "namespace": "str",  # Optional. The namespace of the metrics being queried.
                    "resourceregion": "str"  # Optional. The region of the resource being queried
                      for metrics.
                }
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2018-01-01"))
        cls: ClsType[JSON] = kwargs.pop("cls", None)

        request = build_metrics_list_request(
            resource_uri=resource_uri,
            timespan=timespan,
            interval=interval,
            metricnames=metricnames,
            aggregation=aggregation,
            top=top,
            orderby=orderby,
            filter=filter,
            result_type=result_type,
            metricnamespace=metricnamespace,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                await response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        if response.content:
            deserialized = response.json()
        else:
            deserialized = None

        if cls:
            return cls(pipeline_response, cast(JSON, deserialized), {})

        return cast(JSON, deserialized)


class MetricNamespacesOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~monitor_metrics_client.aio.MonitorMetricsClient`'s
        :attr:`metric_namespaces` attribute.
    """

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def list(self, resource_uri: str, *, start_time: Optional[str] = None, **kwargs: Any) -> AsyncIterable[JSON]:
        """Lists the metric namespaces for the resource.

        :param resource_uri: The identifier of the resource. Required.
        :type resource_uri: str
        :keyword start_time: The ISO 8601 conform Date start time from which to query for metric
         namespaces. Default value is None.
        :paramtype start_time: str
        :return: An iterator like instance of JSON object
        :rtype: ~azure.core.async_paging.AsyncItemPaged[JSON]
        :raises ~azure.core.exceptions.HttpResponseError:

        Example:
            .. code-block:: python

                # response body for status code(s): 200
                response == {
                    "classification": "str",  # Optional. Kind of namespace. Known values are:
                      "Platform", "Custom", and "Qos".
                    "id": "str",  # Optional. The ID of the metric namespace.
                    "name": "str",  # Optional. The escaped name of the namespace.
                    "properties": {
                        "metricNamespaceName": "str"  # Optional. The metric namespace name.
                    },
                    "type": "str"  # Optional. The type of the namespace.
                }
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2017-12-01-preview"))
        cls: ClsType[JSON] = kwargs.pop("cls", None)

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                request = build_metric_namespaces_list_request(
                    resource_uri=resource_uri,
                    start_time=start_time,
                    api_version=api_version,
                    headers=_headers,
                    params=_params,
                )
                request.url = self._client.format_url(request.url)

            else:
                request = HttpRequest("GET", next_link)
                request.url = self._client.format_url(request.url)

            return request

        async def extract_data(pipeline_response):
            deserialized = pipeline_response.http_response.json()
            list_of_elem = deserialized["value"]
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                if _stream:
                    await response.read()  # Load the body in memory and close the socket
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)
