# model file: ../example-models/ARM/Ch.21/radon_vary_intercept_nofloor_chr.stan
import torch
import pyro
import pyro.distributions as dist

def init_vector(name, dims=None):
    return pyro.sample(name, dist.Normal(torch.zeros(dims), 0.2 * torch.ones(dims)))



def validate_data_def(data):
    assert 'J' in data, 'variable not found in data: key=J'
    assert 'N' in data, 'variable not found in data: key=N'
    assert 'county' in data, 'variable not found in data: key=county'
    assert 'u' in data, 'variable not found in data: key=u'
    assert 'y' in data, 'variable not found in data: key=y'
    # initialize data
    J = data["J"]
    N = data["N"]
    county = data["county"]
    u = data["u"]
    y = data["y"]

def init_params(data):
    params = {}
    # initialize data
    J = data["J"]
    N = data["N"]
    county = data["county"]
    u = data["u"]
    y = data["y"]
    # assign init values for parameters
    params["sigma_a"] = pyro.sample("sigma_a", dist.Uniform(0., 100.))
    params["sigma_y"] = pyro.sample("sigma_y", dist.Uniform(0., 100.))

    return params

def model(data, params):
    # initialize data
    J = data["J"]
    N = data["N"]
    county = data["county"].long() - 1
    u = data["u"]
    y = data["y"]

    # init parameters
    sigma_a = params["sigma_a"]
    sigma_y = params["sigma_y"]
    # initialize transformed parameters

    mu_a =  pyro.sample("mu_a", dist.Normal(0., 1))
    eta =  pyro.sample("eta", dist.Normal(0., 1).expand([J]))
    b =  pyro.sample("b", dist.Normal(0., 1))
    a = mu_a + sigma_a * eta
    y_hat = a[county] + u * b * 0.1
    y =  pyro.sample("y", dist.Normal(y_hat, sigma_y), obs=y)
