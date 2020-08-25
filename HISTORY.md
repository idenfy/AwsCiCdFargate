# Release history

#### 7.3.0
Add md files.

#### 7.2.0
AWS CDK dependency update 1.60.0 - 2.0.0.

#### 7.1.0
Force dependency update 1.44.0 AWS CDK.

#### 7.0.0
Do not allow to specify ecs port. Default to 80.
This is AWS limitation.

#### 6.0.0
Instead of taking path config as a parameter, take the 
whole rule config.

#### 5.0.1
Use empty ecs repository dependency.

#### 5.0.0
Project rename to a better and more explanatory name.

#### 4.0.9
Dependency update.

#### 4.0.8
Dependency update. Fix ecs service name key.

#### 4.0.7
Dependency update.

#### 4.0.6
Use newest cdk with newest breaking changes.

#### 4.0.5
Add dependency which creates ecs service. CloudFormation itself
has too many bugs.

#### 4.0.2
Destroy ecr on delete.

#### 4.0.0
Build environment variable fix.

#### 4.0.0
Add pipeline parameters and fix some major pipeline bugs.

#### 3.1.0
Create custom resource to create ecs service. With deployment controller CODE_DEPLOY you
can not do CF updates.

#### 3.0.2
Minor bug fix.

#### 3.0.1
Readme fix.

#### 3.0.0
Full project refactor. Accept loadbalancer's listeners for production and test traffic instead of creting
a loadbalancer here. This way we can reuse an existing loadbalancer.

#### 2.0.0
Remove pipeline parameters as the artifacts bucket should be created automatically within this stack.

#### 1.0.0
Initial project.
