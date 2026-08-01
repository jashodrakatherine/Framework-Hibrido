# automation-framework

Monorepo de automatización de pruebas con módulos separados por tipo de
prueba, que comparten solo lo genérico:

```
shared/   Config, logger, excepciones base, utils, datos de prueba
web/      Automatización de UI sobre Playwright (BDD con pytest-bdd)
api/      Pruebas de API sobre requests (BDD con pytest-bdd)
```

`web/` y `api/` nunca se importan entre sí ni comparten abstracciones de
dominio: cada uno solo depende de `shared/`. Dentro de `web/`, un test nunca
llama a Playwright directamente: siempre pasa por `Pages` (heredan de
`BasePage`) o por un `Workflow` (proceso de negocio compuesto por varias
pantallas). Dentro de `api/`, un test nunca llama a `requests` directamente:
siempre pasa por `ApiClient`.

Tanto los tests web como los de API están escritos en Gherkin (BDD) con
`pytest-bdd`: cada caso es un `Scenario` en un archivo `.feature`,
implementado por *step definitions* en Python que hablan con
`Pages`/`Workflows` (web) o con `ApiClient` (api). Cada módulo tiene su
propio directorio `features/`, por lo que las step definitions de API
indican explícitamente su `features_base_dir` al llamar a `scenarios(...)`
en vez de depender del `bdd_features_base_dir` global (que apunta a
`web/tests/features`).

## Estructura

```
shared/
  config/       YAML de configuración por entorno (dev/qa/prod) + loader (settings.py)
  core/         logger, excepciones base (sin dependencias de Playwright/requests)
  utils/        faker, files, json_utils, excel, dates, retry
  data/         Datos de prueba (JSON/YAML)

web/
  core/         BrowserManager, PlaywrightManager, waits, screenshots, helpers
  pages/        Page Objects (heredan de BasePage)
  locators/     Selectores, separados de la lógica de las páginas
  workflows/    Procesos de negocio completos (ej. login_workflow.login())
  tests/
    features/   Escenarios en Gherkin (.feature) — el "qué" en lenguaje natural
    step_defs/  Step definitions en Python — el "cómo", habla con Pages/Workflows
    conftest.py Fixture `page` (levanta/cierra el navegador, captura fallos)

api/
  core/
    api_client.py   ApiClient, wrapper sobre requests
  tests/
    features/       Escenarios en Gherkin (.feature) — el "qué" en lenguaje natural
    step_defs/      Step definitions en Python — el "cómo", habla con ApiClient
    conftest.py     Fixture `api_client`

reports/      HTML report, Allure results, traces, videos (generado, no versionado)
screenshots/  Capturas automáticas en fallos de tests web (generado, no versionado)
logs/         Un log por ejecución (generado, no versionado)
```

## Instalación

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install
```

Copia `.env.example` a `.env` si necesitas variables de entorno (por ejemplo
`ENV=qa` o secretos que no deben ir en YAML).

## Configuración

`shared/config/config.yaml` trae los valores por defecto (navegador,
timeouts, trace/video, rutas, timeout de API). `shared/config/environments/<env>.yaml`
sobreescribe `base_url` (web), `api_base_url` (api) y lo que haga falta por
entorno. El entorno activo se elige con la variable de entorno `ENV` (por
defecto `dev`, definido en `config.yaml`).

Nunca hardcodear URLs: todo sale de `Settings` (`shared/config/settings.py`).

## Ejecutar pruebas

Las etiquetas de Gherkin (`@smoke`, `@regression`) se traducen automáticamente
a markers de pytest, así que se filtran igual en ambos módulos:

```powershell
pytest -m smoke
pytest -m regression
pytest                      # toda la suite (web + api)
pytest web/tests            # solo web
pytest api/tests            # solo api
$env:ENV="qa"; pytest       # contra otro entorno
```

Al finalizar se generan:
- `reports/report.html` — reporte HTML autocontenido
- `reports/allure-results/` — resultados para el reporte de Allure (ver sección siguiente)
- `reports/traces/<test>.zip` — trace de Playwright si un test web falló (`playwright show-trace <archivo>`)
- `screenshots/FAILED_<test>_*.png` y `.html` — captura + DOM en el momento del fallo (solo web)
- `logs/run_<timestamp>.log` — log detallado de la ejecución

## Ver el reporte de Allure

El CLI de Allure no está en el PATH del sistema (no había winget/scoop/npm
disponibles); quedó descargado localmente en `tools/allure-2.44.1/` (excluido
de git vía `.gitignore`). Para verlo:

```powershell
.\tools\allure-2.44.1\bin\allure.bat serve reports\allure-results
```

Esto abre un servidor local y el reporte en el navegador. Para generar un
reporte estático en vez de servirlo:

```powershell
.\tools\allure-2.44.1\bin\allure.bat generate reports\allure-results -o reports\allure-report --clean
```

Si más adelante instalas Allure globalmente (scoop, npm, etc.), el comando
se simplifica a `allure serve reports/allure-results`.

## Agregar un nuevo escenario web

1. Selectores nuevos → `web/locators/<pantalla>.py`
2. Pantalla nueva → `web/pages/<pantalla>_page.py`, heredando de `BasePage`
3. Proceso de negocio compuesto (opcional) → `web/workflows/<proceso>_workflow.py`
4. Escenario en lenguaje natural → `web/tests/features/<algo>.feature`, con
   `@smoke` o `@regression` según corresponda
5. Step definitions → `web/tests/step_defs/test_<algo>_steps.py`, con
   `scenarios("<algo>.feature")` y los steps hablando con `Pages`/`Workflows`
   (nunca con Playwright directo)

`web/tests/features/login.feature` + `web/tests/step_defs/test_login_steps.py`
corren contra [saucedemo.com](https://www.saucedemo.com) (sitio público
pensado para practicar automatización) y sirven como plantilla para nuevos
escenarios. `web/workflows/login_workflow.py` queda disponible para procesos
compuestos que necesiten loguearse como parte de un flujo más largo (ej. un
checkout).

## Agregar un nuevo escenario de API

1. Escenario en lenguaje natural → `api/tests/features/<algo>.feature`, con
   `@smoke` o `@regression` según corresponda
2. Step definitions → `api/tests/step_defs/test_<algo>_steps.py`, con
   `scenarios("<algo>.feature", features_base_dir=str(FEATURES_DIR))` (donde
   `FEATURES_DIR` apunta a `api/tests/features`) y los steps hablando con la
   fixture `api_client` (definida en `api/tests/conftest.py`), nunca con
   `requests` directo. `.get/.post/.put/.patch/.delete("/ruta", ...)`
   devuelven un `requests.Response` normal (`.status_code`, `.json()`, etc.);
   guárdalo en la fixture `context` (dict) para leerlo desde los steps
   `Then`.

`api/tests/features/demo_api.feature` +
`api/tests/step_defs/test_demo_api_steps.py` corren contra
[jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com) (API
pública gratuita, sin autenticación) y sirven de plantilla.

## Próximos pasos sugeridos

- Arquitectura de plugins (`plugins/database`, `plugins/email`, etc.) si el
  framework crece más allá de un solo equipo/proyecto
- Capa de IA (`ai/locator_healer.py`, generación de casos desde historias de
  usuario, etc.) una vez el core esté estable en uso real
