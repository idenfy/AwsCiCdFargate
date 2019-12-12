from aws_cdk import core, aws_ecs, aws_logs


class CodeStarStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str) -> None:
        super().__init__(scope, id)

        self.log_group = aws_logs.LogGroup(
            self, 'FargateEcsLogGroup',
            log_group_name=f'/aws/ecs/fargate/prefix'
        )

        self.task = aws_ecs.FargateTaskDefinition(
            self, 'FargateEcsTaskDefinition',
            cpu=256, memory_limit_mib=512, family='prefix',

        )
        self.container = self.task.add_container(
            'container_name',
            image=aws_ecs.ContainerImage.from_registry('nginx:latest'),
            logging=aws_ecs.AwsLogDriver(stream_prefix='prefix', log_group=self.log_group)
        )
        self.container.add_port_mappings(aws_ecs.PortMapping(container_port=80))
        print(self.task)


app = core.App()

mystack = CodeStarStack(app, "MySubStack")
