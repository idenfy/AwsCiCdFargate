from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='aws_fargate_cdk',
    version='2.0.0',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(exclude=['venv', 'test']),
    description=(
        'AWS CDK package that helps deploying a fargate service.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'aws_cdk.core',
        'aws_cdk.aws_iam',
        'aws_cdk.custom_resources',
        'aws_cdk.aws_s3',
        'aws_cdk.aws_certificatemanager',
        'aws_cdk.aws_elasticloadbalancingv2',
        'aws_cdk.aws_ec2',
        'aws_cdk.aws_logs',
        'aws_cdk.aws_ecs',
        'aws_cdk.aws_applicationautoscaling',
        'aws_cdk.aws_codedeploy',
        'aws_cdk.aws_codecommit',
        'aws_cdk.aws_codepipeline',
        'aws_cdk.aws_codepipeline_actions',
        'aws_cdk.aws_ecr',
        'aws_cdk.aws_codebuild',
        'aws-empty-bucket>=2.0.1,<3.0.0',
        'aws-vpc>=2.0.0,<3.0.0'
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
