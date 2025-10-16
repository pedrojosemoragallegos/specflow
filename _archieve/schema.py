from __future__ import annotations

import re
from typing import TYPE_CHECKING
from urllib.parse import urlparse

if TYPE_CHECKING:
    from specflow.typing import JSONValue


class Schema:
    def __init__(  # noqa: C901, PLR0912, PLR0915
        self,
        id_: str | None = None,
        schema: str | None = None,
        ref: str | None = None,
        dynamic_ref: str | None = None,
        recursive_ref: str | None = None,
        definitions: dict[str, Schema] | None = None,
        defs: dict[str, Schema] | None = None,
        comment: str | None = None,
        anchor: str | None = None,
        dynamic_anchor: str | None = None,
        vocabulary: dict[str, bool]
        | None = None,  # NOTE: should only appear in meta-schemas (root schemas defining JSON Schema dialects), not regular schemas
        title: str | None = None,
        description: str | None = None,
        *,
        recursive_anchor: bool | None = None,
        deprecated: bool | None = None,
        read_only: bool | None = None,
        write_only: bool | None = None,
    ) -> None:
        if id_ is not None:
            if not isinstance(id_, str) or not id_.strip():  # type: ignore
                raise ValueError("$id must be a non-empty string")
            if not self._is_valid_uri(id_):
                raise ValueError(f"$id must be a valid URI: {id_}")

        if schema is not None:
            if not isinstance(schema, str) or not schema.strip():  # type: ignore
                raise ValueError("$schema must be a non-empty string")
            if not self._is_valid_uri(schema):
                raise ValueError(f"$schema must be a valid URI: {schema}")

        if (
            (ref is not None and dynamic_ref is not None)
            or (ref is not None and recursive_ref is not None)
            or (dynamic_ref is not None and recursive_ref is not None)
        ):
            raise ValueError(
                "Only one reference type allowed: $ref, $dynamicRef, or $recursiveRef",
            )

        if ref is not None:
            if not isinstance(ref, str) or not ref.strip():  # type: ignore
                raise ValueError("$ref must be a non-empty string")
            if not self._is_valid_uri_reference(ref):
                raise ValueError(f"$ref must be a valid URI reference: {ref}")

        if dynamic_ref is not None:
            if not isinstance(dynamic_ref, str) or not dynamic_ref.strip():  # type: ignore
                raise ValueError("$dynamicRef must be a non-empty string")
            if not self._is_valid_uri_reference(dynamic_ref):
                raise ValueError(
                    f"$dynamicRef must be a valid URI reference: {dynamic_ref}",
                )

        if recursive_ref is not None:
            if not isinstance(recursive_ref, str) or not recursive_ref.strip():  # type: ignore
                raise ValueError("$recursiveRef must be a non-empty string")
            if not self._is_valid_uri_reference(recursive_ref):
                raise ValueError(
                    f"$recursiveRef must be a valid URI reference: {recursive_ref}",
                )

        if (
            (anchor is not None and dynamic_anchor is not None)
            or (anchor is not None and recursive_anchor is not None)
            or (dynamic_anchor is not None and recursive_anchor is not None)
        ):
            raise ValueError(
                "Only one anchor type allowed: $anchor, $dynamicAnchor, or $recursiveAnchor",
            )

        if anchor is not None:
            if not isinstance(anchor, str) or not anchor.strip():  # type: ignore
                raise ValueError("$anchor must be a non-empty string")
            if not self._is_valid_anchor(anchor):
                raise ValueError(
                    f"$anchor must be a valid fragment identifier (no '#'): {anchor}",
                )

        if dynamic_anchor is not None:
            if not isinstance(dynamic_anchor, str) or not dynamic_anchor.strip():  # type: ignore
                raise ValueError("$dynamicAnchor must be a non-empty string")
            if not self._is_valid_anchor(dynamic_anchor):
                raise ValueError(
                    f"$dynamicAnchor must be a valid fragment identifier (no '#'): {dynamic_anchor}",
                )

        if (recursive_anchor is not None) and not isinstance(recursive_anchor, bool):  # type: ignore
            raise ValueError("$recursiveAnchor must be a boolean")

        if vocabulary is not None:
            if not isinstance(vocabulary, dict):  # type: ignore
                raise ValueError("$vocabulary must be a dictionary")
            for uri, required in vocabulary.items():
                if not isinstance(uri, str) or not uri.strip():  # type: ignore
                    raise ValueError("$vocabulary keys must be non-empty URI strings")
                if not self._is_valid_uri(uri):
                    raise ValueError(f"$vocabulary key must be a valid URI: {uri}")
                if not isinstance(required, bool):  # type: ignore
                    raise TypeError(f"$vocabulary values must be boolean: {uri}")

        if (read_only is True) and (write_only is True):
            raise ValueError("Schema cannot be both readOnly and writeOnly")

        if read_only is not None and not isinstance(read_only, bool):  # type: ignore
            raise ValueError("readOnly must be a boolean")

        if write_only is not None and not isinstance(write_only, bool):  # type: ignore
            raise ValueError("writeOnly must be a boolean")

        if (definitions is not None) and (defs is not None):
            raise ValueError(
                "Use either 'definitions' (draft-07) or '$defs' (2019-09+), not both",
            )

        if definitions is not None:
            if not isinstance(definitions, dict):  # type: ignore
                raise ValueError("definitions must be a dictionary")
            for key in definitions:
                if not isinstance(key, str) or not key.strip():  # type: ignore
                    raise ValueError("definitions keys must be non-empty strings")

        if defs is not None:
            if not isinstance(defs, dict):  # type: ignore
                raise ValueError("$defs must be a dictionary")
            for key in defs:
                if not isinstance(key, str) or not key.strip():  # type: ignore
                    raise ValueError("$defs keys must be non-empty strings")

        self._id_ = id_
        self._schema = schema
        self._ref = ref
        self._dynamic_ref = dynamic_ref
        self._recursive_ref = recursive_ref
        self._definitions = definitions
        self._defs = defs
        self._comment = comment
        self._anchor = anchor
        self._dynamic_anchor = dynamic_anchor
        self._recursive_anchor = recursive_anchor
        self._vocabulary = vocabulary
        self._title = title
        self._description = description
        self._deprecated = deprecated
        self._read_only = read_only
        self._write_only = write_only

    @staticmethod
    def _is_valid_uri(uri: str) -> bool:
        try:
            return bool(urlparse(uri))
        except Exception:  # noqa: BLE001
            return False

    @staticmethod
    def _is_valid_uri_reference(uri_ref: str) -> bool:
        try:
            urlparse(uri_ref)
            return True  # noqa: TRY300
        except Exception:  # noqa: BLE001
            return False

    @staticmethod
    def _is_valid_anchor(anchor: str) -> bool:
        if "#" in anchor:
            return False

        return bool(
            re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", anchor),
        )  # TODO: pre-compile for performance

    def to_dict(self) -> dict[str, JSONValue]:  # noqa: C901, PLR0912
        result: dict[str, JSONValue] = {}

        if self._id_ is not None:
            result["$id"] = self._id_
        if self._schema is not None:
            result["$schema"] = self._schema
        if self._ref is not None:
            result["$ref"] = self._ref
        if self._dynamic_ref is not None:
            result["$dynamicRef"] = self._dynamic_ref
        if self._recursive_ref is not None:
            result["$recursiveRef"] = self._recursive_ref
        if self._definitions is not None:
            result["definitions"] = {
                key: value.to_dict() if isinstance(value, Schema) else value  # type: ignore
                for key, value in self._definitions.items()
            }
        if self._defs is not None:
            result["$defs"] = {
                key: value.to_dict() if isinstance(value, Schema) else value  # type: ignore
                for key, value in self._defs.items()
            }
        if self._comment is not None:
            result["$comment"] = self._comment
        if self._anchor is not None:
            result["$anchor"] = self._anchor
        if self._dynamic_anchor is not None:
            result["$dynamicAnchor"] = self._dynamic_anchor
        if self._recursive_anchor is not None:
            result["$recursiveAnchor"] = self._recursive_anchor
        if self._vocabulary is not None:
            result["$vocabulary"] = self._vocabulary
        if self._title is not None:
            result["title"] = self._title
        if self._description is not None:
            result["description"] = self._description
        if self._deprecated is not None:
            result["deprecated"] = self._deprecated
        if self._read_only is not None:
            result["readOnly"] = self._read_only
        if self._write_only is not None:
            result["writeOnly"] = self._write_only

        return result
