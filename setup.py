from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='aws_ci_cd_fargate',
    version='7.1.0',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(exclude=['venv', 'test']),
    description=(
        'AWS CDK package that helps deploying a fargate service with ci/cd.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        # AWS CDK dependencies.
        'aws_cdk.core>=1.44.0,<1.50.0',
        'aws_cdk.aws_iam>=1.44.0,<1.50.0',
        'aws_cdk.custom_resources>=1.44.0,<1.50.0',
        'aws_cdk.aws_s3>=1.44.0,<1.50.0',
        'aws_cdk.aws_certificatemanager>=1.44.0,<1.50.0',
        'aws_cdk.aws_elasticloadbalancingv2>=1.44.0,<1.50.0',
        'aws_cdk.aws_ec2>=1.44.0,<1.50.0',
        'aws_cdk.aws_logs>=1.44.0,<1.50.0',
        'aws_cdk.aws_ecs>=1.44.0,<1.50.0',
        'aws_cdk.aws_applicationautoscaling>=1.44.0,<1.50.0',
        'aws_cdk.aws_codedeploy>=1.44.0,<1.50.0',
        'aws_cdk.aws_codecommit>=1.44.0,<1.50.0',
        'aws_cdk.aws_codepipeline>=1.44.0,<1.50.0',
        'aws_cdk.aws_codepipeline_actions>=1.44.0,<1.50.0',
        'aws_cdk.aws_ecr>=1.44.0,<1.50.0',
        'aws_cdk.aws_codebuild>=1.44.0,<1.50.0',

        # Other dependencies.
        'aws-empty-bucket>=2.0.1,<3.0.0',
        'aws-vpc>=2.0.0,<3.0.0',
        'aws_ecs_service>=1.0.7,<2.0.0',
        'aws-ecs-cluster>=1.0.1,<2.0.0',
        'aws-empty-ecr-repository>=1.0.2,<2.0.0'
    ],
    author='Deividas Tamkus, Laimonas Sutkus',
    author_email='dtamkus@gmail.com (deividas@idenfy.com), laimonas.sutkus@gmail.com (laimonas@idenfy.com)',
    keywords='AWS CDK Fargate ECS',
    url='https://github.com/idenfy/AwsFargateCdk.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
