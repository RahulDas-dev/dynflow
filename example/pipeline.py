import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from dynflow.config import Config

from .base import BaseComponent, registry

logger = logging.getLogger(__name__)


class Pipeline:
    _components: List[Tuple[str, BaseComponent, Dict, bool]]

    def __init__(
        self,
        components: Optional[List[Tuple[str, BaseComponent]]] = None,
        disable: Optional[List[str]] = None,
    ):
        self._components = [] if components is None else components
        self._disabled = [] if disable is None else disable

    @classmethod
    def load(cls, config_path: Union[Path, str, Config]) -> "Pipeline":
        if isinstance(config_path, (Path, str)):
            config_path_ = Path(config_path)
            if config_path_.is_file():
                config = Config.from_disk(config_path_)
            else:
                raise ValueError("The load function expects a Config or a path to a config file")
        elif not isinstance(config, Config):
            raise ValueError("The load function expects a Config or a path to a config file")
        return Pipeline.from_config(config)

    @classmethod
    def from_config(cls, config: Config, disable: Optional[Set[str]] = None) -> "Pipeline":
        config_ = Config(**config).copy()
        disable_ = disable if disable is not None else set()
        if "pipeline" not in config_:
            raise ValueError("Config must contain a 'pipeline' key")
        component_names = config_["pipeline"].get("components", [])
        pipeline = Pipeline()
        for name in component_names:
            disabled = name in disable_
            pipeline.add_component(config_[f"component.{name}"], name, disabled)
        return pipeline

    @property
    def component_names(self) -> List[str]:
        return [name for name, _, _, _ in self._components]

    def __repr__(self):
        components = " -> ".join([str(c) for _, c in self._components])
        return f"Pipeline[ components = \n{components}\n]"

    def add_component(self, component_cfg: Dict, name: str, disabled: bool = False) -> BaseComponent:
        factory = component_cfg.get("factory")
        component = registry.get_component(factory, **component_cfg.get("init_args", {}))
        self._components.append((name, component, component_cfg.get("run_args", {}), disabled))
        return component

    def run(self) -> None:
        for name, component, run_args, disabled in self._components:
            logger.info(f"{name} Started Processing ...")
            if disabled:
                continue
            component.run(**run_args)
