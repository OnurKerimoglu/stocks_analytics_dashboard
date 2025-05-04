import yaml

def load_configs(env):
    print(f'loading configs for {env}')
    config = {}
    # load dwh config
    dwh_fpath = "config/dwh.yaml"
    with open(dwh_fpath, 'r') as f:
        config_dwh = yaml.safe_load(f)
    config['DWH'] = config_dwh[env]
    return config