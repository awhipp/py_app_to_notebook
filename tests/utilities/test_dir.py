from py_app_to_notebook.utilities.dir import Dependency


class TestDependency():
    """Test the Dependency class."""

    dependency: Dependency = Dependency(root='queue_to_s3_sample', path='queue_to_s3_sample/app.py')

    def test_dependency_tree_string(self):
        """Test the dependency tree string."""

        # ARRANGE
        expected_tree = """app (queue_to_s3_sample\\app.py)
----app.sqs (queue_to_s3_sample\\aws_helpers\sqs.py)
--------app.sqs.boto_helpers (queue_to_s3_sample\\aws_helpers\\boto_helpers.py)
----app.s3 (queue_to_s3_sample\\aws_helpers\s3.py)
--------app.s3.boto_helpers (queue_to_s3_sample\\aws_helpers\\boto_helpers.py)
----app.boto_helpers (queue_to_s3_sample\\aws_helpers\\boto_helpers.py)
"""

        # ACT
        tree = self.dependency.dependency_tree_as_string()

        # ASSERT
        assert tree == expected_tree