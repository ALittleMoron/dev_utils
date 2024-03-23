NAME := dev_utils
POETRY := $(shell command -v poetry 2> /dev/null)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo -e "Пожалуйста, испольйте \033[0;33m'make <target>'\033[0m где <target> одна из команд:"
	@echo ""
	@echo -e "  \033[0;33minstall\033[0m         запускает установку пакеты и подготовку окружение"
	@echo -e "  \033[0;33mshell\033[0m           запускает ipython оболочку"
	@echo -e "  \033[0;33mclean\033[0m           запускает удаление всех временных файлов"
	@echo -e "  \033[0;33mlint\033[0m            запускает проверку кода"
	@echo -e "  \033[0;33mformat\033[0m          запускает форматирование кода"
	@echo -e "  \033[0;33mtest\033[0m            запускает все тесты проекта"
	@echo -e "  \033[0;33mtest_docker\033[0m     запускает все тесты проекта в докере"

	@echo ""
	@echo -e "Проверьте \033[0;33mMakefile\033[0m, чтобы понимать, что какая команда делает конкретно."


.PHONY: install
install:
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install


.PHONY: shell
shell:
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(ENV_VARS_PREFIX) $(POETRY) run ipython --no-confirm-exit --no-banner --quick \
	--InteractiveShellApp.extensions="autoreload" \
	--InteractiveShellApp.exec_lines="%autoreload 2" \
	--InteractiveShellApp.exec_lines="import sys, pathlib, os" \
	--InteractiveShellApp.exec_lines="sys.path.insert(0, (pathlib.Path(os.getcwd()) / 'src').as_posix())" \
	--InteractiveShellApp.exec_lines="from app.core.models import tables" \
	--InteractiveShellApp.exec_lines="from app.api.v1.dependencies.databases import get_session" \
	--InteractiveShellApp.exec_files="scripts/ipython_shell_enter_message.py"

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf ./logs/*

.PHONY: lint
lint:
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) run pyright $(NAME)
	$(POETRY) run isort --settings-path ./pyproject.toml --check-only $(NAME)
	$(POETRY) run black --config ./pyproject.toml --check $(NAME) --diff
	$(POETRY) run ruff check $(NAME)
	$(POETRY) run vulture $(NAME) --min-confidence 100
	$(POETRY) run bandit --configfile ./pyproject.toml -r ./$(NAME)/app

.PHONY: format
format:
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) run isort --settings-path ./pyproject.toml $(NAME)
	$(POETRY) run black --config ./pyproject.toml $(NAME)

.PHONY: test
test:
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) run pytest ./tests --cov-report xml --cov-fail-under 60 --cov ./$(NAME) -v


.PHONY: test_docker
test_docker:
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(ENV_VARS_PREFIX) docker-compose -f docker/docker-compose-test.yaml up --build