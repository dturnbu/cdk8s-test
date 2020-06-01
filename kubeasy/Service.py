from __future__ import annotations
from imports import k8s
from cdk8s import Chart
from enum import Enum
from kubeasy.Deployment import Deployment


class ServiceType(Enum):
  CLUSTERIP = "ClusterIP"
  LOADBALANCER = "LoadBalancer"
  NODEPORT = "NodePort"

  def k8s_name(self) -> str:
    return '{0}'.format(self.value)


class ServicePort(object):
  def __init__(self, name: str, protocol: str, port: int, target: int):
    self.name = name
    self.protocol = protocol
    self.port = port
    self.target = target


class Service(object):
  def __init__(self, name: str, deployment: Deployment, release: str, environment: str, namespace="default"):
    self.name = name
    self.deployment = deployment
    self.release = release
    self.environment = environment
    self.namespace = namespace
    self.labels = {}
    self.selector = {}
    self.service_type = ServiceType.CLUSTERIP
    self.port = None
    self.target_port = None
    self.__read_defaults__()

  def __read_defaults__(self):
    self.labels["app.kubernetes.io/name"] = self.name
    self.labels["app.kubernetes.io/deployment"] = self.deployment.name
    self.labels["app.kubernetes.io/release"] = self.release
    self.labels["app.kubernetes.io/environment"] = self.environment

    self.selector = self.deployment.match_labels

  def set_type(self, service_type:  ServiceType) -> Service:
    self.service_type = service_type
    return self

  def set_port(self, port: int) -> Service:
    self.port = port
    return self

  def set_target(self, port: int) -> Service:
    self.target_port = port
    return self

  def set_selectors(self, selectors: dict[str]) -> Service:
    self.selector = selectors
    return self

  def add_selector(self, selector_key: str, selector_value: str) -> Service:
    self.selector[selector_key] = selector_value
    return self

  # Service Labels

  def set_labels(self, labels: dict[str]) -> Service:
    self.labels = labels
    return self

  def add_label(self, key: str, value: str) -> Service:
    self.labels[key] = value
    return self

  def render(self, chart: Chart) -> k8s.Service:
    svc_port = k8s.ServicePort(port=self.port, target_port=k8s.IntOrString.from_number(self.target_port))
    svc_spec = k8s.ServiceSpec(type=self.service_type.k8s_name(), ports=[svc_port], selector=self.selector)
    return k8s.Service(chart, 'service', spec=svc_spec)
