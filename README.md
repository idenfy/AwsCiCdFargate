## AWS Fargate SDK
A package used to deploy a fargate service to ECS.

### Description

This package creates a Fargate service with autoscaling, a load balancer and two pipelines.

The pipelines are as follows:

1. ECR to ECS. This pipeline takes an image pushed to ECR and deploys it to Fargate using Blue/Green deployment.
The pipeline needs to be triggered manually duo to AWS CloudWatch event bugs related to ECR.
2. CodeCommit to ECR to first pipeline. This pipeline takes code pushed to the master branch of a CodeCommit repository, builds an image out of it (source code needs a Dockerfile), pushes it to ECR and automatically triggers the first pipeline, which then deploys it to ECS.

TL;DR Pushing code with a Dockerfile to CodeCommit deploys it to ECS

### Prerequisites

In order to operate the package, you must first install it, using
 
```pip install aws-fargate-sdk```

You also need to have an AWS account with a confugured AWS CLI. Here's how to do it:

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

### How to use

Import the main file into your project and call the Main classes constructor in your own cdk stack.

The parameters for the main class include your scope, project prefix, VPC, load balancer parameters, ecs parameters and aws region.

Load balancer paramaters include subnets, security groups, dns name for certificate and list of http codes to be considered healthy for health check.

Ecs parameters include container name, container cpu, container ram, container port, container environment variables, security groups and subnets for your service.

Read more on all parameters in their corresponding class docstrings.

Your code should look something like this:
```python
import jsii
from aws_cdk import core, aws_iam, aws_ec2
from aws_vpc.aws_cdk.vpc_template import VpcTemplate
from aws_fargate_sdk.main import Main
from aws_fargate_sdk.parameters.ecs_parameters import EcsParams
from aws_fargate_sdk.parameters.load_balancer_parameters import LoadBalancerParams

@jsii.implements(core.IAspect)
class Permissions:

    def visit(self, node: core.IConstruct) -> None:
        if isinstance(node, aws_iam.Role):
            node.add_to_policy(
                aws_iam.PolicyStatement(
                    actions=["iam:PassRole"],
                    resources=['*'],
                    effect=aws_iam.Effect.ALLOW
                )
            )


class AwsCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc_stack = VpcTemplate('prefix', self)

        vpc = vpc_stack.vpc

        self.node.apply_aspect(Permissions())

        security_group = aws_ec2.SecurityGroup(
            self, 'FargateEcsSecurityGroup',
            vpc=vpc, allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            aws_ec2.Peer.any_ipv4(),
            connection=aws_ec2.Port(
                protocol=aws_ec2.Protocol.ALL,
                string_representation='FargateEcsSecurityGroupIngressRule',
                from_port=-1,
                to_port=-1
            )
        )

        groups = [
            security_group
        ]

        pub_subnets = vpc.public_subnets
        pri_subnets = vpc.private_subnets

        ecs_params = EcsParams('FargateEcsContainer', '256', '512', 80, {}, ecs_security_groups=groups, ecs_subnets=pri_subnets)
        load_params = LoadBalancerParams(pub_subnets, groups, 'myweb.com')

        self.main = Main(self, 'ProjectPrefix', vpc, load_params, ecs_params, 'your-preferred-aws-region')
```
Notes:
1. In the example we use the aws-vpc python package to create the VPC, but you can use any VPC object.
2. Your stack requires permissions to pass role to create these resources, this is accomplished using aspects and can be seen in the example.