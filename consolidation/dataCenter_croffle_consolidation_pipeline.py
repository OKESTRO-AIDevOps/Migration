import kfp
from kfp import dsl
from kfp.components import func_to_container_op
import kubernetes.client

client = kfp.Client(host='ip_address')


@func_to_container_op
def croffle_consolidation() -> None:
    import sys
    import os
    from utils.result import Reporting
    from jobs.consolidation import Consolidation
    from utils.metaData import metaData
    from utils.metaParsing import MetaParsing

    sys.path.append('path/your/file')
    sys.path.append('path/your/file')

    print(os.listdir())

    reporting = Reporting(job='croffle-consolidation')

    try:
        os.system('echo -e "\nip_address path.your.api" >> /etc/hosts')

        metaData_instance = metaData()
    except Exception as e:
        reporting.report_result(result='fail', error=f'connect: {str(e)}')
        exit(1)

    try:
        providers = metaData_instance.retrieve_meta_providers()
        openstack_providers = [provider['id'] for provider in providers if provider['type'] == 'openstack']
    except Exception as e:
        reporting.report_result(result='fail', error=f'read: {str(e)}')
        exit(1)

    try:
        for provider_id in openstack_providers:
            metaParsing = MetaParsing(provider_id, 'openstack')
            if metaParsing.metas is not None:
                provider = metaParsing.hierarchy_vms()

                consolidation = Consolidation(provider)
                placement, migration_placement, total_cost = consolidation.consolidation(limit=100, division='region')

                try:
                    consolidation.conslidation_to_es(placement, migration_placement, total_cost)
                except Exception as e:
                    reporting.report_result(result='fail', error=f'write: {str(e)}')
                    exit(1)
            print('finish')
        print('real finish')
    except Exception as e:
        reporting.report_result(result='fail', error=f'consolidation Algorithm fail: {str(e)}')
        exit(1)

    reporting.report_result(result='success')


croffle_consolidation_op = croffle_consolidation()


@dsl.pipeline(
    name="croffle-consolidation",
)
def croffle_consolidation_pipeline():
    vop = dsl.PipelineVolume(pvc='croffle-pvc')
    dsl.get_pipeline_conf().set_image_pull_secrets([kubernetes.client.V1LocalObjectReference(name="public_aiops")])

    croffle_consolidation_op("/aiplatform/").add_pvolumes({"/aiplatform/": vop})

    dsl.get_pipeline_conf().set_ttl_seconds_after_finished(20)


client.create_run_from_pipeline_func(croffle_consolidation_pipeline, arguments={})

kfp.compiler.Compiler().compile(
    pipeline_func=croffle_consolidation_pipeline,
    package_path='path/your/croffle_consolidation_pipeline.yaml'
)

client.create_recurring_run(
    experiment_id=client.get_experiment(experiment_name="Default").id,
    job_name="croffle_consolidation",
    description="version: croffle:consolidation_v1",
    cron_expression="0 10 16 * *",
    pipeline_package_path="path/your/croffle_consolidation_pipeline.yaml"
)