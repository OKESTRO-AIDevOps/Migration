import kfp
from kfp import dsl
from kfp import components
from kfp.components import func_to_container_op
from elasticsearch import Elasticsearch
import kubernetes.client
client = kfp.Client(host='ip_address')

def croffle_consolidation() -> None:
    import sys

    sys.path.append('path/your/file')
    sys.path.append('path/your/file')

    import os 

    print(os.listdir())
    from utils.result import Reporting
    reporting = Reporting(job='croffle-consolidation')
    try:
        import os
        os.system('echo -e "\nip_address path.your.api" >> /etc/hosts')

        from jobs.consolidation import Consolidation
        from utils.metaData import metaData
        from utils.metaParsing import MetaParsing
        config_path = 'path/your/config.ini'

    # #### <<< croffle consolidation >>> ####
        metaData = metaData()
    except:
        reporting.report_result(result='fail', error='connect')
        exit(1)

    try:
        providers = metaData.retrieve_meta_providers()
        openstack_providers = list()

        for provider in providers:
            if provider['type'] == 'openstack':
                openstack_providers.append(provider['id'])
    except:
        reporting.report_result(result='fail', error='read')
        exit(1)