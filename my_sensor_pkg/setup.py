from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'my_sensor_pkg'

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

        (
            os.path.join('share', package_name, 'urdf'),
            glob('urdf/*')
        ),

        (
            os.path.join('share', package_name, 'config'),
            glob('config/*')
        ),
    ],

    package_data={'': ['py.typed']},

    install_requires=['setuptools'],
    zip_safe=True,

    maintainer='parkbyeongjun',
    maintainer_email='whitepengg@gmail.com',

    description='Week 06 sensor simulation package',
    license='TODO: License declaration',

    extras_require={
        'test': [
            'pytest',
        ],
    },

    entry_points={
        'console_scripts': [
            'sensor_listener = my_sensor_pkg.sensor_listener:main',
            'emergency_stop = my_sensor_pkg.emergency_stop_node:main',
        ],
    },
)