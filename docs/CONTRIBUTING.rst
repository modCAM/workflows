************
Contributing
************

Build and test the project
==========================

The CMake presets supplied with this project use `vcpkg`_ to install the dependencies.

Note that the following commands include an optional ``FETCHCONTENT_SOURCE_DIR_MODCAM`` config setting. You only need to include this setting if you want to build bindings for a local copy of the modCAM C++ library. This can be useful if you're experimenting with new algorithms that haven't been added to the core C++ repository yet.

To install the project:

.. tab-set::
	:sync-group: install-cmd

	.. tab-item:: pip
		:sync: pip

		.. code-block:: bash

			# Requires pip >= 25.1
			python -m venv .venv
			source .venv/bin/activate
			python -m pip install . --group dev --config-setting=cmake.args="--preset vcpkg" [--config-setting=cmake.define.FETCHCONTENT_SOURCE_DIR_MODCAM="/path/to/modcam"]

	.. tab-item:: uv
		:sync: uv

		.. code-block:: bash

			uv sync --all-extras --dev --config-setting=cmake.args="--preset vcpkg" [--config-setting=cmake.define.FETCHCONTENT_SOURCE_DIR_MODCAM="/path/to/modcam"]

To run the unit tests:

.. tab-set::
	:sync-group: install-cmd

	.. tab-item:: pip
		:sync: pip

		.. code-block:: bash

			# Complete the installation steps above, and then...
			pytest

	.. tab-item:: uv
		:sync: uv

		.. code-block:: bash

			# No need to pre-install the project. This one command will build, install, and test it.
			uv run --all-extras --dev --config-setting=cmake.args="--preset vcpkg" [--config-setting=cmake.define.FETCHCONTENT_SOURCE_DIR_MODCAM="/path/to/modcam"] pytest

To build a wheel package for distribution:

.. tab-set::
	:sync-group: install-cmd

	.. tab-item:: pip
		:sync: pip

		.. code-block:: bash

			python -m venv .venv
			source .venv/bin/activate
			python -m pip wheel --no-deps . --config-setting=cmake.args="--preset vcpkg" [--config-setting=cmake.define.FETCHCONTENT_SOURCE_DIR_MODCAM="/path/to/modcam"]

	.. tab-item:: uv
		:sync: uv

		.. code-block:: bash

			# The wheel file will be placed in the dist/ directory.
			uv build --wheel --config-setting=cmake.args="--preset vcpkg" [--config-setting=cmake.define.FETCHCONTENT_SOURCE_DIR_MODCAM="/path/to/modcam"]

.. _vcpkg: https://vcpkg.io/

Build the documentation
=======================

Note that if you change a docstring, you will need to rebuild the project before re-running Sphinx. This can be problematic with uv, which caches the project. You'll need to run the above ``uv sync`` command with the ``--reinstall`` flag.

.. tab-set::
	:sync-group: install-cmd

	.. tab-item:: pip
		:sync: pip

		.. code-block:: bash

			# Requires pip >= 25.1
			python -m venv .venv
			source .venv/bin/activate
			python -m pip install . --group dev --group docs --config-setting=cmake.args="--preset vcpkg" [--config-setting=cmake.define.FETCHCONTENT_SOURCE_DIR_MODCAM="/path/to/modcam"]
			sphinx-build -a -E -b html docs/ build/docs/sphinx

	.. tab-item:: uv
		:sync: uv

		.. code-block:: bash

			uv run --all-extras --dev --group docs --config-setting=cmake.args="--preset vcpkg" [--config-setting=cmake.define.FETCHCONTENT_SOURCE_DIR_MODCAM="/path/to/modcam"] sphinx-build -a -E -b html docs/ build/docs/sphinx

Adding bindings
===============

Adding Python bindings for a modCAM function should largely be an exercise in copy-and-paste. The bindings should be placed in `src/py_modcam/<namespace>/<file>.cpp`, where each of the bindings files should mirror the corresponding core library file. The Doxygen documentation should be transformed to `NumPy style`_ docstrings.

.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html

Much of the boilerplate code generation is automated so that you don't have to worry about it. However, this automation also means that your bindings are expected to follow a particular structure. Here's an example where we bind the ``bar_baz2026`` algorithm in the ``foo`` namespace::

	// The file must be named bar_baz2026.cpp to match the function name.

	#include "default_types.h" 

	#include <modcam/foo/bar_baz2026.h>

	#include <nanobind/eigen/dense.h>
	#include <nanobind/nanobind.h>
	#include <nanobind/ndarray.h>

	namespace py = nanobind;
	using namespace py::literals;

	namespace py_modcam::foo { // This project uses the `py_modcam` namespace to
	                           // distinguish it from the core library `modcam`
	                           // namespace.

	// This function translates the C++ function to something that Python can use.
	// Note that
	// - It instantiates templates with concrete types.
	// - It converts some C++ asserts (checking the number of columns in input0)
	//   into Python errors. This is not necessary if the matrix dimension assertion
	//   is guaranteed by the template type instantiation.
	// - If multiple things are returned, then they should be grouped together into
	//   a tuple.
	auto bar_baz2026(
		const py::DRef<const Eigen::MatrixXN> &input0,
		const py::DRef<const Eigen::Matrix<int, Eigen::Dynamic, 3, Eigen::RowMajor>>
			&input1)
	{
		if (input0.cols() > 3 || input0.cols() < 2) {
			throw py::type_error("input0 must have two or three columns.");
		}

		std::tuple<Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>,
	               Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>>
			result;
		Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor> &result0 =
			std::get<0>(result);
		Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor> &result1 =
			std::get<1>(result);
		modcam::foo::bar_baz2026(result0, result1, input0, input1);
		return result;
	}

	// This function defines the bindings for py_modcam::foo::bar_baz2026. It must
	// have the `bind_` prefix followed by the name of the function being bound.
	void bind_bar_baz2026(py::module_ &m)
	{
		m.def("bar_baz2026", &py_modcam::foo::bar_baz2026,
		      "input0"_a, "input1"_a,
		      R"(
	Implement the bar algorithm as described in [baz2026]_.

	More detailed description here. This documentation should be copied from the C++
	function and reformatted according to the NumPy style guide.

	Parameters
	----------
	input0 : ndarray
		Description of `input0`.
	input1 : ndarray
		Description of `input1`.

	Returns
	-------
	ndarray
		Description of `result0`.
	ndarray
		Description of `result1`.

	References
	----------
	.. [baz2026] Baz, Bop. The amazing bar algorithm, 2000.
	)");
	}

	} // namespace py_modcam::foo
