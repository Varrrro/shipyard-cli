"""
The task model.
"""

from dataclasses import field
from typing import ClassVar, List, Optional, Type

from marshmallow import Schema
from marshmallow_dataclass import NewType, dataclass
from shipyard_cli.fields import ObjectId
from shipyard_cli.validators import validate_devices

objectid = NewType('objectid', str, ObjectId)


@dataclass(order=True)
class Task:
    """A real-time task that can be deployed as a container to a node."""

    _id: Optional[objectid] = field(metadata={'required': False})
    file_id: Optional[objectid] = field(metadata={'required': False})
    name: Optional[str] = field(metadata={'required': False})
    runtime: Optional[int] = field(metadata={'required': False})
    deadline: Optional[int] = field(metadata={'required': False})
    period: Optional[int] = field(metadata={'required': False})
    devices: List[str] = field(default_factory=lambda: [], metadata={
        'required': False,
        'validate': validate_devices
    })
    capabilities: List[str] = field(default_factory=lambda: [], metadata={
        'required': False
    })

    Schema: ClassVar[Type[Schema]] = Schema
