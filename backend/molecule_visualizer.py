from io import BytesIO

from rdkit import Chem
from rdkit.Chem import Draw


def generate_molecule_image(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    img = Draw.MolToImage(
        mol,
        size=(400, 300)
    )

    buffer = BytesIO()

    img.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return buffer