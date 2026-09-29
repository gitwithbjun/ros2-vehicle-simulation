import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'my_tf_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='parkbyeongjun',
    maintainer_email='whitepengg@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
        entry_points={
            'console_scripts': [
                'static_tf = my_tf_pkg.static_tf_broadcaster:main',
                'dynamic_tf = my_tf_pkg.dynamic_tf_broadcaster:main',
                'tf_listener = my_tf_pkg.tf_listener:main',
            ],
        },
)
