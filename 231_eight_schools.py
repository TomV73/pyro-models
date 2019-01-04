# model file: ../example-models/misc/eight_schools/eight_schools.stan
import torch
import pyro


def validate_data_def(data):
    assert 'J' in data, 'variable not found in data: key=J'
    assert 'y' in data, 'variable not found in data: key=y'
    assert 'sigma' in data, 'variable not found in data: key=sigma'
    # initialize data
    J = data["J"]
    y = data["y"]
    sigma = data["sigma"]

def init_params(data, params):
    # initialize data
    J = data["J"]
    y = data["y"]
    sigma = data["sigma"]
    # assign init values for parameters
    params["mu"] = init_real("mu") # real/double
    params["theta"] = init_real("theta", dims=(J)) # real/double
    params["tau"] = init_real("tau", low=0) # real/double

def model(data, params):
    # initialize data
    J = data["J"]
    y = data["y"]
    sigma = data["sigma"]
    # INIT parameters
    mu = params["mu"]
    theta = params["theta"]
    tau = params["tau"]
    # initialize transformed parameters
    # model block

    theta =  _pyro_sample(theta, "theta", "normal", [mu, tau])
    y =  _pyro_sample(y, "y", "normal", [theta, sigma], obs=y)

