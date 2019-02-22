# model file: example-models/ARM/Ch.3/kidscore_momiq.stan
import torch
import pyro
import pyro.distributions as dist

def init_vector(name, dims=None):
    return pyro.sample(name, dist.Normal(torch.zeros(dims), 0.2 * torch.ones(dims)).to_event(1))



def validate_data_def(data):
    assert 'N' in data, 'variable not found in data: key=N'
    assert 'kid_score' in data, 'variable not found in data: key=kid_score'
    assert 'mom_iq' in data, 'variable not found in data: key=mom_iq'
    # initialize data
    N = data["N"]
    kid_score = data["kid_score"]
    mom_iq = data["mom_iq"]

def init_params(data):
    params = {}
    params["beta"] = init_vector("beta", dims=(3)) # vector
    return params

def model(data, params):
    # initialize data
    N = data["N"]
    kid_score = data["kid_score"]
    mom_iq = data["mom_iq"]

    # init parameters
    beta = params["beta"]

    with pyro.plate("data", N):
        sigma =  pyro.sample("sigma", dist.HalfCauchy(torch.tensor(2.5)))
        kid_score = pyro.sample('obs', dist.Normal(beta[0] + beta[1] * mom_iq, sigma), obs=kid_score)
