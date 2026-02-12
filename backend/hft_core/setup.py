from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys

# 1. Platform-specific flags
c_args = []
if sys.platform == "win32":
    c_args = ["/std:c++17", "/O2"]  # Windows (MSVC) flags
else:
    c_args = ["-std=c++17", "-O3"]  # Linux/Mac (GCC/Clang) flags


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed."""

    def __str__(self):
        import pybind11

        return pybind11.get_include()


ext_modules = [
    Extension(
        "hft_engine",
        sorted(["src/engine/order_book.cpp", "bindings/python_bindings.cpp"]),
        include_dirs=[get_pybind_include(), "include"]
        language="c++",
        extra_compile_args=c_args,  # <--- THIS IS THE FIX
    ),
]

setup(
    name="hft_engine",
    version="0.0.1",
    author="Rohit Thanvi",
    description="C++ HFT Core for Hybrid Simulator",
    ext_modules=ext_modules,
    setup_requires=["pybind11>=2.10.0"],
    install_requires=["pybind11>=2.10.0"],
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
