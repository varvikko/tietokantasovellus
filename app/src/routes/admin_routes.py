from app import app
from middleware.ensure_author import admin_required

@app.route('/admin')
@admin_required
def admin():
    return '/admin'

@app.route('/admin/bans')
@admin_required
def bans():
    return '/admin/bans'

@app.route('/admin/reports')
@admin_required
def reports():
    return '/admin/reports'

@app.route('/admin/ban', methods=['POST'])
@admin_required
def ban():
    return '/admin/ban'

@app.route('/admin/ban/edit', methods=['POST'])
@admin_required
def edit_ban():
    return '/admin/ban/edit'

@app.route('/admin/ban/cancel', methods=['POST'])
@admin_required
def cancel_ban():
    return '/admin/ban/cancel'

@app.route('/admin/solve-report', methods=['POST'])
@admin_required
def solve_report():
    return '/admin/solve-report'

@app.route('/admin/new-board', methods=['POST'])
@admin_required
def new_board():
    return '/admin/new-board'

@app.route('/admin/delete-board', methods=['POST'])
@admin_required
def delete_board():
    return '/admin/delete-board'
