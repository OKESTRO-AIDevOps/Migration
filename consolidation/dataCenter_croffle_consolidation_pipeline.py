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

    try:
        for id in openstack_providers:
            metaParsing = MetaParsing(id, 'openstack')
            if metaParsing.metas is not None:
                provider = metaParsing.hierarchy_vms()

                consolidation = Consolidation(provider)
                placement, migration_placement, total_cost = consolidation.consolidation(limit=100, division='region')

                try:
                    consolidation.conslidation_to_es(placement, migration_placement, total_cost)
                except:
                    reporting.report_result(result='fail', error='write')
                    exit(1)
            print('finish')
        print('real finish')
    except:
        reporting.report_result(result='fail', error='consolidation Algorithm fail')
        exit()
    reporting.report_result(result='success')

croffle_consolidation_component = components.create_component_from_func(
        func=croffle_consolidation,                       
        base_image='path/your/image',
        packages_to_install=['requests']    
    )

@dsl.pipeline(
    name="croffle-consolidation",
)
def croffle_consolidation_pipeline():
    vop = dsl.PipelineVolume(pvc='croffle-pvc')
    dsl.get_pipeline_conf().set_image_pull_secrets([kubernetes.client.V1LocalObjectReference(name="public_aiops")])
    croffle_consolidation_component().add_pvolumes({"/aiplatform/": vop})
    dsl.get_pipeline_conf().set_ttl_seconds_after_finished(20)

client.create_run_from_pipeline_func(croffle_consolidation_pipeline, arguments={})

kfp.compiler.Compiler().compile(
    pipeline_func=croffle_consolidation_pipeline,
    package_path='path/your/croffle_consolidation_pipeline.yaml'
)

client.create_recurring_run(
    experiment_id = client.get_experiment(experiment_name="Default").id,
    job_name="croffle_consolidation",
    description="version: croffle:consolidation_v1",
    cron_expression="0 10 16 * *",
    pipeline_package_path = "path/your/croffle_consolidation_pipeline.yaml"
)
