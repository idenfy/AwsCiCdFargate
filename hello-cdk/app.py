#!/usr/bin/env python3

from aws_cdk import core
from hello_cdk.hello_cdk_stack import MySubStack

app = core.App()

mystack = MySubStack(app, "MySubStack", 'google.com')

app.synth()
