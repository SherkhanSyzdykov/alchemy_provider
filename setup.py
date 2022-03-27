import setuptools

with open('./README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='alchemy_provider',
    version='0.0.2',
    author='Sherkhan Syzdykov',
    author_email='syzdykovsherkhan@gmail.com',
    description='Dynamic query builder based on SQLAlchemy Core and ORM',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SherkhanSyzdykov/alchemy_provider',
    project_urls={
        'Bug Tracker': 'https://github.com/SherkhanSyzdykov/alchemy_provider/issues',
        'Discussions': 'https://github.com/SherkhanSyzdykov/alchemy_provider/discussions',
    },
    classifiers=[
        'Typing :: Typed',
        'Topic :: Internet',
        'Topic :: Communications',
        'Framework :: AsyncIO',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(where='.'),
    install_requires=[
        'orjson',
        'SQLAlchemy',
        'SQLAlchemy-Utils'
    ],
    python_requires='>=3.6',
)
