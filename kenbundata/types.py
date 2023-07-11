from typing import List, Optional, TypeAlias

from pydantic import AnyHttpUrl
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, IPvAnyAddress
from pydantic.fields import Field

from .fields import Bytes, EncodedImage, Id, MimeType, Timestamp
from .utils import camelizer

IncEx: TypeAlias = "set[int] | set[str] | dict[int, IncEx] | dict[str, IncEx] | None"


class BaseModel(PydanticBaseModel):
    """
    >>> from unittest.mock import patch
    >>> from uuid import UUID
    >>> import freezegun
    >>> from datetime import timedelta, timezone, datetime
    >>> class DerivedModel(BaseModel):
    ...   id: Id = Field(default_factory=Id.generate)
    ...   object_name: str
    ...   created_at: Timestamp = Field(default_factory=Timestamp.now)
    >>> with patch("uuid.uuid4", return_value=UUID('cf57432e-809e-4353-adbd-9d5c0d733868')), \
        freezegun.freeze_time(datetime(2023, 1, 22, 14, 29, 23, 123321, tzinfo=timezone.utc)):
    ...   x = DerivedModel(object_name="test")
    >>> x
    DerivedModel(id=Id('z1dDLoCeQ1OtvZ1cDXM4aA'), object_name='test', created_at=Timestamp(1674397763123321))
    >>> x.model_dump()
    {'id': Id('z1dDLoCeQ1OtvZ1cDXM4aA'), 'object_name': 'test', 'created_at': Timestamp(1674397763123321)}
    >>> x.model_dump_json()
    '{"id":"z1dDLoCeQ1OtvZ1cDXM4aA","objectName":"test","createdAt":1674397763123321}'
    >>> DerivedModel.model_validate_json('{"id":"z1dDLoCeQ1OtvZ1cDXM4aA","objectName":"test","createdAt":1674397763123321}')
    DerivedModel(id=Id('z1dDLoCeQ1OtvZ1cDXM4aA'), object_name='test', created_at=Timestamp(1674397763123321))
    >>> with patch("uuid.uuid4", return_value= UUID('9ac80d4a-97f5-4ff2-9e68-2e62d833bf60')):
    ...   DerivedModel.model_validate_json('{"objectName":"test","createdAt":1674397763123321}')
    DerivedModel(id=Id('msgNSpf1T_KeaC5i2DO_YA'), object_name='test', created_at=Timestamp(1674397763123321))
    >>> DerivedModel.model_validate_json('{"id":"z1dDLoCeQ1OtvZ1cDXM4aA","object_name":"test","created_at":1674397763123321}')
    DerivedModel(id=Id('z1dDLoCeQ1OtvZ1cDXM4aA'), object_name='test', created_at=Timestamp(1674397763123321))
    >>> DerivedModel.model_json_schema()
    {'properties': {'id': {'format': 'base64EncodedUuid', 'title': 'Id', 'type': 'string'}, 'objectName': {'title': 'Objectname', 'type': 'string'}, 'createdAt': {'format': 'timestamp', 'title': 'Createdat', 'type': 'integer'}}, 'required': ['objectName'], 'title': 'DerivedModel', 'type': 'object'}
    """  # noqa: E501

    model_config = ConfigDict(populate_by_name=True, alias_generator=camelizer)

    def model_dump_json(
        self,
        *,
        indent: int | None = None,
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> str:
        return super(BaseModel, self).model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )


class BaseEntity(BaseModel):
    """Base entity for all entities in kenbun.
    >>> from unittest.mock import patch
    >>> from uuid import UUID
    >>> class MyEntity(BaseEntity):
    ...     name: str
    ...     url: str
    ...
    >>> with patch("uuid.uuid4", return_value=UUID('29865d64-327a-4f9a-ba73-981cadcaf86a')):
    ...     MyEntity(name="kenbun", url="https://kenbun.app")
    ...
    MyEntity(id=Id('KYZdZDJ6T5q6c5gcrcr4ag'), name='kenbun', url='https://kenbun.app')
    >>>
    """

    id: Id = Field(default_factory=Id.generate)


class TargetUrl(BaseEntity):
    """Data model represents URL
    >>> from unittest.mock import patch
    >>> from uuid import UUID
    >>> with patch("uuid.uuid4", return_value=UUID('1a2805e9-2554-4a1d-9647-3b59ee281349')):
    ...     x = TargetUrl(url="https://kenbun.app")
    ...
    >>> x
    TargetUrl(id=Id('GigF6SVUSh2WRztZ7igTSQ'), url=Url('https://kenbun.app/'))
    >>> x.model_dump()
    {'id': Id('GigF6SVUSh2WRztZ7igTSQ'), 'url': Url('https://kenbun.app/')}
    >>> x.model_dump_json()
    '{"id":"GigF6SVUSh2WRztZ7igTSQ","url":"https://kenbun.app/"}'
    """

    url: AnyHttpUrl


class Blob(BaseEntity):
    """
    >>> from unittest.mock import patch
    >>> from uuid import UUID
    >>> with patch("uuid.uuid4", return_value=UUID('e2ad3ba0-1197-4097-b26b-11461534cca5')):
    ...     x = Blob(data=b"hello world", mime_type="text/plain")
    ...
    >>> x
    Blob(id=Id('4q07oBGXQJeyaxFGFTTMpQ'), data=Bytes(b'hello world'), mime_type=MimeType('text/plain'))
    >>> x.model_dump()
    {'id': Id('4q07oBGXQJeyaxFGFTTMpQ'), 'data': Bytes(b'hello world'), 'mime_type': MimeType('text/plain')}
    >>> x.model_dump_json()
    '{"id":"4q07oBGXQJeyaxFGFTTMpQ","data":"aGVsbG8gd29ybGQ=","mimeType":"text/plain"}'
    """

    data: Bytes
    mime_type: MimeType


class Screenshot(BaseEntity):
    """Data model represents screenshot
    >>> from unittest.mock import patch
    >>> from uuid import UUID
    >>> with patch("uuid.uuid4", return_value=UUID('7287d74a-8894-4935-8c9b-0a437e59e8e2')):
    ...     x = Screenshot(encoded_image=EncodedImage("iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAAAAAC86un7AAAADElEQVR4nGP4z8QAAAMFAQLUtn8MAAAAAElFTkSuQmCC"))

    >>> x
    Screenshot(id=Id('cofXSoiUSTWMmwpDflno4g'), encoded_image=EncodedImage('iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAAAAAC86un7AAAADElEQVR4nGP4z8QAAAMFAQLUtn8MAAAAAElFTkSuQmCC'))
    >>> x.model_dump()
    {'id': Id('cofXSoiUSTWMmwpDflno4g'), 'encoded_image': EncodedImage('iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAAAAAC86un7AAAADElEQVR4nGP4z8QAAAMFAQLUtn8MAAAAAElFTkSuQmCC')}
    >>> x.model_dump_json()
    '{"id":"cofXSoiUSTWMmwpDflno4g","encodedImage":"iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAAAAAC86un7AAAADElEQVR4nGP4z8QAAAMFAQLUtn8MAAAAAElFTkSuQmCC"}'
    >>> x.encoded_image.image.size
    (1, 2)
    >>> x.encoded_image.image.format
    'PNG'
    >>> x.encoded_image.image.mode
    'L'
    """  # noqa: E501

    encoded_image: EncodedImage


class HarCreator(BaseModel):
    """
    >>> HarCreator(name='WebInspector', version='537.36')
    HarCreator(name='WebInspector', version='537.36', comment=None)
    """

    name: str
    version: str
    comment: Optional[str] = None


class HarBrowser(BaseModel):
    """
    >>> HarBrowser(name='Chrome', version='80.0.3987.132')
    HarBrowser(name='Chrome', version='80.0.3987.132', comment=None)
    """

    name: str
    version: str
    comment: Optional[str] = None


class HarPageTiming(BaseModel):
    """
    >>> HarPageTiming(on_content_load=6629, on_load=9854)
    HarPageTiming(on_content_load=6629, on_load=9854, comment=None)
    """

    on_content_load: Optional[int] = None
    on_load: Optional[int] = None
    comment: Optional[str] = None


class HarPage(BaseModel):
    """
    >>> HarPage(started_date_time='2023-03-18T16:08:48.981Z', id='page_1', title='https://www.somepage.nowhere/', page_timings={"on_content_load": 6629, "on_load": 9854})
    HarPage(started_date_time=Timestamp(1679155728981000), id='page_1', title='https://www.somepage.nowhere/', page_timings=HarPageTiming(on_content_load=6629, on_load=9854, comment=None), comment=None)
    """  # noqa: E501

    started_date_time: Timestamp
    id: str
    title: str
    page_timings: HarPageTiming
    comment: Optional[str] = None


class HarCookie(BaseModel):
    """
    >>> HarCookie(name='nothing.user.token', value='00000000-1111-2222-3333-444444444444', path='/', domain='.somepage.nowhere', expires='2024-04-21T16:08:22.665Z', http_only=False, secure=False)
    HarCookie(name='nothing.user.token', value='00000000-1111-2222-3333-444444444444', path='/', domain='.somepage.nowhere', expires=Timestamp(1713715702665000), http_only=False, secure=False, comment=None)
    """  # noqa: E501

    name: str
    value: str
    path: Optional[str] = None
    domain: Optional[str] = None
    expires: Optional[Timestamp] = None
    http_only: Optional[bool] = None
    secure: Optional[bool] = None
    comment: Optional[str] = None


class HarHeader(BaseModel):
    """
    >>> HarHeader(name=':authority', value='www.somepage.nowhere', comment=None)
    HarHeader(name=':authority', value='www.somepage.nowhere', comment=None)
    """

    name: str
    value: str
    comment: Optional[str] = None


class HarQueryString(BaseModel):
    """
    >>> HarQueryString(name='v', value='45', comment=None)
    HarQueryString(name='v', value='45', comment=None)
    """

    name: str
    value: str
    comment: Optional[str] = None


class HarParam(BaseModel):
    name: str
    value: Optional[str] = None
    file_name: Optional[str] = None
    content_type: Optional[str] = None
    comment: Optional[str] = None


class HarPostData(BaseModel):
    """
    >>> HarPostData(
    ...   mime_type='text/plain;charset=UTF-8',
    ...   params=None,
    ...   text='{"events":[],"metadata":{"client_version":"4.4.0"},"token":"xxxxxxxxxxxxxxxx","visitor_token":"00000000-1111-2222-3333-444444444444"}')
    ...
    HarPostData(mime_type=MimeType('text/plain;charset=UTF-8'), params=None, text='{"events":[],"metadata":{"client_version":"4.4.0"},"token":"xxxxxxxxxxxxxxxx","visitor_token":"00000000-1111-2222-3333-444444444444"}', comment=None)
    """  # noqa: E501

    mime_type: MimeType
    params: Optional[List[HarParam]] = None
    text: str
    comment: Optional[str] = None


class HarRequest(BaseModel):
    """
    >>> HarRequest(method='GET', url='https://cdn.somepage.nowhere/stub.js', http_version='http/2.0', cookies=[], headers=[{"name":'sec-ch-ua', "value":'"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"'}, {"name":'Referer', "value":'https://www.somepage.nowhere/'}, {"name":'sec-ch-ua-mobile', "value":'?0'}, {"name":'User-Agent', "value":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}, {"name":'sec-ch-ua-platform', "value":'"Linux"'}], query_string=[], post_data=None, headers_size=-1, body_size=0, comment=None)
    HarRequest(method='GET', url=Url('https://cdn.somepage.nowhere/stub.js', ), http_version='http/2.0', cookies=[], headers=[HarHeader(name='sec-ch-ua', value='"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"', comment=None), HarHeader(name='Referer', value='https://www.somepage.nowhere/', comment=None), HarHeader(name='sec-ch-ua-mobile', value='?0', comment=None), HarHeader(name='User-Agent', value='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', comment=None), HarHeader(name='sec-ch-ua-platform', value='"Linux"', comment=None)], query_string=[], post_data=None, headers_size=-1, body_size=0, comment=None)
    """  # noqa: E501

    method: str
    url: AnyHttpUrl
    http_version: str
    cookies: List[HarCookie]
    headers: List[HarHeader]
    query_string: List[HarQueryString]
    post_data: Optional[HarPostData] = None
    headers_size: int
    body_size: int
    comment: Optional[str] = None


class HarContent(BaseModel):
    r"""
    >>> HarContent(size=45, mime_type='application/json', text='{\n    "success": true,\n    "iso_code": "JP"\n}')
    HarContent(size=45, compression=None, mime_type=MimeType('application/json'), text='{\n    "success": true,\n    "iso_code": "JP"\n}', encoding=None, comment=None)
    """  # noqa: E501

    size: int
    compression: Optional[int] = None
    mime_type: MimeType
    text: Optional[str] = None
    encoding: Optional[str] = None
    comment: Optional[str] = None


class HarResponse(BaseModel):
    r"""
    >>> HarResponse(status=200, statusText="", httpVersion="http/2.0", headers=[{
    ...   "name": "access-control-allow-headers",
    ...   "value": "x-newrelic-id, x-requested-with"
    ... }, {
    ...   "name": "access-control-allow-methods",
    ...   "value": "GET, OPTIONS"
    ... }, {
    ...   "name": "access-control-allow-origin",
    ...   "value": "https://www.somepage.nowhere"
    ... }, {
    ...   "name": "cache-control",
    ...   "value": "no-store, max-age=0, no-cache"
    ... }, {
    ...   "name": "content-length",
    ...   "value": "45"
    ... }, {
    ...   "name": "content-type",
    ...   "value": "application/json; charset=UTF-8"
    ... }, {
    ...   "name": "date",
    ...   "value": "Sat, 18 Mar 2023 16:08:49 GMT"
    ... }, {
    ...   "name": "permissions-policy",
    ...   "value": "camera=(), geolocation=(), microphone=()"
    ... }, {
    ...   "name": "referrer-policy",
    ...   "value": "strict-origin-when-cross-origin"
    ... }, {
    ...   "name": "strict-transport-security",
    ...   "value": "max-age=31536000; includeSubDomains; preload"
    ... }, {
    ...   "name": "x-content-type-options",
    ...   "value": "nosniff"
    ... }], cookies=[], content={
    ...   "size": 45,
    ...   "mimeType": "application/json",
    ...   "text": "{\n    \"success\": true,\n    \"iso_code\": \"JP\"\n}"
    ... }, redirectURL="", headersSize=-1, bodySize=-1, _transferSize=814, _error=None)
    HarResponse(status=200, status_text='', http_version='http/2.0', cookies=[], headers=[HarHeader(name='access-control-allow-headers', value='x-newrelic-id, x-requested-with', comment=None), HarHeader(name='access-control-allow-methods', value='GET, OPTIONS', comment=None), HarHeader(name='access-control-allow-origin', value='https://www.somepage.nowhere', comment=None), HarHeader(name='cache-control', value='no-store, max-age=0, no-cache', comment=None), HarHeader(name='content-length', value='45', comment=None), HarHeader(name='content-type', value='application/json; charset=UTF-8', comment=None), HarHeader(name='date', value='Sat, 18 Mar 2023 16:08:49 GMT', comment=None), HarHeader(name='permissions-policy', value='camera=(), geolocation=(), microphone=()', comment=None), HarHeader(name='referrer-policy', value='strict-origin-when-cross-origin', comment=None), HarHeader(name='strict-transport-security', value='max-age=31536000; includeSubDomains; preload', comment=None), HarHeader(name='x-content-type-options', value='nosniff', comment=None)], content=HarContent(size=45, compression=None, mime_type=MimeType('application/json'), text='{\n    "success": true,\n    "iso_code": "JP"\n}', encoding=None, comment=None), redirect_url='', headers_size=-1, body_size=-1, comment=None)
    """  # noqa: E501
    status: int
    status_text: str
    http_version: str
    cookies: List[HarCookie]
    headers: List[HarHeader]
    content: HarContent
    redirect_url: str
    headers_size: int
    body_size: int
    comment: Optional[str] = None


class HarCacheRequest(BaseModel):
    """
    >>> HarCacheRequest(expires="2009-04-16T15:50:36", lastAccess="2009-02-16T15:50:34", eTag="", hitCount=0, comment="")
    HarCacheRequest(expires=Timestamp(1239864636000000), last_access=Timestamp(1234767034000000), e_tag='', hit_count=0, comment='')
    """  # noqa: E501

    expires: Optional[Timestamp] = None
    last_access: Timestamp
    e_tag: str
    hit_count: int
    comment: Optional[str] = None


class HarCache(BaseModel):
    """
    >>> HarCache(beforeRequest=None, afterRequest=None, comment="")
    HarCache(before_request=None, after_request=None, comment='')
    """

    before_request: Optional[HarCacheRequest] = None
    after_request: Optional[HarCacheRequest] = None
    comment: Optional[str] = None


class HarTiming(BaseModel):
    """
    >>> HarTiming(blocked=1, dns=-1, connect=-1, send=0, wait=312, receive=274, ssl=-1)
    HarTiming(blocked=1, dns=-1, connect=-1, send=0, wait=312, receive=274, ssl=-1, comment=None)
    """

    blocked: Optional[int] = None
    dns: Optional[int] = None
    connect: Optional[int] = None
    send: int
    wait: int
    receive: int
    ssl: Optional[int] = None
    comment: Optional[str] = None


class HarEntry(BaseModel):
    r"""
    >>> HarEntry(
    ...   pageref="page_1",
    ...   started_date_time="2023-03-19T01:35:06.638Z",
    ...   time=3,
    ...   request={
    ...     "method": "GET",
    ...     "url": "https://developer.mozilla.org/manifest.56b1cedc.json",
    ...     "http_version": "http/2.0",
    ...     "cookies": [],
    ...     "headers": [],
    ...     "query_string": [],
    ...     "headers_size": -1,
    ...     "body_size": 0
    ...   },
    ...   response={
    ...     "status": 200,
    ...     "status_text": "",
    ...     "http_version": "http/2.0",
    ...     "cookies": [],
    ...     "headers": [{
    ...       "name": "age",
    ...       "value": "15336"
    ...     }, {
    ...       "name": "cache-control",
    ...       "value": "max-age=31536000, public"
    ...     }, {
    ...       "name": "content-length",
    ...       "value": "381"
    ...     }],
    ...     "content": {
    ...       "size": 381,
    ...       "mime_type": "application/json",
    ...       "text": '{\n  "short_name": "MDN",\n}\n'
    ...     },
    ...     "redirect_url": "",
    ...     "headers_size": -1,
    ...     "body_size": 0
    ...   },
    ...   timings={
    ...     "blocked": 0,
    ...     "dns": -1,
    ...     "connect": -1,
    ...     "send": 0,
    ...     "wait": 2,
    ...     "receive": 1,
    ...     "ssl": -1
    ...   },
    ...   cache={},
    ...   server_ip_address='0.0.0.0'
    ... )
    HarEntry(pageref='page_1', started_date_time=Timestamp(1679189706638000), time=3, request=HarRequest(method='GET', url='https://developer.mozilla.org/manifest.56b1cedc.json', http_version='http/2.0', cookies=[], headers=[], query_string=[], post_data=None, headers_size=-1, body_size=0, comment=None), response=HarResponse(status=200, status_text='', http_version='http/2.0', cookies=[], headers=[HarHeader(name='age', value='15336', comment=None), HarHeader(name='cache-control', value='max-age=31536000, public', comment=None), HarHeader(name='content-length', value='381', comment=None)], content=HarContent(size=381, compression=None, mime_type=MimeType('application/json'), text='{\n  "short_name": "MDN",\n}\n', encoding=None, comment=None), redirect_url='', headers_size=-1, body_size=0, comment=None), cache=HarCache(before_request=None, after_request=None, comment=None), timings=HarTiming(blocked=0, dns=-1, connect=-1, send=0, wait=2, receive=1, ssl=-1, comment=None), server_ip_address=IPv4Address('0.0.0.0'), connection=None, comment=None)

    """  # noqa: E501
    pageref: Optional[str] = None
    started_date_time: Timestamp
    time: int
    request: HarRequest
    response: HarResponse
    cache: HarCache
    timings: HarTiming
    server_ip_address: Optional[IPvAnyAddress] = None
    connection: Optional[str] = None
    comment: Optional[str] = None


class HarRoot(BaseModel):
    r"""
    >>> HarRoot(
    ...   version="1.2",
    ...   creator={
    ...     "name": "WebInspector",
    ...     "version": "537.36"
    ...   },
    ...   pages=[{
    ...     "startedDateTime": "2023-03-19T06:36:15.430Z",
    ...     "id": "page_1",
    ...     "title": "http://localhost:8000/",
    ...     "pageTimings": {
    ...       "onContentLoad": 13.81399999999644,
    ...       "onLoad": 13.707000000010794
    ...     }
    ...   }],
    ...   entries=[{
    ...     "_initiator": {
    ...       "type": "other"
    ...     },
    ...     "_priority": "VeryHigh",
    ...     "_resourceType": "document",
    ...     "cache": {},
    ...     "connection": "445",
    ...     "pageref": "page_1",
    ...     "request": {
    ...     "method": "GET",
    ...     "url": "http://localhost:8000/",
    ...     "httpVersion": "HTTP/1.1",
    ...     "headers": [{
    ...       "name": "Accept",
    ...       "value": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    ...     }, {
    ...       "name": "Accept-Encoding",
    ...       "value": "gzip, deflate, br"
    ...     }, {
    ...       "name": "Accept-Language",
    ...       "value": "ja-JP,ja;q=0.9"
    ...     }, {
    ...       "name": "Cache-Control",
    ...       "value": "max-age=0"
    ...     }, {
    ...       "name": "Connection",
    ...       "value": "keep-alive"
    ...     }, {
    ...       "name": "Host",
    ...       "value": "localhost:8000"
    ...     }, {
    ...       "name": "Sec-Fetch-Dest",
    ...       "value": "document"
    ...     }, {
    ...       "name": "Sec-Fetch-Mode",
    ...       "value": "navigate"
    ...     }, {
    ...       "name": "Sec-Fetch-Site",
    ...       "value": "none"
    ...     }, {
    ...       "name": "Sec-Fetch-User",
    ...       "value": "?1"
    ...     }, {
    ...       "name": "Upgrade-Insecure-Requests",
    ...       "value": "1"
    ...     }, {
    ...       "name": "User-Agent",
    ...       "value": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    ...     }, {
    ...       "name": "sec-ch-ua",
    ...       "value": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\""
    ...     }, {
    ...       "name": "sec-ch-ua-mobile",
    ...       "value": "?0"
    ...     }, {
    ...       "name": "sec-ch-ua-platform",
    ...       "value": "\"Linux\""
    ...     }],
    ...     "queryString": [],
    ...     "cookies": [],
    ...     "headersSize": 669,
    ...     "bodySize": 0
    ...   },
    ...   "response": {
    ...     "status": 200,
    ...     "statusText": "OK",
    ...     "httpVersion": "HTTP/1.0",
    ...     "headers": [{
    ...       "name": "Content-Length",
    ...       "value": "934"
    ...     }, {
    ...       "name": "Content-type",
    ...       "value": "text/html; charset=utf-8"
    ...     }, {
    ...       "name": "Date",
    ...       "value": "Sun, 19 Mar 2023 06:36:15 GMT"
    ...     }, {
    ...       "name": "Server",
    ...       "value": "SimpleHTTP/0.6 Python/3.10.10"
    ...     }],
    ...     "cookies": [],
    ...     "content": {
    ...       "size": 934,
    ...       "mimeType": "text/html",
    ...       "compression": 0,
    ...       "text": "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">\n<html>\n<head>\n</html>\n"
    ...     },
    ...     "redirectURL": "",
    ...     "headersSize": 156,
    ...     "bodySize": 934,
    ...     "_transferSize": 1090,
    ...     "_error": None
    ...   },
    ...   "serverIPAddress": "127.0.0.1",
    ...   "startedDateTime": "2023-03-19T06:36:15.428Z",
    ...   "time": 5.0220000000062015,
    ...   "timings": {
    ...     "blocked": 2.073000000002765,
    ...     "dns": 0.015000000000000013,
    ...     "ssl": -1,
    ...     "connect": 0.40700000000000003,
    ...     "send": 0.16400000000000003,
    ...     "wait": 1.6620000000111448,
    ...     "receive": 0.7009999999922911,
    ...     "_blocked_queueing": 1.7100000000027649
    ...   }
    ... }])
    HarRoot(version='1.2', creator=HarCreator(name='WebInspector', version='537.36', comment=None), browser=None, pages=[HarPage(started_date_time=Timestamp(1679207775430000), id='page_1', title='http://localhost:8000/', page_timings=HarPageTiming(on_content_load=13, on_load=13, comment=None), comment=None)], entries=[HarEntry(pageref='page_1', started_date_time=Timestamp(1679207775428000), time=5, request=HarRequest(method='GET', url=Url('http://localhost:8000/', ), http_version='HTTP/1.1', cookies=[], headers=[HarHeader(name='Accept', value='text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', comment=None), HarHeader(name='Accept-Encoding', value='gzip, deflate, br', comment=None), HarHeader(name='Accept-Language', value='ja-JP,ja;q=0.9', comment=None), HarHeader(name='Cache-Control', value='max-age=0', comment=None), HarHeader(name='Connection', value='keep-alive', comment=None), HarHeader(name='Host', value='localhost:8000', comment=None), HarHeader(name='Sec-Fetch-Dest', value='document', comment=None), HarHeader(name='Sec-Fetch-Mode', value='navigate', comment=None), HarHeader(name='Sec-Fetch-Site', value='none', comment=None), HarHeader(name='Sec-Fetch-User', value='?1', comment=None), HarHeader(name='Upgrade-Insecure-Requests', value='1', comment=None), HarHeader(name='User-Agent', value='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', comment=None), HarHeader(name='sec-ch-ua', value='"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"', comment=None), HarHeader(name='sec-ch-ua-mobile', value='?0', comment=None), HarHeader(name='sec-ch-ua-platform', value='"Linux"', comment=None)], query_string=[], post_data=None, headers_size=669, body_size=0, comment=None), response=HarResponse(status=200, status_text='OK', http_version='HTTP/1.0', cookies=[], headers=[HarHeader(name='Content-Length', value='934', comment=None), HarHeader(name='Content-type', value='text/html; charset=utf-8', comment=None), HarHeader(name='Date', value='Sun, 19 Mar 2023 06:36:15 GMT', comment=None), HarHeader(name='Server', value='SimpleHTTP/0.6 Python/3.10.10', comment=None)], content=HarContent(size=934, compression=0, mime_type=MimeType('text/html'), text='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n<html>\n<head>\n</html>\n', encoding=None, comment=None), redirect_url='', headers_size=156, body_size=934, comment=None), cache=HarCache(before_request=None, after_request=None, comment=None), timings=HarTiming(blocked=2, dns=0, connect=0, send=0, wait=1, receive=0, ssl=-1, comment=None), server_ip_address=IPv4Address('127.0.0.1'), connection='445', comment=None)], comment=None)
    """  # noqa: E501
    version: str
    creator: HarCreator
    browser: Optional[HarBrowser] = None
    pages: Optional[List[HarPage]] = None
    entries: List[HarEntry]
    comment: Optional[str] = None


class Har(BaseEntity):
    log: HarRoot
