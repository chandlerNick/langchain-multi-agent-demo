# Makefile "Routeur" Multi-OS
# Ce fichier détecte automatiquement le système d'exploitation
# et inclut le fichier de configuration approprié.

ifeq ($(OS),Windows_NT)
    # Détection Windows
    include Makefile.win
else
    # Détection Linux / MacOS
    include Makefile.linux
endif

# Cible par défaut pour vérifier quel OS est détecté
check-os:
ifeq ($(OS),Windows_NT)
	@echo "Système détecté : Windows (Utilisation de Makefile.win)"
else
	@echo "Système détecté : Linux/Mac (Utilisation de Makefile.linux)"
endif