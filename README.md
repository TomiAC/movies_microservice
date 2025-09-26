
# Cinema API

## English

This is a FastAPI application for managing a cinema. It provides a comprehensive API for managing movies, genres, directors, cinemas, auditoriums, and movie screenings.

### Features

*   CRUD operations for all resources.
*   Role-based access control (ADMIN, STAFF).
*   Search for movies by title and genre.
*   Initial data loading on startup.
*   SQLAlchemy for database interaction.
*   Testing with pytest.

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  Run the application:
    ```bash
    uvicorn main:app --reload
    ```
2.  The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

The following endpoints are available:

*   `/genres`: Manage genres.
*   `/directors`: Manage directors.
*   `/movies`: Manage movies.
*   `/cinemas`: Manage cinemas.
*   `/auditoriums`: Manage auditoriums.
*   `/functions`: Manage movie screenings.

For more details, please refer to the source code in the `routers` directory.

### Running Tests

To run the tests, use the following command:

```bash
pytest
```

---

## Español

Esta es una aplicación FastAPI para la gestión de un cine. Proporciona una API completa para la gestión de películas, géneros, directores, cines, auditorios y funciones de cine.

### Características

*   Operaciones CRUD para todos los recursos.
*   Control de acceso basado en roles (ADMIN, STAFF).
*   Búsqueda de películas por título y género.
*   Carga de datos inicial al iniciar la aplicación.
*   SQLAlchemy para la interacción con la base de datos.
*   Pruebas con pytest.

### Instalación

1.  Clona el repositorio:
    ```bash
    git clone <repository-url>
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

### Uso

1.  Ejecuta la aplicación:
    ```bash
    uvicorn main:app --reload
    ```
2.  La API estará disponible en `http://127.0.0.1:8000`.

### Endpoints de la API

Los siguientes endpoints están disponibles:

*   `/genres`: Gestionar géneros.
*   `/directors`: Gestionar directores.
*   `/movies`: Gestionar películas.
*   `/cinemas`: Gestionar cines.
*   `/auditoriums`: Gestionar auditorios.
*   `/functions`: Gestionar funciones de cine.

Para más detalles, por favor consulta el código fuente en el directorio `routers`.

### Ejecución de Pruebas

Para ejecutar las pruebas, utiliza el siguiente comando:

```bash
pytest
```
