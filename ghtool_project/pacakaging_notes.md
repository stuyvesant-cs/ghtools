# Changes to create pip-able package

- python files copied to `ghtool_project/src/ghtool`
- rename `ghtool.py` to `cli.py`
- change relative imports to `from . import create_assignment` etc


# Bot advice for publishing on PyPi
Step C: Test with TestPyPI (Highly Recommended)
  Do not upload to the real PyPI first. There is a separate instance called [TestPyPI](https://test.pypi.org/) designed
  exactly for this. It allows you to see if your package renders correctly and installs properly without "polluting" the
  real index.

  1.  Create an account on [TestPyPI](https://test.pypi.org/).
  2.  Upload your build to TestPyPI:
        python -m twine upload --repository testpypi dist/*
  3.  Try installing your package from TestPyPI to see if it works:
        pip install --index-url https://test.pypi.org/simple/ ghtool

  Step D: Upload to the real PyPI
  Once you are 100% sure everything works, upload to the real index:
    python -m twine upload dist/*

  ---

  3. Essential Security Note: Use API Tokens
  When twine asks for a username and password:
  *   Username: Enter __token__ (literally that string).
  *   Password: Enter the API Token you generated from your PyPI account
  settings.

  Never use your actual PyPI account password in the terminal. Using an API token is much safer; if your computer is
  compromised, you can simply revoke the token without needing to change your main account
  password.

  ---

  4. Pro-Tips for a Professional Package

  1.  `.gitignore`: Before uploading, ensure you have a .gitignore file in your root directory so you don't accidentally
  upload __pycache__, .env files (which might contain secrets), or local build artifacts to your git
  repository.
  2.  Version Management: Every time you want to update your package on PyPI, you must change the version = "0.1.0" in
  pyproject.toml to something higher (e.g., 0.1.1). PyPI will reject an upload if the version number already
  exists.
  3.  License: Always include a LICENSE file (like MIT or Apache 2.0) so others know how they are legally allowed to use
  your code.
  4.  README: Ensure your README.md is descriptive. This is the "homepage" of your project on PyPI; it's what users see when
  they look up your package.
