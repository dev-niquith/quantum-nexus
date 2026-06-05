from backend.descriptor_engine import extract_descriptors


def test_extract_descriptors():

    result = extract_descriptors("CCO")

    assert result is not None

    assert "MolWt" in result

    assert "TPSA" in result

    assert result["MolWt"] > 0