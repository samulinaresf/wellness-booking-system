Documentación técnica
    Las clases en FastAPI se escribirán en base a la sintaxis por convención de python que es snake case en el nombre de las variables y nombres en singular.

La primera clase es User que hará referencia a los usuarios de la plataforma. Es una clase generalista que recibirá todos los registros de usuarios ya sean clientes, profesionales o desarrolladores. 

Los campos de la tabla user en la base de datos se corresponderán con los atributos de la clase User en el archivo de models. Estos serán:

- user_id
- name
- email
- password
- phone_number
- role
- profile_picture:
- bio:
- created_at
- updated_at
- is_active
- last_login_at

La clase UserRole será de tipo cadena de texto, y se listarán el número de opciones que van a ser user, admin y superadmin. El usuario solo va a tener privilegios relacionados con sus citas. Podrá reservar, consultar las citas disponibles y modificar tanto la información de su cuenta como de sus citas. Los admin tendrán otros privilegios a parte de modificar su información personal y es la modificación de citas en su totalidad, podrá añadir más horas disponibles o menos, y editar cualquier tipo de reservas. Por último el superadmin va a tener absolutamente todos los privilegios.