from setuptools import setup


setup(
    name='lexibank_clarkkimmun',
    py_modules=['lexibank_clarkkimmun'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'clarkkimmun=lexibank_clarkkimmun:Dataset',
        ],
        'cldfbench.commands':[
            'clarkkimmun=clarkkimmuncommands',
        ]
    },
    install_requires=[
        'pylexibank>=3.0',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
