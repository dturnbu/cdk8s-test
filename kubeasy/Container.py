from __future__ import annotations
from imports import k8s
from kubeasy import Security
from kubeasy.Resources import ResourceRequirements


class ContainerPort(object):
  def __init__(self, name: str = None, protocol: str = None, port: int = None):
    self.name = name
    self.protocol = protocol
    self.port = port
    self.__read_defaults__()

  def __read_defaults__(self):
    pass

  def render(self):
    return k8s.ContainerPort(name=self.name, protocol=self.protocol, container_port=self.port)


class Container(object):
  def __init__(self, name: str, image: str, tag: str):
    self.name = name
    self.image = image
    self.tag = tag
    self.ports = []
    self.security_context = Security.SecurityContext().render()
    self.resource_requirements = ResourceRequirements().render()
    self.__read_defaults__()

  def __read_defaults__(self):
    pass

  def set_resource_requirements(self, resource_requirements: ResourceRequirements) -> Container:
    self.resource_requirements = resource_requirements.render()
    return self

  def set_security_context(self, security_context: Security.SecurityContext) -> Container:
    self.security_context = security_context.render()
    return self

  def add_port(self, port: int) -> Container:
    self.ports.append(ContainerPort(port=port).render())
    return self

  def set_ports(self, ports: list[int]) -> Container:
    for port in ports:
      self.add_port(port)
    return self

  def render(self) -> k8s.Container:
    return k8s.Container(name=self.name,
                         image=f"{self.image}:{self.tag}",
                         ports=self.ports,
                         security_context=self.security_context,
                         resources=self.resource_requirements)


class Containers(list):
  def add_container(self, name: str, image: str, tag: str, ports: list[int]):
    self.append(Container(name, image, tag).set_ports(ports))

  def get_container(self, index) -> Container:
    return self[index]

  def render(self) -> list[k8s.Container]:
    containers = []
    for container_index in range(0, len(self)):
      containers.append(self.get_container(container_index).render())
    return containers
