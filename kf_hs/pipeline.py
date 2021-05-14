from kfp import dsl, compiler, components
from kfp.components import create_component_from_func
from kf_hs.steps.train_model.train import train
from kf_hs.steps.update_application.update import update_application
from kf_hs.steps.upload_model.upload import upload_model


def load_component(component_path):
    """
    Loads component definition from .yaml file.
    :param component_path: Path to component definition
    """
    with open(component_path, "r") as inp:
        return components.load_component(text=inp.read())

train_op = load_component("./kf_hs/steps/train_model/component.yaml")
upload_model_op = load_component("./kf_hs/steps/upload_model/component.yaml")
update_app_op = load_component("./kf_hs/steps/update_application/component.yaml")

@dsl.pipeline("Hydrosphere Training Pipeline")
def pipeline(
    hydrosphere_uri = "",
    model_name = "hs_lr_model",
    application_name = "hs_lr_app"
):
    trained_model = train_op().output
    deployed_version = upload_model_op(
        hydrosphere_uri = hydrosphere_uri,
        model = trained_model,
        model_name = model_name
    ).output
    update_app_op(
        model_name = model_name,
        model_version = deployed_version,
        hydrosphere_uri = hydrosphere_uri,
        application_name = application_name
    )

def compile():
    create_component_from_func(
        upload_model,
        output_component_file='./kf_hs/steps/upload_model/component.yaml',
        base_image='kineticcookie/demo-kf',
    )
    create_component_from_func(
        update_application,
        output_component_file='./kf_hs/steps/update_application/component.yaml',
        base_image='kineticcookie/demo-kf',
    )
    create_component_from_func(
        train,
        output_component_file='./kf_hs/steps/train_model/component.yaml',
        base_image='kineticcookie/demo-kf',
    )
    compiler.Compiler().compile(pipeline, "./output/pipeline.tar.gz")
    print("Done! Compiled to ./output/pipeline.tar.gz")

def build_image():
    import subprocess
    subprocess.run(["docker", "build", "-t", "kineticcookie/demo-kf", "."])
    