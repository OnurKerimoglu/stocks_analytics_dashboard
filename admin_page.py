from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st

from src.utils import get_ishares_etfs, run_query
from src.queries import Queries


queries = Queries()

def sequential_df_filter(df, to_filter_columns):
    for col in to_filter_columns:
        col_pretty = col.replace("_", " ").title()
        choices = st.multiselect(
            f"Select {col_pretty}",
            list(df[col].unique()))
        df = df[df[col].isin(choices)]
    return df

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
        manager, browser = st.tabs(["Manager", "Browser"])

        with manager:
            st.subheader(f"Manage Tracked ETFs:")
            user = st.user.name
            user_etfs_query = queries.user_etfs(user)
            df = run_query(user_etfs_query)
            st.write("Select rows")
            event = st.dataframe(
                    df,
                    # column_config=column_configuration,
                    use_container_width=True,
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="multi-row",
                )
        with browser:
            st.subheader(f"Browse ETFs:")
            etfs = get_ishares_etfs()
            etfs_filt = sequential_df_filter(
                    etfs,
                    ['region', 'country', 'subasset_class'])
            if etfs_filt.shape[0] > 0:
                st.write("Select rows")
                event = st.dataframe(
                    etfs_filt,
                    # column_config=column_configuration,
                    use_container_width=True,
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="multi-row",
                )
                selected_rows = event.selection.rows
                etfs_filt2 = etfs_filt.iloc[selected_rows]

                # # Display selected ETF
                if etfs_filt2.shape[0] > 0:
                    st.write(f"Selected ETFs:")
                    st.write(', '.join(etfs_filt2.symbol.values))

    else:
        st.write(f"User ({st.user.name}) not authorized")
        st.stop()