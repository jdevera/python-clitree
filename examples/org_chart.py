from collections import defaultdict

from clitree import tree

# List of (name, position, manager) with Spanish names
ORG_TUPLES = [
    ("Juan García", "CEO", None),
    ("Alicia Fernández", "VP Ingeniería", "Juan García"),
    ("Wendy Moreno", "VP Producto", "Juan García"),
    ("Tina Ruiz", "VP Operaciones", "Juan García"),
    ("Roberto Torres", "Director Backend", "Alicia Fernández"),
    ("Iván Martínez", "Director Frontend", "Alicia Fernández"),
    ("Pedro Reyes", "Director QA", "Alicia Fernández"),
    ("Javier Díaz", "Director UX", "Wendy Moreno"),
    ("Eva Castro", "Director PM", "Wendy Moreno"),
    ("León Morales", "Director Datos", "Wendy Moreno"),
    ("Ulises Vega", "Director RRHH", "Tina Ruiz"),
    ("Beatriz Gil", "Director Finanzas", "Tina Ruiz"),
    ("Ignacio Navarro", "Director IT", "Tina Ruiz"),
    ("Patricia Ramos", "Director Legal", "Tina Ruiz"),
    ("Carlos Blanco", "Manager Backend 1", "Roberto Torres"),
    ("Francisco Molina", "Manager Backend 2", "Roberto Torres"),
    ("Joaquín Romero", "Manager Frontend 1", "Iván Martínez"),
    ("Miriam Gómez", "Manager Frontend 2", "Iván Martínez"),
    ("Quintín Alonso", "Manager QA 1", "Pedro Reyes"),
    ("Tomás Bravo", "Manager QA 2", "Pedro Reyes"),
    ("Yara Esteban", "Manager UX 1", "Javier Díaz"),
    ("Benjamín Jiménez", "Manager UX 2", "Javier Díaz"),
    ("Federico Granados", "Manager PM 1", "Eva Castro"),
    ("Irene Jurado", "Manager PM 2", "Eva Castro"),
    ("Mayra Nieto", "Manager Datos 1", "León Morales"),
    ("Pablo Quintana", "Manager Datos 2", "León Morales"),
    ("Verónica Aguirre", "Manager RRHH 1", "Ulises Vega"),
    ("Yolanda Domínguez", "Manager RRHH 2", "Ulises Vega"),
    ("César Herrera", "Manager Finanzas 1", "Beatriz Gil"),
    ("Fiona Lara", "Manager Finanzas 2", "Beatriz Gil"),
    ("Julia Ortega", "Manager IT 1", "Ignacio Navarro"),
    ("Miguel Suárez", "Manager IT 2", "Ignacio Navarro"),
    ("Quirino Barrera", "Manager Legal 1", "Patricia Ramos"),
    ("Tatiana Escobar", "Manager Legal 2", "Patricia Ramos"),
    ("David Méndez", "IC Backend 1", "Carlos Blanco"),
    ("Elena Delgado", "IC Backend 2", "Carlos Blanco"),
    ("Gabriel Tejada", "IC Backend 3", "Francisco Molina"),
    ("Héctor Andrade", "IC Backend 4", "Francisco Molina"),
    ("Karina León", "IC Frontend 1", "Joaquín Romero"),
    ("Luis Blanco", "IC Frontend 2", "Joaquín Romero"),
    ("Nora Cordero", "IC Frontend 3", "Miriam Gómez"),
    ("Olga Herrera", "IC Frontend 4", "Miriam Gómez"),
    ("Raúl Sanz", "IC QA 1", "Quintín Alonso"),
    ("Sofía Verde", "IC QA 2", "Quintín Alonso"),
    ("Úrsula Paredes", "IC QA 3", "Tomás Bravo"),
    ("Vicente Lobo", "IC QA 4", "Tomás Bravo"),
    ("Zaira Fuentes", "IC UX 1", "Yara Esteban"),
    ("Aarón Hidalgo", "IC UX 2", "Yara Esteban"),
    ("Carla Lamas", "IC UX 3", "Benjamín Jiménez"),
    ("Damián Montes", "IC UX 4", "Benjamín Jiménez"),
    ("Gisela Hoyos", "IC PM 1", "Federico Granados"),
    ("Hugo Ibarra", "IC PM 2", "Federico Granados"),
    ("Jorge Kuri", "IC PM 3", "Irene Jurado"),
    ("Katia Lobo", "IC PM 4", "Irene Jurado"),
    ("Nicolás Olmedo", "IC Datos 1", "Mayra Nieto"),
    ("Ofelia Prieto", "IC Datos 2", "Mayra Nieto"),
    ("Rita Salas", "IC Datos 3", "Pablo Quintana"),
    ("Samuel Torres", "IC Datos 4", "Pablo Quintana"),
    ("Walter Benítez", "IC RRHH 1", "Verónica Aguirre"),
    ("Ximena Cobo", "IC RRHH 2", "Verónica Aguirre"),
    ("Zulema Díaz", "IC RRHH 3", "Yolanda Domínguez"),
    ("Alonso Figueroa", "IC RRHH 4", "Yolanda Domínguez"),
    ("Diana Iglesias", "IC Finanzas 1", "César Herrera"),
    ("Esteban Jiménez", "IC Finanzas 2", "César Herrera"),
    ("Guadalupe Lira", "IC Finanzas 3", "Fiona Lara"),
    ("Helena Molina", "IC Finanzas 4", "Fiona Lara"),
    ("Kevin Ponce", "IC IT 1", "Julia Ortega"),
    ("Laura Quintana", "IC IT 2", "Julia Ortega"),
    ("Nuria Ríos", "IC IT 3", "Miguel Suárez"),
    ("Octavio Sánchez", "IC IT 4", "Miguel Suárez"),
    ("Rocío Torres", "IC Legal 1", "Quirino Barrera"),
    ("Sergio Urrutia", "IC Legal 2", "Quirino Barrera"),
    ("Ulises Vargas", "IC Legal 3", "Tatiana Escobar"),
    ("Valeria Zúñiga", "IC Legal 4", "Tatiana Escobar"),
]


def build_org_tree(tuples):
    nodes = {}
    children = defaultdict(list)
    for name, position, manager in tuples:
        nodes[name] = {"name": f"{name} ({position})"}
        if manager:
            children[manager].append(name)
    for manager, reports in children.items():
        nodes[manager]["reports"] = [nodes[r] for r in reports]
    root = next(
        n
        for n, (name, position, manager) in zip(nodes.values(), tuples)
        if manager is None
    )
    return root


if __name__ == "__main__":
    org_chart = build_org_tree(ORG_TUPLES)
    print(tree(org_chart, children="reports"))
