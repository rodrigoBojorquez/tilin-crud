def translate_error(error):
    error_type = error['type']
    ctx = error.get('ctx', {})

    translations = {
        "value_error.email": "El correo electrónico no es válido: {reason}",
        "string_too_short": "Asegúrese de que este valor tenga al menos {min_length} caracteres",
        "value_error.integer": "El valor no es un número entero válido",
        "value_error.missing": "Campo requerido"
    }

    if error_type in translations:
        msg_template = translations[error_type]
        msg = msg_template.format(**ctx)
    else:
        msg = error['msg']

    return msg

def format_errors(errors, model):
    formatted_errors = []
    for error in errors:
        field_name = error['loc'][0]
        field_info = model.__fields__[field_name]
        field_title = field_info.title
        translated_msg = translate_error(error)
        formatted_error_msg = f"{field_title}: {translated_msg}"
        formatted_errors.append(formatted_error_msg)
    return formatted_errors
