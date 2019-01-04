# model file: ../example-models/ARM/Ch.23/electric_1c_chr.stan
import torch
import pyro


def validate_data_def(data):
    assert 'N' in data, 'variable not found in data: key=N'
    assert 'n_grade' in data, 'variable not found in data: key=n_grade'
    assert 'n_grade_pair' in data, 'variable not found in data: key=n_grade_pair'
    assert 'n_pair' in data, 'variable not found in data: key=n_pair'
    assert 'grade' in data, 'variable not found in data: key=grade'
    assert 'grade_pair' in data, 'variable not found in data: key=grade_pair'
    assert 'pair' in data, 'variable not found in data: key=pair'
    assert 'pre_test' in data, 'variable not found in data: key=pre_test'
    assert 'treatment' in data, 'variable not found in data: key=treatment'
    assert 'y' in data, 'variable not found in data: key=y'
    # initialize data
    N = data["N"]
    n_grade = data["n_grade"]
    n_grade_pair = data["n_grade_pair"]
    n_pair = data["n_pair"]
    grade = data["grade"]
    grade_pair = data["grade_pair"]
    pair = data["pair"]
    pre_test = data["pre_test"]
    treatment = data["treatment"]
    y = data["y"]

def init_params(data, params):
    # initialize data
    N = data["N"]
    n_grade = data["n_grade"]
    n_grade_pair = data["n_grade_pair"]
    n_pair = data["n_pair"]
    grade = data["grade"]
    grade_pair = data["grade_pair"]
    pair = data["pair"]
    pre_test = data["pre_test"]
    treatment = data["treatment"]
    y = data["y"]
    # assign init values for parameters
    params["eta_a"] = init_vector("eta_a", dims=(n_pair)) # vector
    params["mu_a"] = init_vector("mu_a", dims=(n_grade_pair)) # vector
    params["sigma_a"] = init_vector("sigma_a", low=0, high=100, dims=(n_grade_pair)) # vector
    params["sigma_y"] = init_vector("sigma_y", low=0, high=100, dims=(n_grade)) # vector
    params["b"] = init_vector("b", dims=(n_grade)) # vector
    params["c"] = init_vector("c", dims=(n_grade)) # vector

def model(data, params):
    # initialize data
    N = data["N"]
    n_grade = data["n_grade"]
    n_grade_pair = data["n_grade_pair"]
    n_pair = data["n_pair"]
    grade = data["grade"]
    grade_pair = data["grade_pair"]
    pair = data["pair"]
    pre_test = data["pre_test"]
    treatment = data["treatment"]
    y = data["y"]
    # INIT parameters
    eta_a = params["eta_a"]
    mu_a = params["mu_a"]
    sigma_a = params["sigma_a"]
    sigma_y = params["sigma_y"]
    b = params["b"]
    c = params["c"]
    # initialize transformed parameters
    a = init_vector("a", dims=(n_pair)) # vector
    sigma_y_hat = init_vector("sigma_y_hat", low=0, high=100, dims=(N)) # vector
    y_hat = init_vector("y_hat", dims=(N)) # vector
    for i in range(1, to_int(n_pair) + 1):
        a[i - 1] = _pyro_assign(a[i - 1], ((50 * _index_select(mu_a, grade_pair[i - 1] - 1) ) + (_index_select(sigma_a, grade_pair[i - 1] - 1)  * _index_select(eta_a, i - 1) )))
    for i in range(1, to_int(N) + 1):

        y_hat[i - 1] = _pyro_assign(y_hat[i - 1], ((_index_select(a, pair[i - 1] - 1)  + (_index_select(b, grade[i - 1] - 1)  * _index_select(treatment, i - 1) )) + (_index_select(c, grade[i - 1] - 1)  * _index_select(pre_test, i - 1) )))
        sigma_y_hat[i - 1] = _pyro_assign(sigma_y_hat[i - 1], _index_select(sigma_y, grade[i - 1] - 1) )
    # model block

    eta_a =  _pyro_sample(eta_a, "eta_a", "normal", [0, 1])
    mu_a =  _pyro_sample(mu_a, "mu_a", "normal", [0, 1])
    b =  _pyro_sample(b, "b", "normal", [0, 100])
    c =  _pyro_sample(c, "c", "normal", [0, 100])
    y =  _pyro_sample(y, "y", "normal", [y_hat, sigma_y_hat], obs=y)

