from kfp.components import InputPath

def upload_model(
    hydrosphere_uri: str, 
    model_path: InputPath(),
    model_name: str = "kf_regression", 
) -> int:
    from hydrosdk import Cluster
    from hydrosdk.modelversion import LocalModel, ModelContract
    from hydrosdk.contract import SignatureBuilder
    from hydrosdk.image import DockerImage
    import tempfile, os, shutil

    signature = SignatureBuilder('infer') \
        .with_input('x1', 'double', "scalar") \
        .with_input('x2', 'double', "scalar") \
        .with_output('y', 'int64', "scalar") \
        .build()
    contract = ModelContract(predict=signature)

    cluster = Cluster(hydrosphere_uri)

    model_file = "model.joblib"
    requirements = "requirements.txt"
    
    with tempfile.TemporaryDirectory() as model_dir:
        shutil.copy(os.path.join(model_path, model_file), model_dir)
        shutil.copy("/app/kf_hs/steps/upload_model/requirements.txt", model_dir)
        src_dir = os.path.join(model_dir, "src")
        os.makedirs(src_dir)
        shutil.copy("/app/kf_hs/steps/upload_model/func_main.py", src_dir)

        print("Creating a Model object")
        model = LocalModel(
            name = model_name,
            runtime = DockerImage("hydrosphere/serving-runtime-python-3.7", "2.4.0", None),
            path = model_dir,
            payload = [model_file, "src/", requirements],
            contract = contract,
            metadata = {"author": "a cool dude"},
            install_command = "pip install -r requirements.txt",
            training_data = None,
            monitoring_configuration = None
        )
        result = model.upload(cluster)
        result.lock_till_released()
        print(result)
        return result.version