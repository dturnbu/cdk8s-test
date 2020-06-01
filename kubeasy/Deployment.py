from __future__ import annotations
from imports import k8s
from cdk8s import Chart
from kubeasy.Container import Container, Containers
from kubeasy import Service


class Deployment(object):
  def render(self, chart: Chart) -> Deployment:
    object_meta = k8s.ObjectMeta(labels=self.labels)
    label_selector = k8s.LabelSelector(match_labels=self.match_labels)
    self.containers.add_container(self.name, self.image, self.tag, self.ports)

    podspec = k8s.PodSpec(containers=Containers(self.containers).render())
    podspec_template = k8s.PodTemplateSpec(metadata=object_meta, spec=podspec)

    deployment_spec = k8s.DeploymentSpec(replicas=self.replicas, selector=label_selector, template=podspec_template)
    k8s.Deployment(chart, 'deployment', spec=deployment_spec)
    return self

  def __init__(self, name: str, image: str, tag: str, environment: str):
    self.name = name
    self.image = image
    self.tag = tag
    self.environment = environment
    self.ports = [80]
    self.replicas = 1
    self.image_pull_policy = "Always"
    self.image_pull_secret = None

    self.labels = {}
    self.match_labels = {}

    self.services = []
    self.init_containers = Containers()
    self.containers = Containers()
    self.env_variables = {}
    self.volume_mounts = {}

    # Default deployment probes
    self.liveness_probe_path = "/"
    self.liveness_probe_port = 80
    self.readiness_probe_path = "/"
    self.readiness_probe_port = 80

    self.__read_defaults__()

  def __read_defaults__(self):
    self.labels["app.kubernetes.io/name"] = self.name
    self.labels["app.kubernetes.io/release"] = self.tag
    self.labels["app.kubernetes.io/environment"] = self.environment

    self.match_labels["app.kubernetes.io/deployment"] = self.name
    self.match_labels["app.kubernetes.io/release"] = self.tag
    self.match_labels["app.kubernetes.io/environment"] = self.environment

  def set_replicas(self, replica_count: int) -> Deployment:
    self.replicas = replica_count
    return self

  # Deployment Labels

  def set_labels(self, labels: dict[str]) -> Deployment:
    self.labels = labels
    return self

  def add_label(self, key: str, value: str) -> Deployment:
    self.labels[key] = value
    return self

  # Deployment Match Labels

  def set_match_labels(self, match_labels: dict[str]) -> Deployment:
    self.match_labels = match_labels
    return self

  def add_match_label(self, key: str, value: str) -> Deployment:
    self.match_labels[key] = value
    return self

  # Deployment Services

  def set_services(self, services: list[Service]) -> Deployment:
    self.services = services
    return self

  def add_service(self, service: Service) -> Deployment:
    self.services.append(service)

  # Security Settings

  def set_image_pull_policy(self, pull_policy: str) -> Deployment:
    self.image_pull_policy = pull_policy
    return self

  def set_image_pull_secret(self, pull_secret: str) -> Deployment:
    self.image_pull_secret = pull_secret
    return self

  def set_cpu_requests(self, cpu_requests: str) -> Deployment:
    self.cpu_requests = cpu_requests
    return self

  def set_cpu_limits(self, cpu_limits: str) -> Deployment:
    self.cpu_limits = cpu_limits
    return self

  def set_memory_requests(self, memory_requests: str) -> Deployment:
    self.memory_requests = memory_requests
    return self

  def set_memory_limits(self, memory_limits: str) -> Deployment:
    self.memory_limits = memory_limits
    return self

  def set_read_only_root_fs(self, ro_root_fs: bool) -> Deployment:
    self.ro_root_fs = ro_root_fs
    return self

  def set_run_as_non_root(self, run_as_non_root: bool) -> Deployment:
    self.run_as_non_root = run_as_non_root
    return self

  def set_drop_all_capabilities(self, drop_all_capabilities) -> Deployment:
    self.drop_all_capabilities = drop_all_capabilities
    return self

  def set_run_as_uid(self, run_as_uid: int) -> Deployment:
    self.run_as_uid = run_as_uid
    return self

  def set_run_as_gid(self, run_as_gid: int) -> Deployment:
    self.run_as_gid = run_as_gid
    return self

  def set_pod_fs_gid(self, pod_fs_gid: int) -> Deployment:
    self.pod_fs_gid = pod_fs_gid
    return self

  def set_liveness_probe(self, path: str, port: int) -> Deployment:
    self.liveness_probe_path = path
    self.liveness_probe_port = port
    return self

  def set_readiness_probe(self, path: str, port: int) -> Deployment:
    self.readiness_probe_path = path
    self.readiness_probe_port = port
    return self

  # Containers
  def set_containers(self, containers: list[Container]) -> Deployment:
    self.containers = containers
    return self

  def add_container(self, container: Container) -> Deployment:
    self.containers.append(container)
    return self

  # Init Containers

  def set_init_containers(self, containers: list[Container]) -> Deployment:
    self.init_containers = containers
    return self

  def add_init_container(self, container: Container) -> Deployment:
    self.init_containers.append(container)
    return self

  # Environment Variables

  def set_env_variables(self, variables: dict[str]) -> Deployment:
    self.env_variables = variables
    return self

  def add_env_variable(self, key: str, value: str) -> Deployment:
    self.env_variables[key] = value
    return self

  # Volume Mounts

  def set_volume_mounts(self, mounts: dict[str]) -> Deployment:
    self.volume_mounts = mounts
    return self

  def add_volume_mount(self, key: str, value: str) -> Deployment:
    self.volume_mounts[key] = value
    return self
