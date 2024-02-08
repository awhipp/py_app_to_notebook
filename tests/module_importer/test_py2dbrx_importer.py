"""Test the py2databricks importer module."""

import sys
import pytest

import py2databricks.module_importer.py2dbrx_importer as importer

# ! Tests are not 1:1 because in notebooks they share the same globals()

def test_define_checkpoint():
    """Test the define checkpoint method to ensure globals() is stored."""
    file_uuid = importer.define_checkpoint()

    assert f"checkpoint-{file_uuid}" in list(importer.__dict__.keys())

@pytest.mark.parametrize("module_name", [
    "test_module", 
    "test_module.example", 
    "test_module.example.submodule", 
    "test_module.example.submodule.subsubmodule"
])
def test_update_modules_from_checkpoint(module_name):
    """Test the update modules from checkpoint method to ensure globals() is updated."""
    
    file_uuid = importer.define_checkpoint()

    importer.update_modules_from_checkpoint(file_uuid, module_name)

    assert module_name in list(sys.modules.keys())

def test_update_modules_from_checkpoint_no_checkpoint():
    """Test the update modules when the checkpoint does not exist."""

    with pytest.raises(KeyError):
        importer.update_modules_from_checkpoint("fake_uuid", 'test.module')

def test_get_all_module_chunks():
    """Test the get all module chunks method to ensure the correct chunks are returned."""
    modules = ["test", "module", "example"]

    chunks = list(importer.get_all_module_chunks(modules))

    assert chunks == ["test", "test.module", "test.module.example"]