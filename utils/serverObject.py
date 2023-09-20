class Provider:
    def __init__(self, provider_id, provider_name):
        self.provider_id = provider_id
        self.provider_name = provider_name
        self.regions = []

    def add_region(self, region):
        self.regions.append(region)


class Region:
    def __init__(self, region_name):
        self.region_name = region_name
        self.hosts = []

    def add_host(self, host):
        self.hosts.append(host)


class Zone:
    def __init__(self, zone_name):
        self.zone_name = zone_name
        self.hosts = []

    def add_host(self, host):
        self.hosts.append(host)


class Host:
    def __init__(self, host_id, host_name, status, total_cpu, total_memory, total_disk):
        self.host_id = host_id
        self.host_name = host_name
        self.status = status
        self.total_cpu = total_cpu
        self.total_memory = total_memory
        self.total_disk = total_disk
        self.used_cpu = 0
        self.used_memory = 0
        self.used_disk = 0
        self.remain_cpu = 0
        self.remain_memory = 0
        self.remain_disk = 0
        self.vms = []

    def add_vm(self, vm):
        self.vms.append(vm)


class Vm:
    def __init__(self, vm_id, vm_name, cpu, memory, disk):
        self.vm_id = vm_id
        self.vm_name = vm_name
        self.cpu = cpu
        self.memory = memory
        self.disk = disk