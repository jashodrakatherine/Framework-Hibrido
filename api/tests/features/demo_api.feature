Feature: Posts en JSONPlaceholder
  Como consumidor de la API de posts
  Quiero consultar y crear posts
  Para verificar el contrato HTTP del servicio

  @smoke
  Scenario: Obtener un post existente por id
    When solicito el post con id 1
    Then la respuesta debe tener status 200
    And el post debe tener id 1
    And el post debe tener título

  @smoke
  Scenario: Crear un post nuevo
    When creo un post con título "foo" y cuerpo "bar" para el usuario 1
    Then la respuesta debe tener status 201
    And el post creado debe tener título "foo"
    And el post creado debe tener id

  @regression
  Scenario: Solicitar un post inexistente devuelve 404
    When solicito el post con id 99999
    Then la respuesta debe tener status 404
