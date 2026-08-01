Feature: Login en SauceDemo
  Como usuario de SauceDemo
  Quiero iniciar sesión
  Para acceder al catálogo de productos

  Background:
    Given que estoy en la página de login

  @smoke
  Scenario: Login exitoso con usuario estándar
    When inicio sesión con el usuario "standard_user" y la contraseña "secret_sauce"
    Then debo ver el dashboard cargado
    And debo ver al menos un producto listado

  @smoke
  Scenario: Usuario bloqueado no puede iniciar sesión
    When inicio sesión con el usuario "locked_out_user" y la contraseña "secret_sauce"
    Then debo ver un error de login

  @regression
  Scenario: Login falla con contraseña incorrecta
    When inicio sesión con el usuario "standard_user" y la contraseña "clave_incorrecta"
    Then debo ver un error de login

  @regression
  Scenario: Login falla con campos vacíos
    When inicio sesión con el usuario "" y la contraseña ""
    Then debo ver un error de login
