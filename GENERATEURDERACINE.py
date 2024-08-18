import streamlit as st
import pandas as pd
import os

# Fichier CSV pour stocker les codes racines
CSV_FILE = 'codes_racines.csv'
STARTING_NUMBER = 7638920

# Chargés d'affaires initiaux
charged_affaires = ['Mme FAYE', 'Mme NDIAYE', 'M. DIENG']


# Fonction pour générer un code racine basé sur un compteur
def generate_code_racine():
    if not os.path.exists(CSV_FILE):
        code = STARTING_NUMBER
    else:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            code = STARTING_NUMBER
        else:
            code = df['Code Racine'].max() + 1
    return code


# Fonction pour sauvegarder un code racine dans le fichier CSV
def save_code_to_csv(charged_affaire, registre, nom_entreprise, code_racine):
    new_row = pd.DataFrame({
        'Chargé d\'Affaires': [charged_affaire],
        'Numéro de Registre': [registre],
        'Nom de l\'Entreprise': [nom_entreprise],
        'Code Racine': [code_racine]
    })

    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Chargé d\'Affaires', 'Numéro de Registre', 'Nom de l\'Entreprise', 'Code Racine'])
    else:
        df = pd.read_csv(CSV_FILE)

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)


# Fonction pour supprimer un code racine du fichier CSV
def delete_code_from_csv(code_racine):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = df[df['Code Racine'] != code_racine]
        df.to_csv(CSV_FILE, index=False)


# Fonction pour modifier un code racine dans le fichier CSV
def modify_code_in_csv(old_code, new_code):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df.loc[df['Code Racine'] == old_code, 'Code Racine'] = new_code
        df.to_csv(CSV_FILE, index=False)


# Interface Streamlit
def main():
    st.title('Application de Génération de Codes Racines SUNU ROUME')

    # Sélection du chargé d'affaires
    st.sidebar.header('Gestion des Chargés d\'Affaires')
    selected_affaire = st.sidebar.selectbox('Choisissez un chargé d\'affaires', charged_affaires)
    add_affaire = st.sidebar.text_input('Ajouter un nouveau chargé d\'affaires')

    if add_affaire:
        charged_affaires.append(add_affaire)
        st.sidebar.success(f'Chargé d\'affaires "{add_affaire}" ajouté.')

    # Saisie des informations
    st.header('Saisie des Informations')
    registre = st.text_input('Numéro de registre de commerce')
    nom_entreprise = st.text_input('Nom de l\'entreprise')

    if st.button('Générer Code Racine'):
        if registre and nom_entreprise:
            code_racine = generate_code_racine()
            save_code_to_csv(selected_affaire, registre, nom_entreprise, code_racine)
            st.success(f'Code racine généré : {code_racine}')
        else:
            st.error('Veuillez entrer toutes les informations requises.')

    st.header('Gestion des Codes Racines')
    st.subheader('Supprimer un Code Racine')
    delete_code = st.text_input('Code racine à supprimer')
    if st.button('Supprimer Code Racine'):
        if delete_code:
            delete_code_from_csv(int(delete_code))
            st.success(f'Code racine {delete_code} supprimé.')
        else:
            st.error('Veuillez entrer le code racine à supprimer.')

    st.subheader('Modifier un Code Racine')
    old_code = st.text_input('Code racine à modifier')
    new_code = st.text_input('Nouveau code racine')
    if st.button('Modifier Code Racine'):
        if old_code and new_code:
            modify_code_in_csv(int(old_code), int(new_code))
            st.success(f'Code racine {old_code} modifié en {new_code}.')
        else:
            st.error('Veuillez entrer les codes racines à modifier.')

    st.header('Codes Racines en Mémoire')
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        st.dataframe(df)
    else:
        st.write('Aucun code racine enregistré.')


if __name__ == "__main__":
    main()