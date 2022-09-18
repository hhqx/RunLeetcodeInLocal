

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PythonLeetcodeRunner',
    version='1.0.2',
    author='hhqx',
    author_email='weiwushaonian@foxmail.com',
    description='This is a package help you to run leetcode in local python IDE.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hhqx/PythonLeetcodeRunner',
    project_urls = {
        "Bug Tracker": "https://github.com/mike-huls/PythonLeetcodeRunner/issues"
    },
    license='MIT',
    packages=['PythonLeetcodeRunner'],
    install_requires=['rich', 'typing'],
)



"""

# 引用包管理工具setuptools，其中find_packages可以帮我们便捷的找到自己代码中编写的库
from setuptools import setup, find_packages

setup(
    name='example',  # 包名称，之后如果上传到了pypi，则需要通过该名称下载
    version='0.1',  # version只能是数字，还有其他字符则会报错
    keywords=('setup', 'example'),
    description='setup example',
    long_description='',
    license='MIT',  # 遵循的协议
    install_requires=[],  # 这里面填写项目用到的第三方依赖
    author='hhqx',
    author_email='weiwushaonian@foxmail.com',
    packages=find_packages(),  # 项目内所有自己编写的库
    platforms='any',
    url='',  # 项目链接,
    include_package_data = True,
    entry_points={
        'console_scripts': [
            'example=run:main'
        ]
    },
)

"""

