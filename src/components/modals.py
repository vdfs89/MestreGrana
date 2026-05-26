"""Modal and alert components."""

try:
    import streamlit as st
except Exception:
    from _stubs import st


def show_alert(message, alert_type="info", dismiss=True):
    """Show alert message.
    
    Args:
        message: str - Alert message
        alert_type: str - 'success', 'error', 'warning', 'info'
        dismiss: bool - Show dismiss button
    """
    if alert_type == "success":
        st.success(message)
    elif alert_type == "error":
        st.error(message)
    elif alert_type == "warning":
        st.warning(message)
    else:
        st.info(message)


def show_confirm_dialog(title, message, yes_label="Sim", no_label="Não"):
    """Show confirmation dialog.
    
    Args:
        title: str - Dialog title
        message: str - Dialog message
        yes_label: str - Yes button label
        no_label: str - No button label
    
    Returns:
        bool - True if yes clicked, False if no clicked
    """
    st.subheader(title)
    st.write(message)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(yes_label, key=f"confirm_{title}"):
            return True
    with col2:
        if st.button(no_label, key=f"cancel_{title}"):
            return False
    
    return None


def show_loading_spinner(message="Processando..."):
    """Show loading spinner context manager.
    
    Args:
        message: str - Loading message
    
    Returns:
        context manager
    """
    return st.spinner(message)


def show_progress(current, total, label="Progresso"):
    """Show progress bar.
    
    Args:
        current: int - Current value
        total: int - Total value
        label: str - Progress label
    """
    if total <= 0:
        return
    
    percentage = current / total
    st.progress(percentage, text=f"{label}: {current}/{total}")


def show_toast(message, duration=3):
    """Show toast notification.
    
    Args:
        message: str - Toast message
        duration: int - Duration in seconds (Streamlit default handling)
    """
    # Streamlit handles toast internally
    st.toast(message)


def show_sidebar_alert(message, alert_type="info"):
    """Show alert in sidebar.
    
    Args:
        message: str - Alert message
        alert_type: str - 'success', 'error', 'warning', 'info'
    """
    with st.sidebar:
        if alert_type == "success":
            st.success(message)
        elif alert_type == "error":
            st.error(message)
        elif alert_type == "warning":
            st.warning(message)
        else:
            st.info(message)


def show_expandable(title, content_fn):
    """Show expandable section.
    
    Args:
        title: str - Section title
        content_fn: callable - Function that renders content
    """
    with st.expander(title):
        content_fn()


def show_tabs(tab_names, content_fns):
    """Show tabs with dynamic content.
    
    Args:
        tab_names: list - Names of tabs
        content_fns: list - Functions that render tab content
    """
    if len(tab_names) != len(content_fns):
        raise ValueError("Number of tab names must match number of content functions")
    
    tabs = st.tabs(tab_names)
    for tab, content_fn in zip(tabs, content_fns):
        with tab:
            content_fn()
