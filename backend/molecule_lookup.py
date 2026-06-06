import pubchempy as pcp


def get_molecule_info(name: str):

    try:

        compounds = pcp.get_compounds(
            name,
            "name"
        )

        if not compounds:
            return None

        compound = compounds[0]

        return {
            "name": compound.iupac_name or compound.synonyms[0] if compound.synonyms else None,
            "formula": compound.molecular_formula,
            "molecular_weight": compound.molecular_weight,
            "smiles": compound.connectivity_smiles
        }

    except Exception:
        return None


def get_molecule_from_smiles(smiles: str):

    try:

        compounds = pcp.get_compounds(
            smiles,
            namespace="smiles"
        )

        if not compounds:
            return None

        compound = compounds[0]

        return {
            "name": compound.iupac_name or compound.synonyms[0] if compound.synonyms else None,
            "formula": compound.molecular_formula,
            "molecular_weight": compound.molecular_weight,
            "smiles": compound.connectivity_smiles
        }

    except Exception:
        return None