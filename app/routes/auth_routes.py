from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from . import auth_bp
from app.models.user import User

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """顯示註冊頁面"""
    pass

@auth_bp.route('/register', methods=['POST'])
def handle_register():
    """處理註冊表單提交"""
    pass

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """顯示登入頁面"""
    pass

@auth_bp.route('/login', methods=['POST'])
def handle_login():
    """處理登入表單提交"""
    pass

@auth_bp.route('/logout', methods=['GET'])
def handle_logout():
    """處理登出"""
    pass
