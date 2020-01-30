from setuptools import setup


setup(
    name='cldfbench_clarkkimmun',
    py_modules=['cldfbench_clarkkimmun'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'clarkkimmun=cldfbench_clarkkimmun:Dataset',
        ],
        'cldfbench.commands':[
            'clarkkimmun=clarkkimmuncommands',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
