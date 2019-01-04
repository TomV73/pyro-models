# model file: ../example-models/Bayesian_Cognitive_Modeling/ParameterEstimation/Binomial/Rate_5.stan
import torch
import pyro


def validate_data_def(data):
    assert 'n1' in data, 'variable not found in data: key=n1'
    assert 'n2' in data, 'variable not found in data: key=n2'
    assert 'k1' in data, 'variable not found in data: key=k1'
    assert 'k2' in data, 'variable not found in data: key=k2'
    # initialize data
    n1 = data["n1"]
    n2 = data["n2"]
    k1 = data["k1"]
    k2 = data["k2"]

def init_params(data, params):
    # initialize data
    n1 = data["n1"]
    n2 = data["n2"]
    k1 = data["k1"]
    k2 = data["k2"]
    # assign init values for parameters
    params["theta"] = init_real("theta", low=0, high=1) # real/double

def model(data, params):
    # initialize data
    n1 = data["n1"]
    n2 = data["n2"]
    k1 = data["k1"]
    k2 = data["k2"]
    # INIT parameters
    theta = params["theta"]
    # initialize transformed parameters
    # model block

    theta =  _pyro_sample(theta, "theta", "beta", [1, 1])
    k1 =  _pyro_sample(k1, "k1", "binomial", [n1, theta], obs=k1)
    k2 =  _pyro_sample(k2, "k2", "binomial", [n2, theta], obs=k2)

