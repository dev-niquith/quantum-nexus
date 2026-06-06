from backend.molecule_visualizer import generate_molecule_image

img = generate_molecule_image("CCO")

img.save("test_molecule.png")