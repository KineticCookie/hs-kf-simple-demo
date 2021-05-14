def update_application(
    model_name: str,
    model_version: int,
    hydrosphere_uri: str,
    application_name: str = "kf_lr_app"
):
    import time
    from hydrosdk import Cluster
    from hydrosdk.modelversion import ModelVersion
    from hydrosdk.application import Application, ApplicationBuilder, ExecutionStageBuilder

    cluster = Cluster(hydrosphere_uri)
    mv = ModelVersion.find(cluster, model_name, model_version)

    try:
        Application.delete(cluster, application_name)
        time.sleep(5)
    except Exception as e:
        print(f"Got error while trying to delete an application {application_name}")
        print(e)

    print("Creating an Application object")
    app_builder = ApplicationBuilder(cluster, application_name)
    stage = ExecutionStageBuilder().with_model_variant(mv, 100).build()
    app_builder = app_builder.with_stage(stage)
    print(f"Uploading model to the cluster {hydrosphere_uri}")
    app = app_builder.build()
    app = app.lock_while_starting()
    print(app)
    return app