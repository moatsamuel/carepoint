from functools import wraps
from flask import session, redirect, url_for, flash, abort


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to continue.', 'error')
                return redirect(url_for('auth.login'))

            if session.get('role') not in allowed_roles:
                abort(403)

            return view(*args, **kwargs)
        return wrapped
    return decorator