from app import app

@app.route('/admin')
def admin():
    return '/admin'

@app.route('/admin/bans')
def bans():
    return '/admin/bans'

@app.route('/admin/reports')
def reports():
    return '/admin/reports'

@app.route('/admin/ban', methods=['POST'])
def ban():
    return '/admin/ban'

@app.route('/admin/ban/edit', methods=['POST'])
def edit_ban():
    return '/admin/ban/edit'

@app.route('/admin/ban/cancel', methods=['POST'])
def cancel_ban():
    return '/admin/ban/cancel'

@app.route('/admin/solve-report', methods=['POST'])
def solve_report():
    return '/admin/solve-report'

@app.route('/admin/new-board', methods=['POST'])
def new_board():
    return '/admin/new-board'

@app.route('/admin/delete-board', methods=['POST'])
def delete_board():
    return '/admin/delete-board'
