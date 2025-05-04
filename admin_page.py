from google.oauth2 import service_account
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st

from src.utils import get_ishares_etfs, run_query_nocache, execute_query, insert_df_to_table
from src.queries import Queries

USER_DATASET = "stocks_user_data"
ETFS_TABLE = "ETFS_to_track"
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
    username = st.user.name
    useremail = st.user.email
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account_admin"])

    # Check for admin status based on email domain
    if st.user.email in st.secrets.security.admins:
        st.write(f"Welcome, {username}!")
        
        # Show admin-only features here
        etfs = get_ishares_etfs()

        user_etfs_query = queries.user_etfs(
                useremail,
                table=f'{USER_DATASET}.{ETFS_TABLE}')
        df = run_query_nocache(
            user_etfs_query,
            _credentials=credentials)
        
        symbols_tracked = df.symbol.unique()
        
        manager, browser = st.tabs(["Manager", "Browser"])
        
        with manager:
            st.subheader(f"Manage Tracked ETFs:")
            if df.shape[0] > 0:
                st.write(f"Showing currently tracked ETFs by user: {useremail}.")
                st.write("Select rows to remove:")
                event = st.dataframe(
                        df,
                        # column_config=column_configuration,
                        use_container_width=True,
                        hide_index=True,
                        on_select="rerun",
                        selection_mode="multi-row",
                    )
                selected_rows = event.selection.rows
                symbols_to_remove = df['symbol'].iloc[selected_rows].values
                # print(f'symbols: {symbols}, len={len(symbols)}')
                if len(symbols_to_remove) > 0:
                    symbols = [f"'{symbol}'" for symbol in symbols_to_remove]
                    symbols_str = ', '.join(symbols)
                    confirmed = st.button(f"Confirm removing etfs: {symbols_str}")
                    if confirmed:
                        query = f"DELETE FROM stocks_user_data.ETFS_to_track WHERE symbol IN ({symbols_str}) AND user = '{useremail}'"
                        execute_query(query, credentials)
            else:
                st.write(f"Currently no tracked ETFs by user: {useremail}")
            
            st.write("Add new ETFs:")
            # Initialize session state variables
            if 'selection' not in st.session_state:
                st.session_state.selection = []
            if 'final_list' not in st.session_state:     
                st.session_state.final_list = []
            if 'confirmed' not in st.session_state:
                st.session_state.confirmed = False
            # Input field
            user_input = st.text_input("Enter item to add:")
            user_input = user_input.upper().strip()
            # Button to add item
            if st.button("Add to List"):
                if user_input not in symbols_tracked:
                    if user_input in etfs.symbol.values:
                        if user_input not in st.session_state.selection:
                            st.session_state.selection.append(user_input)
                            st.session_state.final_list = st.session_state.selection.copy()  # Force update
                            st.success(f"'{user_input}' added to the list.")
                        else:
                            st.info(f"'{user_input}' is already in the list.")
                    else:
                        st.warning(f"'{user_input}' is not available")
                        st.write("Enter one of: {}".format(', '.join(etfs.symbol.values)))
                else:
                    st.info(f"'{user_input}' is already tracked.")

            # Show current list
            if st.session_state.final_list:
                st.session_state.final_list = st.multiselect(
                    "Select items to keep in list:",
                    options=st.session_state.selection,
                    default=st.session_state.selection,
                    # on_change=update_selection
                    )
                st.session_state.selection = st.session_state.final_list.copy()

            # Confirm addition
            if st.button("Confirm Addition"):
                st.session_state.confirmed = True

            if st.session_state.confirmed:
                list_str = ', '.join(st.session_state.final_list)
                st.info(f"ETFs to be added: {list_str}")
                # create dataframe based on values:
                df = pd.DataFrame({
                    'symbol': st.session_state.final_list,
                    'user': useremail})
                # print(df.head())
                # adding to BQ table
                Query = insert_df_to_table(
                    df=df,
                    dataset_table=f'{USER_DATASET}.{ETFS_TABLE}',
                    credentials=credentials)
            
        with browser:
            st.subheader(f"Browse ETFs:")
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
        st.write(f"User {username} ({useremail}) not authorized")
        st.stop()