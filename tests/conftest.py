from tempfile import TemporaryDirectory
import os

import pytest

from blag import blag


@pytest.fixture
def environment():
    site = {
        'base_url': 'site base_url',
        'title': 'site title',
        'description': 'site description',
        'author': 'site author',
    }
    env = blag.environment_factory(globals_=dict(site=site))
    yield env


@pytest.fixture
def page_template(environment):
    yield environment.get_template('page.html')


@pytest.fixture
def article_template(environment):
    yield environment.get_template('article.html')


@pytest.fixture
def archive_template(environment):
    yield environment.get_template('archive.html')


@pytest.fixture
def tags_template(environment):
    yield environment.get_template('tags.html')


@pytest.fixture
def tag_template(environment):
    yield environment.get_template('tag.html')


@pytest.fixture
def cleandir():
    """Create a temporary workind directory and cwd.

    """
    config = """
[main]
base_url = https://example.com/
title = title
description = description
author = a. u. thor
    """

    with TemporaryDirectory() as dir:
        for d in 'content', 'build', 'static', 'templates':
            os.mkdir(f'{dir}/{d}')
        with open(f'{dir}/config.ini', 'w') as fh:
            fh.write(config)
        # change directory
        old_cwd = os.getcwd()
        os.chdir(dir)
        yield dir
        # and change back afterwards
        os.chdir(old_cwd)


@pytest.fixture
def args(cleandir):

    class NameSpace:
        def __init__(self, **kwargs):
            for name in kwargs:
                setattr(self, name, kwargs[name])

    args = NameSpace(
            input_dir='content',
            output_dir='build',
            static_dir='static',
            template_dir='templates',
    )
    yield args
