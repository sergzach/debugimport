"""
A testing executor with pytest.
"""
import shutil
import os
from shutil import rmtree
from tempfile import mkdtemp
import subprocess
from venv import EnvBuilder

_CUR_DIR = os.path.dirname(os.path.realpath(__file__))


class _DebugImportEnvBuilder(EnvBuilder):
    """
    A custom env. builder to setup a sample app which we would import.
    """
    _PYLIB_INSTALL_TEMPLATE = '{env_exe} -m pip install {pylibs}'

    def __init__(   self, 
                    system_site_packages=False, 
                    clear=False,
                    symlinks=False, 
                    upgrade=False, 
                    with_pip=False, 
                    prompt=None,
                    *,
                    install_pylibs,
                    setup_paths):
        """
        :param bool system_site_packages: If True, the system (global) site-packages
            dir is available to created environments.
        :param bool clear: If True, delete the contents of the environment directory 
            if it already exists, before environment creation.
        :param bool symlinks: If True, attempt to symlink rather than copy files 
            into virtual environment.
        :param bool upgrade: If True, upgrade an existing virtual environment.
        :param bool with_pip: If True, ensure pip is installed in the virtual 
            environment.
        :param str prompt: Alternative terminal prefix for the environment.
        :param List[Str] install_pylibs: Libraries to install to the venv.
        :param List[Str] setup_paths: Paths with setup.py files to install
        libraries by executing `python3 setup.py install`.
        """
        super().__init__(   system_site_packages,
                            clear,
                            symlinks,
                            upgrade,
                            with_pip,
                            prompt)
        self._install_pylibs = install_pylibs or []
        self._setup_paths = setup_paths or []
        self.env_exe = None

    def post_setup(self, context):
        """
        Place here all libraries which can be imported by tests (from venv).

        :param types.SimpleNamespace context: A context of current venv object.
        """
        self.env_exe = context.env_exe
        self._make_install_pylibs()
        self._make_setup()

    def _make_install_pylibs(self):
        """
        Install all libraries from self._PYLIB_INSTALL_TEMPLATE to the `venv`.
        """
        install_pylibs_args = self._PYLIB_INSTALL_TEMPLATE.format(
            env_exe=self.env_exe, 
            pylibs=' '.join(self._install_pylibs)
        ).split()
        subprocess.call(install_pylibs_args)

    def _make_setup(self):
        """
        Setup all libraries from `self.setup_path`.
        """
        tmp_setup_root = mkdtemp()
        try:
            for setup_path in self._setup_paths:
                setup_dir = os.path.dirname(setup_path)
                setup_postfix = os.path.basename(setup_dir)
                tmp_setup_dir = os.path.join(tmp_setup_root, setup_postfix)
                shutil.copytree(setup_dir, tmp_setup_dir)
                tmp_setup_dir = os.path.join( 
                    tmp_setup_root, 
                    os.path.basename(setup_dir)
                )
                subprocess.call(    [self.env_exe, setup_path, 'install'], 
                                    cwd=tmp_setup_dir)
        except Exception:
            raise
        finally:            
            shutil.rmtree(tmp_setup_root)


class TestDebugImport:
    """
    The main testing class.
    """
    _TEST_APP_NAME = 'testapp'
    _TEST_APP_DIR = os.path.join(_CUR_DIR, '..', 'test_data', _TEST_APP_NAME)
    _env_exe = None

    def setup_class(cls):
        """
        Initial actions for all tests.
        """
        cls._env_builder_dir = None
        cls._setup_testapps()

    @classmethod
    def teardown_class(cls):
        """
        Cleaning actions for all tests.
        """
        cls._cleanup_testapp()

    @classmethod
    def _setup_testapps(cls):        
        """
        Set up a sample application to test debug importing to venv.
        """
        env_builder = _DebugImportEnvBuilder(
            with_pip=True,
            install_pylibs=['setuptools'],
            setup_paths=[
                os.path.join(cls._TEST_APP_DIR,'setup.py') 
            ]
        )
        cls._env_builder_dir = mkdtemp()
        env_builder.create(cls._env_builder_dir)
        cls._env_exe = env_builder.env_exe

    def _env_python_call(self, code):
        """
        Call an external py code env builder environment and return the output.

        :param str code: A code to execute.
        """
        try:
            output = subprocess.check_output(   [self._env_exe, '-c', code], 
                                                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            raise Exception(exc.output)
        return output

    def _execute_test_code(self, *, is_debug):
        """
        Execute a common code for test.

        :param bool is_debug: If True then import in debug mode otherwise
        in production mode.
        """
        test_output = self._env_python_call(
            f'from debugimport import debug_import\n'
            f'mod = debug_import( "{self._TEST_APP_NAME}",'
            f'"{self._TEST_APP_DIR}",'
            f'{is_debug});'
            f'mod.main()'
        )
        test_output = test_output.strip()
        return test_output

    def test_debug(self):
        """
        The test of debug import (is_debug=True).

        Import the module, call the function main from it and check it's output
        is 'imported'.
        """
        test_output = self._execute_test_code(is_debug=True)
        assert test_output == b'imported'

    def test_prod(self):
        """
        The test of debug import (is_debug=False).

        Import the module, call the function main from it and check it's output
        is 'imported'.
        """
        test_output = self._execute_test_code(is_debug=False)
        assert test_output == b'imported'

    @classmethod
    def _cleanup_testapp(cls):
        """
        Remove a venv directory of a sample application.
        """
        rmtree(cls._env_builder_dir)
