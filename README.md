## AWS Fargate SDK

A library that creates a full out-of-the-box solution for ECS Fargate with CI/CD pipeline.

#### Remarks

The project is written by [Deividas Tamkus](https://github.com/deitam), supervised by 
[Laimonas Sutkus](https://github.com/laimonassutkus) and is owned by 
[iDenfy](https://github.com/idenfy). This is an open source
library intended to be used by anyone. [iDenfy](https://github.com/idenfy) aims
to share its knowledge and educate market for better and more secure IT infrastructure.

#### Related technology

This project utilizes the following technology:

- *AWS* (Amazon Web Services).
- *AWS CDK* (Amazon Web Services Cloud Development Kit).
- *AWS CloudFormation*.
- *AWS Loadbalancer*.
- *AWS ECS* (Amazon Web Services Elastic Container Service).
- *AWS Fargate* (Serverless solution for ECS).
- *AWS CodePipeline*.

#### Assumptions

This library project assumes the following:

- You have knowledge in AWS (Amazon Web Services).
- You have knowledge in AWS CloudFormation and AWS loadbalancing.
- You are managing your infrastructure with AWS CDK.
- You are writing AWS CDK templates with a python language.

#### Install

The project is built and uploaded to PyPi. Install it by using pip.

```bash
pip install aws-fargate-cdk
```

Or directly install it through source.

```bash
./build.sh -ic
```

### Description

This package creates a Fargate service with autoscaling, a load balancer and two pipelines 
for a complete out-of-the-box hosting infrastructure.

The pipelines are as follows:

1. **ECR to ECS**. This pipeline takes an image pushed to ECR and deploys it to Fargate using Blue/Green deployment.
The pipeline needs to be triggered manually duo to AWS CloudWatch event bugs related to ECR.
2. **CodeCommit to ECR**. This pipeline takes code pushed to the master branch of a CodeCommit repository, builds an image out of it (_source code needs a Dockerfile_), pushes it to ECR and automatically triggers the first pipeline, which then deploys it to ECS.

**TL;DR** Pushing source code with a Dockerfile to CodeCommit repository deploys it to ECS Fargate.

### Examples

To create a full infrastructure around ECS Fargate, use the following code below in your stack.

```python
from aws_cdk import core, aws_ec2, aws_elasticloadbalancingv2
from aws_fargate_sdk.parameters.ecs_parameters import EcsParams
from aws_fargate_sdk.parameters.load_balancer_parameters import LoadBalancerParams
from aws_fargate_sdk.parameters.lb_listener_parameters import LbListenerParameters
from aws_fargate_sdk.ecs_fargate_with_ci_cd import EcsFargateWithCiCd

class MainStack(core.Stack):
    def __init__(self, scope: core.App) -> None:
        super().__init__(
            scope=scope,
            id='MyCoolStack'
        )

        # Create your own vpc or use an existing one.
        vpc = aws_ec2.Vpc(...)
        
        # Create a security group for your ECS Fargate instances.
        sg = aws_ec2.SecurityGroup(...)
        
        # Create a loadbalancer.
        loadbalancer = aws_elasticloadbalancingv2.ApplicationLoadBalancer(...)
        production_listener = aws_elasticloadbalancingv2.ApplicationListener(self, 'Prod', load_balancer=loadbalancer)
        deployments_listener = aws_elasticloadbalancingv2.ApplicationListener(self, 'Test', load_balancer=loadbalancer)
        
        ecs_params = EcsParams('FargateEcsContainer', 256, 512, 80, {}, [sg], vpc.private_subnets)
        load_params = LoadBalancerParams()
        listener_params = LbListenerParameters(
            production_listener=production_listener,
            production_listener_path='/*',
            production_listener_rule_priority=100,
            deployment_listener=deployments_listener,
            deployment_listener_path='/*',
            deployment_listener_rule_priority=100
        )

        self.ecs_infrastructure = EcsFargateWithCiCd(
            scope=self,
            prefix='MyCool',
            vpc=vpc,
            lb_params=load_params,
            ecs_params=ecs_params,
            lb_listener_params=listener_params
        )
        
        # Access CodeCommit-To-Ecr pipeline.
        _ = self.ecs_infrastructure.pipeline.commit_to_ecr
        
        # Access Ecr-To-Ecs pipeline.
        _ = self.ecs_infrastructure.pipeline.ecr_to_ecs
```
