import logging.config
from functools import wraps


class LogIndentation:
    """Pour indenter les logs lorsque l'on rentre dans une nouvelle méthode"""

    current_indentation = 0

    @classmethod
    def increase(cls):
        cls.current_indentation += 1

    @classmethod
    def decrease(cls):
        cls.current_indentation = max(cls.current_indentation - 1, 0)

    @classmethod
    def get(cls):
        return "    " * cls.current_indentation


def truncate_result(result):
    """Retourne une version courte du résultat pour le log"""
    if isinstance(result, list):
        snippet = [str(item) for item in result[:3]]
        return f"{snippet} ... ({len(result)} elements)"
    elif isinstance(result, dict):
        snippet = {str(k): str(v) for i, (k, v) in enumerate(result.items()) if i < 3}
        return f"{snippet} ... ({len(result)} elements)"
    elif isinstance(result, str) and len(result) > 50:
        return f"{result[:50]} ... ({len(result)} caractères)"
    return str(result)


def log(func):
    """Décorateur pour logger l'entrée et sortie des méthodes"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        LogIndentation.increase()
        indentation = LogIndentation.get()

        class_name = args[0].__class__.__name__ if args else ""
        method_name = func.__name__

        # Paramètres
        args_list = list(args[1:]) + list(kwargs.values())
        param_names = func.__code__.co_varnames[1 : func.__code__.co_argcount]
        for i, name in enumerate(param_names):
            if i < len(args_list) and name.lower() in ["password", "passwd", "pwd", "pass", "mot_de_passe", "mdp"]:
                args_list[i] = "*****"
        args_list = tuple(args_list)

        logger.info(f"{indentation}{class_name}.{method_name}{args_list} - DEBUT")
        result = func(*args, **kwargs)
        logger.info(f"{indentation}{class_name}.{method_name}{args_list} - FIN")
        logger.info(f"{indentation}   └─> Sortie : {truncate_result(result)}")

        LogIndentation.decrease()
        return result

    return wrapper
