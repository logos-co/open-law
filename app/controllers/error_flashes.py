from flask import flash


def create_error_flash(form):
    for field, errors in form.errors.items():
        field_label = form._fields[field].label.text
        for error in errors:
            flash(error.replace("Field", field_label), "danger")
