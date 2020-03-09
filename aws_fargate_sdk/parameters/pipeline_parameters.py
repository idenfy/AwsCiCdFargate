from typing import Optional, Dict, Any


class PipelineParams:
    def __init__(
            self,
            build_environment: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Constructor.

        :param build_environment: Environment variables for a build step. You can put here various config
        parameters, urls, secrets, etc.
        """
        self.build_environment: Dict[str, Any] = build_environment or {}
