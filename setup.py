from setuptools import setup
import os
import sys
import copy
import shlex
import shutil
import fileinput

VERSION = '1.0.457.10snapshot6'
PATCH_DIR = 'build'
INSTALL_UPSTART = True
INSTALL_SYSTEMD = True

prefix = sys.prefix
for arg in copy.copy(sys.argv):
    if arg.startswith('--prefix'):
        prefix = os.path.normpath(shlex.split(arg)[0].split('=')[-1])
    elif arg == '--no-upstart':
        sys.argv.remove('--no-upstart')
        INSTALL_UPSTART = False
    elif arg == '--no-systemd':
        sys.argv.remove('--no-systemd')
        INSTALL_SYSTEMD = False

if not os.path.exists('build'):
    os.mkdir('build')

main_css_path = os.path.join('www/vendor/dist/css',
    os.listdir('www/vendor/dist/css')[0])
main_js_path = os.path.join('www/vendor/dist/js',
    sorted(os.listdir('www/vendor/dist/js'))[0])

data_files = [
    ('/etc', ['data/etc/pritunl.conf']),
    ('/var/log', [
        'data/var/pritunl.log',
        'data/var/pritunl.log.1',
    ]),
    ('/usr/share/pritunl/www', [
        'www/dbconf.html',
        'www/key_view.html',
        'www/login.html',
        'www/upgrade.html',
        'www/vendor/dist/favicon.ico',
        'www/vendor/dist/index.html',
        'www/vendor/dist/robots.txt',
    ]),
    ('/usr/share/pritunl/www/css', [main_css_path]),
    ('/usr/share/pritunl/www/fonts', [
        'www/vendor/dist/fonts/fredoka-one.eot',
        'www/vendor/dist/fonts/fredoka-one.woff',
        'www/vendor/dist/fonts/glyphicons-halflings-regular.eot',
        'www/vendor/dist/fonts/glyphicons-halflings-regular.svg',
        'www/vendor/dist/fonts/glyphicons-halflings-regular.ttf',
        'www/vendor/dist/fonts/glyphicons-halflings-regular.woff',
        'www/vendor/dist/fonts/ubuntu.eot',
        'www/vendor/dist/fonts/ubuntu.woff',
        'www/vendor/dist/fonts/ubuntu-bold.eot',
        'www/vendor/dist/fonts/ubuntu-bold.woff',
    ]),
    ('/usr/share/pritunl/www/js', [
        main_js_path,
        'www/vendor/dist/js/require.min.js',
    ]),
]

patch_files = []
if INSTALL_UPSTART:
    patch_files.append('%s/pritunl.conf' % PATCH_DIR)
    data_files.append(('/etc/init', ['%s/pritunl.conf' % PATCH_DIR]))
    data_files.append(('/etc/init.d', ['data/init.d/pritunl.sh']))
    shutil.copy('data/init/pritunl.conf', '%s/pritunl.conf' % PATCH_DIR)
if INSTALL_SYSTEMD:
    patch_files.append('%s/pritunl.service' % PATCH_DIR)
    data_files.append(('/etc/systemd/system',
        ['%s/pritunl.service' % PATCH_DIR]))
    shutil.copy('data/systemd/pritunl.service',
        '%s/pritunl.service' % PATCH_DIR)

for file_name in patch_files:
    for line in fileinput.input(file_name, inplace=True):
        line = line.replace('%PREFIX%', prefix)
        print line.rstrip('\n')

packages = ['pritunl']

for dir_name in os.listdir('pritunl'):
    if os.path.isdir(os.path.join('pritunl', dir_name)):
        packages.append('pritunl.%s' % dir_name)

setup(
    name='pritunl',
    version=VERSION,
    description='Pritunl vpn server',
    long_description=open('README.rst').read(),
    author='Pritunl',
    author_email='contact@pritunl.com',
    url='https://github.com/pritunl/pritunl',
    download_url='https://github.com/pritunl/pritunl/archive/%s.tar.gz' % (
        VERSION),
    keywords='openvpn, vpn, management, server, web interface',
    packages=packages,
    license=open('LICENSE').read(),
    zip_safe=False,
    install_requires=[
        'flask>=0.6',
        'pymongo>=2.5.2',
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': ['pritunl = pritunl.__main__:main'],
    },
    platforms=[
        'Linux',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Networking',
    ],
)
