#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart

from kubeasy import Deployment
from kubeasy import Service


class MyChart(Chart):
    def __init__(self, scope: Construct, name: str):
        super().__init__(scope, name)

        name = "hello-k8s"
        image = "paulbouwer/hello-kubernetes"
        release = "1.7"
        environment = "stg"
        replicas = 2

        deployment = Deployment(name=name, image=image, tag=release, environment=environment) \
            .set_replicas(replicas) \
            .render(self)

        Service("custom_service", deployment, release, environment) \
            .set_port(80)   \
            .set_target(80) \
            .render(self)


app = App()
MyChart(app, "cdk8s_test")

app.synth()

type(app)
