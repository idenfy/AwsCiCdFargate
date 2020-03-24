from typing import Optional, Dict, Any


class PipelineParams:
    def __init__(
            self,
            build_environment: Optional[Dict[str, Any]] = None,
            docker_build_args: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Constructor.

        :param build_environment: Environment variables for a build step. You can put here various config
        parameters, urls, secrets, etc.
        :param docker_build_args: Build arguments for docker build command.
        """
        self.build_environment: Dict[str, Any] = build_environment or {}
        self.docker_build_args: Dict[str, str] = docker_build_args or {}
