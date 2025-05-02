import streamlit as st


if not st.user.is_logged_in:
    if st.button("Log in"):
        st.login()
    st.stop()  # Execution stops here for unauthenticated users
else:
    if st.button("Log out"):
        st.logout()

    # Check for admin status based on email domain
    if st.user.email in st.secrets.security.admins:
        st.write(f"Welcome, {st.user.name}!")
        # Show admin-only features here
    else:
        st.write(f"User ({st.user.name}) not authorized")
        st.stop()