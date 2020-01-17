from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='aws_fargate_sdk',
    version='1.0.0',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(exclude=['venv', 'test']),
    description=(
        'AWS CDK package that helps deploying a fargate service.'
    ),
    long_description=README,
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
    ],
    author='Deividas Tamkus, Laimonas Sutkus',
    author_email='dtamkus@gmail.com, laimonas.sutkus@gmail.com',
    keywords='AWS CDK Fargate ECS',
    url='https://github.com/laimonassutkus/AwsFargateSdk.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)