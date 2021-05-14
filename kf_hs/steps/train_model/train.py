from kfp.components import OutputPath, create_component_from_func

def train(
    output_path: OutputPath(),
    n_samples: int = 300,
):
    import joblib
    import os
    from sklearn.datasets import make_blobs
    from sklearn.linear_model import LogisticRegression
    os.makedirs(output_path)
    # initialize data
    X, y = make_blobs(n_samples=n_samples, n_features=2, centers=[[-5, 1],[5, -1]])
    # create a model
    model = LogisticRegression()
    model.fit(X, y)

    model_filename = "model.joblib"
    full_path = os.path.join(output_path, model_filename)
    joblib.dump(model, full_path)