from typing import Any, Dict, Protocol, Tuple, runtime_checkable

from dynflow.registry import Registry


@runtime_checkable
class BaseComponent(Protocol):
    def run(self, args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any: ...


registry = Registry("ComponentRegistry", BaseComponent)


# To register a component, you can use the registry decorator:


# @registry.register("MyComponent1")
# class MyComponent1:
#    def run(self, args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
#        print("Running MyComponent with args:", args, "and kwargs:", kwargs)


# @registry.register("MyComponent2")
# class MyComponent2:
#    def run(self, args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
#        print("Running MyComponent with args:", args, "and kwargs:", kwargs)
