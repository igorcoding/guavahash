from __future__ import print_function

from distutils.core import setup, Extension
import os
import shutil
import platform

version = '0.3'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def local_file(filename):
    return os.path.join(BASE_DIR, filename)


print('-----------------')
print('Platform: ' + platform.system())
print('-----------------')

c_files = [
    'src/guava.c',
]

# Make VS treat *.c files as *.cpp
# (/TP flag being ignored)
tmp_dir = None
if platform.system() == 'Windows':
    tmp_dir = local_file(os.path.join('.', 'tmp'))
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    cpp_files = list(map(lambda f: os.path.join('tmp', f + 'pp'), c_files))

    for i in range(len(c_files)):
        shutil.copy(local_file(c_files[i]), local_file(cpp_files[i]))

    c_files = cpp_files

# define the extension module
module = Extension('guavahash',
                   sources=[local_file(f) for f in c_files],
                   include_dirs=[local_file('.')],
                   language='c'
                   )

# run the setup
setup(name='guavahash',
      ext_modules=[module],
      version=version,
      description='Google\'s Guava consistent hashing implementation',
      long_description="""Google's Guava consistent hashing implementation
      
      
      Assign to `input` a "bucket" in the range `[0, buckets)`, in a uniform manner
      that minimizes the need for remapping as `buckets` grows.
      That is, `consistentHash(h, n)` equals:

      * `n - 1`, with approximate probability `1/n`;
      * `consistentHash(h, n - 1)`, otherwise (probability `1 - 1/n`).

      See the [wikipedia article on consistent hashing](http://en.wikipedia.org/wiki/Consistent_hashing)
      for more information.
      """,
      author='igorcoding',
      author_email='igorcoding@gmail.com',
      url='https://github.com/igorcoding/guavahash',
      download_url='https://github.com/igorcoding/guavahash/tarball/v' + version,
      license='MIT License',
      keywords='guava consistent hashing hash digest',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      )

if platform.system() == 'Windows':
    shutil.rmtree(tmp_dir)
