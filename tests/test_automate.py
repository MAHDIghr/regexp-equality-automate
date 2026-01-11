from src.automate import *
import traceback
from src.visualize import save_pdf

# Variable pour stocker tous les automates à visualiser
pdf_content = []


def run_test(name, func):
    try:
        func()
        print(f"✅ OK : {name}")
    except Exception as e:
        print(f"❌ FAIL : {name}")
        print("   →", e)
        traceback.print_exc()


def add_to_pdf(title, automate):
    """Ajoute un automate au PDF"""
    pdf_content.append((title, automate))


# ===========================
# TESTS UNION
# ===========================
def test_union():
    print("\n=== Tests UNION ===")
    
    # Test 1: a + b
    print("Test 1: a + b")
    a = automate("a")
    b = automate("b")
    u = union(a, b)
    
    add_to_pdf("UNION Test 1: Automate a", a)
    add_to_pdf("UNION Test 1: Automate b", b)
    add_to_pdf("UNION Test 1: Résultat a+b", u)
    
    assert isinstance(u, automate)
    assert len(u.final) == 1
    print("  ✓ OK")
    
    # Test 2: a + a
    print("Test 2: a + a")
    a1 = automate("a")
    a2 = automate("a")
    u2 = union(a1, a2)
    
    add_to_pdf("UNION Test 2: Automate a", a1)
    add_to_pdf("UNION Test 2: Automate a (copie)", a2)
    add_to_pdf("UNION Test 2: Résultat a+a", u2)
    
    assert isinstance(u2, automate)
    assert len(u2.final) == 1
    print("  ✓ OK")
    
    # Test 3: (a+b) + c
    print("Test 3: (a+b) + c")
    a3 = automate("a")
    b3 = automate("b")
    c3 = automate("c")
    u_ab = union(a3, b3)
    u3 = union(u_ab, c3)
    
    add_to_pdf("UNION Test 3: Union a+b", u_ab)
    add_to_pdf("UNION Test 3: Automate c", c3)
    add_to_pdf("UNION Test 3: Résultat (a+b)+c", u3)
    
    assert isinstance(u3, automate)
    print("  ✓ OK")


# ===========================
# TESTS CONCATENATION
# ===========================
def test_concat():
    print("\n=== Tests CONCATENATION ===")
    
    # Test 1: a.b
    print("Test 1: a.b")
    a = automate("a")
    b = automate("b")
    c = concatenation(a, b)
    
    add_to_pdf("CONCAT Test 1: Automate a", a)
    add_to_pdf("CONCAT Test 1: Automate b", b)
    add_to_pdf("CONCAT Test 1: Résultat a.b", c)
    
    assert isinstance(c, automate)
    assert len(c.final) >= 1
    print("  ✓ OK")
    
    # Test 2: a.E
    print("Test 2: a.E")
    a2 = automate("a")
    e = automate("E")
    c2 = concatenation(a2, e)
    
    add_to_pdf("CONCAT Test 2: Automate a", a2)
    add_to_pdf("CONCAT Test 2: Automate E", e)
    add_to_pdf("CONCAT Test 2: Résultat a.E", c2)
    
    assert isinstance(c2, automate)
    print("  ✓ OK")
    
    # Test 3: (a.b).c
    print("Test 3: (a.b).c")
    a3 = automate("a")
    b3 = automate("b")
    c3 = automate("c")
    c_ab = concatenation(a3, b3)
    c_final = concatenation(c_ab, c3)
    
    add_to_pdf("CONCAT Test 3: Concat a.b", c_ab)
    add_to_pdf("CONCAT Test 3: Automate c", c3)
    add_to_pdf("CONCAT Test 3: Résultat (a.b).c", c_final)
    
    assert isinstance(c_final, automate)
    print("  ✓ OK")


# ===========================
# TESTS ÉTOILE
# ===========================
def test_etoile():
    print("\n=== Tests ÉTOILE ===")
    
    # Test 1: a*
    print("Test 1: a*")
    a = automate("a")
    e = etoile(a)
    
    add_to_pdf("ETOILE Test 1: Automate a", a)
    add_to_pdf("ETOILE Test 1: Résultat a*", e)
    
    assert isinstance(e, automate)
    assert len(e.final) == 1
    print("  ✓ OK")
    
    # Test 2: (a+b)*
    print("Test 2: (a+b)*")
    a2 = automate("a")
    b2 = automate("b")
    u = union(a2, b2)
    e2 = etoile(u)
    
    add_to_pdf("ETOILE Test 2: Union a+b", u)
    add_to_pdf("ETOILE Test 2: Résultat (a+b)*", e2)
    
    assert isinstance(e2, automate)
    print("  ✓ OK")
    
    # Test 3: E*
    print("Test 3: E*")
    e_auto = automate("E")
    e3 = etoile(e_auto)
    
    add_to_pdf("ETOILE Test 3: Automate E", e_auto)
    add_to_pdf("ETOILE Test 3: Résultat E*", e3)
    
    assert isinstance(e3, automate)
    print("  ✓ OK")


# ===========================
# TESTS DÉTERMINISATION
# ===========================
def test_determinisation():
    print("\n=== Tests DÉTERMINISATION ===")
    
    # Test 1: Automate non-déterministe simple
    print("Test 1: Automate ND simple")
    nd = automate()
    nd.n = 3
    nd.final = [2]
    nd.transition = {
        (0, 'a'): [1, 2],
        (1, 'b'): [2],
        (2, 'a'): [2]
    }
    nd.name = "ND"
    
    det = determinisation(nd)
    
    add_to_pdf("DETER Test 1: Entrée ND", nd)
    add_to_pdf("DETER Test 1: Résultat Déterministe", det)
    
    for (q, c), dests in det.transition.items():
        assert len(dests) == 1  # doit être déterministe
    print("  ✓ OK")
    
    # Test 2: Union a+b
    print("Test 2: Union a+b")
    a = automate("a")
    b = automate("b")
    u = union(a, b)
    no_eps = supression_epsilon_transitions(u)
    det2 = determinisation(no_eps)
    
    add_to_pdf("DETER Test 2: Union a+b", u)
    add_to_pdf("DETER Test 2: Sans epsilon", no_eps)
    add_to_pdf("DETER Test 2: Résultat Déterministe", det2)
    
    for (q, c), dests in det2.transition.items():
        assert len(dests) == 1
    print("  ✓ OK")


# ===========================
# TESTS COMPLETION
# ===========================
def test_completion():
    print("\n=== Tests COMPLETION ===")
    
    # Test 1: Automate incomplet
    print("Test 1: Automate incomplet")
    inc = automate()
    inc.n = 2
    inc.final = [1]
    inc.transition = {
        (0, 'a'): [1],
        (1, 'b'): [1]
    }
    
    comp = completion(inc)
    
    add_to_pdf("COMPL Test 1: Entrée incomplète", inc)
    add_to_pdf("COMPL Test 1: Résultat complet", comp)
    
    assert isinstance(comp, automate)
    print("  ✓ OK")
    
    # Test 2: Automate déjà complet
    print("Test 2: Automate déjà complet")
    compl_auto = automate()
    compl_auto.n = 1
    compl_auto.final = [0]  # état 0 est final
    compl_auto.transition = {
        (0, 'a'): [0],
        (0, 'b'): [0],
        (0, 'c'): [0]
    }
    compl_auto.name = "Complet"
    
    # Appliquer completion (ne devrait rien changer)
    comp2 = completion(compl_auto)
    
    add_to_pdf("COMPL Test 2: Entrée complète", compl_auto)
    add_to_pdf("COMPL Test 2: Résultat complet", comp2)
    
    assert comp2.n == compl_auto.n  # doit rester identique
    print("  ✓ OK")


# ===========================
# TESTS ÉGAL
# ===========================
def test_egalite():
    print("\n=== Tests ÉGAL ===")
    
    # Test 1: Deux automates identiques
    print("Test 1: a == a")
    a1 = automate("a")
    a2 = automate("a")
    result1 = egal(a1, a2)
    
    add_to_pdf("EGAL Test 1: Automate a", a1)
    add_to_pdf("EGAL Test 1: Automate a (copie)", a2)
    add_to_pdf(f"EGAL Test 1: Résultat = {result1}", a1)
    
    assert result1 == True
    print("  ✓ OK")
    
    # Test 2: Deux automates différents
    print("Test 2: a != b")
    a3 = automate("a")
    b = automate("b")
    result2 = egal(a3, b)
    
    add_to_pdf("EGAL Test 2: Automate a", a3)
    add_to_pdf("EGAL Test 2: Automate b", b)
    add_to_pdf(f"EGAL Test 2: Résultat = {result2}", a3)
    
    assert result2 == False
    print("  ✓ OK")
    
    # Test 3: Automates isomorphes
    print("Test 3: Automates isomorphes")
    iso1 = automate()
    iso1.n = 2
    iso1.final = [1]
    iso1.transition = {(0, 'a'): [1], (1, 'b'): [1]}
    
    iso2 = automate()
    iso2.n = 2
    iso2.final = [1]
    iso2.transition = {(0, 'a'): [1], (1, 'b'): [1]}
    
    result3 = egal(iso1, iso2)
    
    add_to_pdf("EGAL Test 3: Automate 1", iso1)
    add_to_pdf("EGAL Test 3: Automate 2", iso2)
    add_to_pdf(f"EGAL Test 3: Résultat = {result3}", iso1)
    
    assert result3 == True
    print("  ✓ OK")


# ===========================
# LANCEUR PRINCIPAL
# ===========================
def run_all_tests():
    print("=" * 60)
    print("LANCEMENT DE TOUS LES TESTS")
    print("=" * 60)
    
    # Vider le contenu PDF
    global pdf_content
    pdf_content = []
    
    # Liste de tous les tests
    tests = [
        ("Union", test_union),
        ("Concatenation", test_concat),
        ("Etoile", test_etoile),
        ("Determinisation", test_determinisation),
        ("Completion", test_completion),
        ("Egalite", test_egalite),
    ]
    
    # Exécuter tous les tests
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}: TOUS LES TESTS PASSÉS")
        except Exception as e:
            print(f"❌ {name}: ÉCHEC - {e}")
        print("-" * 40)
    
    # Sauvegarder le PDF
    if pdf_content:
        save_pdf(pdf_content, "tests/tests_automates.pdf")
        print(f"\n📄 PDF généré : tests/tests_automates.pdf")
    else:
        print("\n⚠️ Aucun automate à sauvegarder dans le PDF")
    
    print("=" * 60)
    print("FIN DES TESTS")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()