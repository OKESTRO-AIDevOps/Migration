
# 221205_v1 consolidation
import kfp
from kfp import dsl
from kfp import components
from kfp.components import func_to_container_op
from elasticsearch import Elasticsearch
import kubernetes.client
# client = kfp.Client(host='ip_address')
client = kfp.Client(host='ip_address')

def croffle_consolidation() -> None:
    import sys
    # sys.path.append('/symphony/croffle/')
    sys.path.append('/croffle/')
    from utils.result import Reporting
    reporting = Reporting(job='croffle-consolidation')

    try:
        import os
        # os.system('echo -e "\nip_address path.your.api" >> /etc/hosts ')
        os.system('echo -e "\nip_address path.your.api" >> /etc/hosts ') 
        print(sys.path)
        from jobs.consolidation import Consolidation
        from utils.metaData import metaData
        from utils.metaParsing import MetaParsing
        config_path = '/path/youre/config.ini'

    # #### <<< croffle consolidation >>> ####
        metaData = metaData()
    except:
        reporting.report_result(result='fail', error='connect')
        exit(1)

    try:
        providers = metaData.retrieve_meta_providers()
        print('providers: ', providers)
        openstack_providers = list()

        for provider in providers:
            if provider['type'] == 'openstack':
                openstack_providers.append(provider['id'])
        print('openstack_provider: ', openstack_providers)

    except Exception as e:
        reporting.report_result(result='fail', error='read')
        print(e)
        exit(1)

    try:
        for id in openstack_providers:
            print("start consolidation Algorithm provider: ", id)
            metaParsing = MetaParsing(id, 'openstack')
            if type(metaParsing.metas) is not None:
                provider = metaParsing.hierarchy_vms()
                print(provider)
                consolidation = Consolidation(provider)
                placement, migration_placement, total_cost = consolidation.consolidation(limit=100, division='region')
                try:
                    consolidation.conslidation_to_es(placement, migration_placement, total_cost)
                except Exception as e:
                    reporting.report_result(result='fail', error='write')
                    print(e)
                    exit()
    except Exception as e:
        reporting.report_result(result='fail', error='consolidation Algorithm fail')
        print(e)
        exit()