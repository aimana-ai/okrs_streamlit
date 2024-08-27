import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['ubuntu']).generate()
print(hashed_passwords)