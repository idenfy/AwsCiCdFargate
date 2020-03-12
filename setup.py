from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='aws_fargate_cdk',
    version='4.0.6',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(exclude=['venv', 'test']),
    description=(
        'AWS CDK package that helps deploying a fargate service.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'aws_cdk.core>=1.27.0,<1.28.0',
        'aws_cdk.aws_iam>=1.27.0,<1.28.0',
        'aws_cdk.custom_resources>=1.27.0,<1.28.0',
        'aws_cdk.aws_s3>=1.27.0,<1.28.0',
        'aws_cdk.aws_certificatemanager>=1.27.0,<1.28.0',
        'aws_cdk.aws_elasticloadbalancingv2>=1.27.0,<1.28.0',
        'aws_cdk.aws_ec2>=1.27.0,<1.28.0',
        'aws_cdk.aws_logs>=1.27.0,<1.28.0',
        'aws_cdk.aws_ecs>=1.27.0,<1.28.0',
        'aws_cdk.aws_applicationautoscaling>=1.27.0,<1.28.0',
        'aws_cdk.aws_codedeploy>=1.27.0,<1.28.0',
        'aws_cdk.aws_codecommit>=1.27.0,<1.28.0',
        'aws_cdk.aws_codepipeline>=1.27.0,<1.28.0',
        'aws_cdk.aws_codepipeline_actions>=1.27.0,<1.28.0',
        'aws_cdk.aws_ecr>=1.27.0,<1.28.0',
        'aws_cdk.aws_codebuild>=1.27.0,<1.28.0',
        'aws-empty-bucket>=2.0.1,<3.0.0',
        'aws-vpc>=2.0.0,<3.0.0',
        'aws_ecs_service>=1.0.4,<2.0.0'
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
