from setuptools import find_packages, setup

package_name = 'inspire_hand_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dobot',
    maintainer_email='dobot@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 'inspire_hand_bringup = inspire_hand_demo.inspire_hand_bringup:main'
            'talker = inspire_hand_demo.inspire_pub:main',
            'client = inspire_hand_demo.inspire_sub:main',
        ],
    },
)
