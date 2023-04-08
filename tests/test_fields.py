from kenbundata.fields import MimeType


def test_mime_type() -> None:
    from .fixtures.fields_fixture import possible_mime_types

    for mt in possible_mime_types:
        _ = MimeType(mt)
