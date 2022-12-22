import os
import sys

from utils.consolidation.serverObject import Provider
from utils.consolidation.serverObject import Region
from utils.consolidation.serverObject import Zone
from utils.consolidation.serverObject import Host
from utils.consolidation.serverObject import Vm

from utils.logs.log import standardLog
from utils.metaData import metaData

standardLog = standardLog()

metaData = metaData()


class MetaParsing:
    def __init__(self, provider_id, provider_type, cpu_overcommit=7, memory_overcommit=3, disk_overcommit=1):
        self.provider_id = provider_id
        self.provider_type = provider_type
        self.cpu_overcommit = cpu_overcommit
        self.memory_overcommit = memory_overcommit
        self.disk_overcommit = disk_overcommit
        self.metas_v1 = metaData.retrieve_meta_openstack_info(provider_id=provider_id, info='metas')

        self.hypervisor_v2 = metaData.retrieve_meta_openstack_info_v2(provider_id=provider_id, info='hypervisors')
        self.metas_v2 = metaData.retrieve_meta_openstack_info_v2(provider_id=provider_id, info='vms')

    def hierarchy_vms(self):
        try:
            provider = Provider(self.provider_id, self.provider_type)
            if 'region' not in self.metas_v1.keys():
                region = Region('korea')

            for zone_value in self.metas_v1['zones']:
                zone = Zone(zone_value['name'])

                for host_value in self.metas_v1['hosts']:
                    total_cpu = host_value['totalVCpu'] * self.cpu_overcommit
                    total_memory = host_value['totalMemory'] * self.memory_overcommit
                    host_value['totalDisk'] = host_value['totalDisk'] * self.disk_overcommit

                    host = Host(host_value['id'], host_value['hypervisorHostname'],
                                host_value['status'], total_cpu, total_memory,
                                host_value['totalDisk'])

                    for vm_value in self.metas_v1['vms']:
                        if zone.zone_name != vm_value['availabilityZone']:
                            continue
                        if host.host_name != vm_value['hypervisorHostName']:
                            continue

                        vm = Vm(vm_value['id'], vm_value['name'],
                                vm_value['vCpus'], vm_value['localMemory'], vm_value['localDisk'])

                        host.used_cpu += vm_value['vCpus']
                        host.used_memory += vm_value['localMemory']
                        host.used_disk += vm_value['localDisk']
                        host.vms.append(vm)

                    if len(host.vms) != 0:
                        host.remain_cpu = round(host.total_cpu - host.used_cpu, 2)
                        host.remain_memory = round(host.total_memory - host.used_memory, 2)
                        host.remain_disk = round(host.total_disk - host.used_disk, 2)

                        zone.hosts.append(host)
                        region.hosts.append(host)

                provider.zones.append(zone)
            provider.regions.append(region)

        except Exception as e:
            standardLog.sending_log('error', e).error('metaData parsing error')
            print(e)
            exit()
        standardLog.sending_log('success').info('metaData parsing success')

        return provider

    def hierarchy_vms_v2(self):
        try:
            provider = Provider(self.provider_id, self.provider_type)
            self.hypervisor_v2 = self.hypervisor_v2
            zone_names = list()
            region_names = list()

            for hypervisor in self.hypervisor_v2:
                if hypervisor['availabilityZone'] not in zone_names:
                    zone_names.append(hypervisor['availabilityZone'])
                if 'region' in hypervisor.keys():
                    if hypervisor['region'] not in region_names:
                        region_names.append(hypervisor['region'])
            if len(region_names) == 0:
                region = Region('korea')

            for zone_value in zone_names:
                zone = Zone(zone_value)

                for host_value in self.hypervisor_v2:
                    total_cpu = host_value['virtualCpu'] * self.cpu_overcommit
                    total_memory = host_value['memory'] * self.memory_overcommit
                    total_disk = host_value['disk'] * self.disk_overcommit

                    host = Host(host_value['hypervisorId'], host_value['hypervisorHostName'],
                                host_value['hypervisorStatus'], total_cpu, total_memory,
                                total_disk)

                    for vm_value in self.metas_v2:
                        if zone.zone_name != vm_value['availabilityZone']:
                            continue
                        if host.host_name != vm_value['vmHostName']:
                            continue

                        vm = Vm(vm_value['tenantId'], vm_value['vmName'],
                                vm_value['cpu'], vm_value['memory'], vm_value['disk'])

                        host.used_cpu += vm_value['cpu']
                        host.used_memory += vm_value['memory']
                        host.used_disk += vm_value['disk']
                        host.vms.append(vm)

                    if len(host.vms) != 0:
                        host.remain_cpu = round(host.total_cpu - host.used_cpu, 2)
                        host.remain_memory = round(host.total_memory - host.used_memory, 2)
                        host.remain_disk = round(host.total_disk - host.used_disk, 2)

                        zone.hosts.append(host)
                        region.hosts.append(host)

                provider.zones.append(zone)
            provider.regions.append(region)
        except Exception as e:
            print(e)
            standardLog.sending_log('error', e).error('metaData parsing error')
            exit()
        standardLog.sending_log('success').info('metaData parsing success')

        return provider