#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart

from imports import k8s


class MyChart(Chart):
    def __init__(self, scope: Construct, name: str):
        super().__init__(scope, name)

        # define resources here
        label = {"app": "hello-k8s"}
        label_selector = k8s.LabelSelector(match_labels=label)

        svc_port = k8s.ServicePort(port=80, target_port=k8s.IntOrString.from_number(8080))
        k8s.Service(self, 'service', spec=k8s.ServiceSpec(type='LoadBalancer', ports=[svc_port], selector=label))

        dep_port = k8s.ContainerPort(container_port=8080)
        dep_container = k8s.Container(name='hello-k8s', image='paulbouwer/hello-kubernetes:1.7', ports=[dep_port])
        dep_podspec = k8s.PodSpec(containers=[dep_container])
        dep_podspectemplate = k8s.PodTemplateSpec(metadata=k8s.ObjectMeta(labels=label), spec=dep_podspec)
        dep_spec = k8s.DeploymentSpec(replicas=2, selector=label_selector, template=dep_podspectemplate)
        k8s.Deployment(self, 'deployment', spec=dep_spec)


app = App()
MyChart(app, "cdk8s_test")

app.synth()
