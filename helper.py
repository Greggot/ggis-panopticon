import os


def existence_configs_check(
        configs_target_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), 'env', 'skird_config')),
        silent: bool = True) -> bool:
    if os.path.isdir(configs_target_path):
        if len(os.listdir(configs_target_path)) == 0:
            if not silent:
                print("Директория конфигураций существует, но она пуста")
                return False
        return True
    if not silent:
        print("Директория конфигураций не существует")
    return False


def prepare_configs_path(
        configs_target_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), 'env', 'skird_config')),
        overwrite: bool = False) -> bool:
    if os.path.isdir(configs_target_path):
        if overwrite:
            try:
                import shutil
                shutil.rmtree(configs_target_path)
            except Exception as e:
                print(e)
                return False
        else:
            return True

    try:
        import shutil
        shutil.copytree(os.path.abspath(os.path.join(os.path.dirname(__file__), 'json', 'skird_config')),
                        configs_target_path)
        return True
    except Exception as e:
        print(e)
        return False


def check_and_prepare_configs_path() -> None:
    if not existence_configs_check(silent=True):
        if not prepare_configs_path():
            print("Пути конфигураций для карточек не найдены, а создать их автоматически не вышло")
            print("Возможно, отсутствует модуль 'shutil'")
            print(f"Вы можете руками скопировать {os.path.join(os.path.dirname(__file__), 'json', 'skird_config')} в "
                  f"{os.path.join(os.path.dirname(__file__), 'env', 'skird_config')} ")
            exit(1)
