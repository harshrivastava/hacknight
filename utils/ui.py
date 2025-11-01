"""
Shared utilities for UI components and styles
"""

import streamlit as st
from pathlib import Path
import json

def load_css(css_file):
    """Load and inject custom CSS"""
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def custom_card(content, animate=True):
    """Render content in a custom styled card"""
    animation_class = "animate-fade-in" if animate else ""
    return st.markdown(f'''
        <div class="naborly-card {animation_class}">
            {content}
        </div>
    ''', unsafe_allow_html=True)

def status_badge(text, status):
    """Render a colored status badge"""
    status_class = {
        "in-stock": "status-in-stock",
        "limited": "status-limited",
        "out": "status-out"
    }.get(status.lower().replace(" ", "-"), "")
    
    return st.markdown(f'''
        <span class="status-badge {status_class}">
            {text}
        </span>
    ''', unsafe_allow_html=True)

def add_logo():
    """Add a small logo/brand in the sidebar"""
    st.sidebar.markdown('''
        <div style="text-align: center; margin-bottom: 20px;">
            <h3>📍 Naborly</h3>
            <p style="color: #666;">Your Local Community App</p>
        </div>
    ''', unsafe_allow_html=True)

# JavaScript interactivity helpers
def add_js_interactivity():
    """Add JavaScript functionality"""
    st.components.v1.html('''
        <script>
        // Custom alert function
        function showNaborlyAlert(message) {
            const alert = document.createElement('div');
            alert.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #2563eb;
                color: white;
                padding: 1rem;
                border-radius: 0.5rem;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                z-index: 9999;
                animation: slideIn 0.3s ease-out forwards;
            `;
            alert.innerHTML = message;
            document.body.appendChild(alert);
            
            setTimeout(() => {
                alert.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => alert.remove(), 300);
            }, 3000);
        }

        // Add animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);

        // Make function available to Python
        window.showAlert = showNaborlyAlert;
        </script>
    ''', height=0)

def show_alert(message):
    """Trigger a JavaScript alert"""
    js = f'''
        <script>
            if (window.showAlert) {{
                window.showAlert("{message}");
            }}
        </script>
    '''
    st.components.v1.html(js, height=0)