# Лабораторная работа 1. CI/CD с использованием SourceCraft на примере Hugo.

**Формулировка задания**:
1. Регистрация в sourcecraft.dev: используйте учетную запись Yandex.
2. Создание организации (организация должна быть публичной).
3. Создание репозитория (должен быть публичным).
4. Создать токены/ключи для работы посредством https и/или ssh:
    * https://sourcecraft.dev/portal/docs/en/sourcecraft/security/pat
    * https://sourcecraft.dev/portal/docs/en/sourcecraft/security/ssh
5. Клонировать репозиторий и запушить в SourceCraft основу для построения статического сайта (пример репозитория). 
    * Инструкция от самого Yandex https://sourcecraft.dev/portal/docs/ru/sourcecraft/tutorials/sites



Реализовать CI/CD-процесс публикации сайта на Hugo с использованием DevOps-платформы Sourcecraft:

1. Переписать существующий пайплайн на основе среды SourceCraft
2. Дополнить сценарии проверками синтаксиса Markdown (в виде отдельных шагов).



Ссылка на [репозиторий SourceCraft](https://sourcecraft.dev/antsib-public/hugo-portfolio?rev=main). Ссылка на [сайт](https://antsib-public.sourcecraft.site/hugo-portfolio/).

### Структура проекта

```
project/
├─ .sourcecraft/
│ | ├─ ci.yaml
│ │ └─ sites.yaml
│ ├─ archetypes/
│ │ └─ default.md
│ ├─ content/
│ │ ├─ ***/
│ │ ├─ **/
│ │ └─ about.md
│ ├─ resources/
│ │ ├─ main.scss_***
│ │ └─ main.scss_***
│ ├─ services/
│ │ └─ currency_rates.py
│ ├─ static/
│ │ └─ avatar.jpg
│ ├─ themes/***/**/*
│ │ └─ ***
├─ .gitmodules
├─ .hugo_build.lock
└─ hugo.toml
```

### CI
```yaml
on:
  push:
    workflows: [build-hugo-site]
    filter:
      branches: main

workflows:
  build-hugo-site:
    env:
      HUGO_VERSION: 0.157.0
    tasks:
      - name: Check-markdown-links
        cubes:
          - name: Run-markdown-link-check
            action: tcort/github-action-markdown-link-check@v1
            with:
              base-branch: main
              use-verbose-mode: yes

      - name: Build-and-deploy
        needs: [Check-markdown-links]
        cubes:
          - name: Download-Hugo
            script:
              # Download Hugo package
              - curl -LJO https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb

          - name: Check_File
            script:
              - ls -la

          - name: Install_Hugo
            script:
              # Install Hugo and remove downloaded package
              - sudo dpkg -i hugo_extended_${HUGO_VERSION}_linux-amd64.deb
              - rm hugo_extended_${HUGO_VERSION}_linux-amd64.deb

          - name: Check_Hugo
            script:
              - hugo version

          - name: Build_Site
            script:
              # Create directory for site build
              - mkdir public
              # Build site
              - hugo --config hugo.toml --destination ./public
              # Check build files
              - ls -la public/
          
          - name: Publish_Reliase_Site
            script:
              # git checkout
              - git checkout -b release
              # Check files in repository
              - ls -la
              # Add, commit and push
              - git add .
              - "git commit -m \"feat: Deploy Hugo site\""
              - "git push origin release -f"
```

## Описание проделанной работы

Для развёртывания был взят, созданный ранее, сайт на Hugo. 
Пайплайн CI/CD выполняет следующие действия:
1. Проверяет синтаксис ссылок в файлах Markdown.
2. Скачивает и устанавливает пакет Hugo.
3. Выводит в качестве отладочной информации установленную версию Hugo.
4. Создает директорию для сборки с сайтом и выполняет сборку.
5. Публикует сборку на sourcecraft.site.


### Анализ

В результате был создан пайплайн CI/CD, который автоматически собирает и публикует сайт на Hugo на sourcecraft.site.
Функционал CI поддерживает все необходимые функции для автоматического деплоя, однако стоит отметить тот факт, что на данный момент функционал уступает Github actions в плане встроенного функционала для разработки процессов CI/CD.

