import json
import pytest
from selenium import webdriver


@pytest.fixture
def config(scope='session'):
    # Read the file
    with open('C:\\Users\\dipak\\PycharmProjects\\zacks\\config.json') as config_file:
        config = json.load(config_file)

    # Assert values
    assert config['browser'] in ['FireFox', 'Chrome', 'Headless Chrome', 'IE']
    assert isinstance(config['implicit_wait'], int)
    assert config['implicit_wait'] > 0

    # RETURN THE CONFIG VALUE
    return config


@pytest.fixture
def browser(config):
    # Initialize the chrome browser instance
    # driverExecutable = utilityClass.readConfig('common', 'driverExecutable')

    if config['browser'] == 'Chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        b = webdriver.Chrome(chrome_options=options, executable_path=config['driverExecutable'])
    elif config['browser'] == 'Headless Chrome':
        # s = ChromeDriverManager.Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        b = webdriver.Chrome(chrome_options=options, executable_path=config['driverExecutable'])
    elif config['browser'] == 'IE':
        # options = webdriver.IeOptions()
        # options.add_argument('headless')
        b = webdriver.Ie(executable_path=config['driverExecutable'])
    else:
        raise Exception(f'Browser "{config["browser"]}" is not supported')

    # implicitly wait for 10 seconds
    b.implicitly_wait(config['implicit_wait'])

    # return chromedriver instance for set up
    yield b

    # quit the webdriver instance for the clean
    b.quit()
